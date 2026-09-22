from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import math
from typing import Iterable, Sequence, Tuple

from .core import Sample, ThreePlusOneMLP


Matrix = Tuple[Tuple[float, ...], ...]
ComplexVector = Tuple[complex, ...]


_BRANCH_REAL = (
    2.0 / math.sqrt(6.0),
    -1.0 / math.sqrt(6.0),
    -1.0 / math.sqrt(6.0),
)

_BRANCH_IMAG = (
    0.0,
    1.0 / math.sqrt(2.0),
    -1.0 / math.sqrt(2.0),
)


@dataclass(frozen=True)
class TransverseEpochRecord:
    epoch: int
    mse: float
    singular_values: Tuple[float, float, float, float]
    unstable_dimension: int
    cumulative_singular_values: Tuple[float, float, float, float]

    @property
    def top_growth_rate(self) -> float:
        """One-epoch log singular growth rate."""
        return math.log(self.singular_values[0])

    @property
    def cumulative_top_gain(self) -> float:
        return self.cumulative_singular_values[0]


def _local_state(net: ThreePlusOneMLP, unit: int) -> tuple[float, ...]:
    return (
        float(net.output_w[unit + 1]),
        *tuple(float(v) for v in net.hidden_w[unit]),
    )


def transverse_residual(
    net: ThreePlusOneMLP,
    group: Sequence[int] = (0, 1, 2),
) -> ComplexVector:
    """
    Extract the actual hidden residual among a three-unit symmetric group.

    For local unit states

        q_i = (output weight, hidden bias, hidden x1 weight, hidden x2 weight),

    use the branch-aligned orthonormal basis

        c_R = (2,-1,-1)/sqrt(6)
        c_I = (0,1,-1)/sqrt(2).

    The complex four-channel residual is

        Z = sum_i (c_R[i] + i c_I[i]) q_i.

    Z=0 exactly when the three local states coincide (within their affine
    three-copy subspace).

    In this convention, the three singleton rays are at phases
    0, +2*pi/3 and -2*pi/3.
    """
    if len(group) != 3:
        raise ValueError("transverse_residual requires exactly three units")

    states = [_local_state(net, int(i)) for i in group]
    width = len(states[0])

    out = []
    for channel in range(width):
        re = sum(_BRANCH_REAL[i] * states[i][channel] for i in range(3))
        im = sum(_BRANCH_IMAG[i] * states[i][channel] for i in range(3))
        out.append(complex(re, im))
    return tuple(out)


def transverse_residual_norm(
    net: ThreePlusOneMLP,
    group: Sequence[int] = (0, 1, 2),
) -> float:
    return math.sqrt(sum(abs(z) ** 2 for z in transverse_residual(net, group)))


def add_transverse_seed(
    net: ThreePlusOneMLP,
    *,
    amplitude: float,
    phase: float,
    channel: int = 0,
    group: Sequence[int] = (0, 1, 2),
) -> None:
    """
    Add a mean-zero transverse perturbation to one local parameter channel.

    channel=0 is the hidden-to-output weight.
    channels 1..3 are hidden bias, x1 and x2 incoming weights.

    The three exact singleton rays are phase 0, +2*pi/3 and -2*pi/3.
    """
    if len(group) != 3:
        raise ValueError("add_transverse_seed requires exactly three units")
    if channel not in (0, 1, 2, 3):
        raise ValueError("channel must be 0, 1, 2, or 3")

    c = math.cos(float(phase))
    s = math.sin(float(phase))
    pattern = tuple(
        float(amplitude) * (_BRANCH_REAL[i] * c + _BRANCH_IMAG[i] * s)
        for i in range(3)
    )

    for pos, unit in enumerate(group):
        unit = int(unit)
        if channel == 0:
            net.output_w[unit + 1] += pattern[pos]
        else:
            net.hidden_w[unit][channel - 1] += pattern[pos]


def _identity(n: int) -> list[list[float]]:
    return [
        [1.0 if i == j else 0.0 for j in range(n)]
        for i in range(n)
    ]


def _matmul(a: Sequence[Sequence[float]], b: Sequence[Sequence[float]]) -> list[list[float]]:
    rows = len(a)
    inner = len(b)
    cols = len(b[0])
    return [
        [
            sum(float(a[i][k]) * float(b[k][j]) for k in range(inner))
            for j in range(cols)
        ]
        for i in range(rows)
    ]


def _transpose(a: Sequence[Sequence[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*a)]


def _jacobi_eigenvalues_symmetric(
    matrix: Sequence[Sequence[float]],
    *,
    tolerance: float = 1e-14,
    max_iterations: int = 1000,
) -> list[float]:
    """
    Small dependency-free Jacobi eigensolver.

    Used only on the 4x4 positive-semidefinite matrix M^T M.
    """
    a = [list(map(float, row)) for row in matrix]
    n = len(a)

    for _ in range(max_iterations):
        p = 0
        q = 0
        largest = 0.0

        for i in range(n):
            for j in range(i + 1, n):
                value = abs(a[i][j])
                if value > largest:
                    largest = value
                    p, q = i, j

        if largest < tolerance:
            break

        app = a[p][p]
        aqq = a[q][q]
        apq = a[p][q]

        angle = 0.5 * math.atan2(2.0 * apq, aqq - app)
        c = math.cos(angle)
        s = math.sin(angle)

        for k in range(n):
            if k == p or k == q:
                continue
            akp = a[k][p]
            akq = a[k][q]
            a[k][p] = a[p][k] = c * akp - s * akq
            a[k][q] = a[q][k] = s * akp + c * akq

        a[p][p] = c * c * app - 2.0 * s * c * apq + s * s * aqq
        a[q][q] = s * s * app + 2.0 * s * c * apq + c * c * aqq
        a[p][q] = a[q][p] = 0.0

    return sorted((a[i][i] for i in range(n)), reverse=True)


def singular_values(matrix: Sequence[Sequence[float]]) -> tuple[float, ...]:
    ata = _matmul(_transpose(matrix), matrix)
    eigenvalues = _jacobi_eigenvalues_symmetric(ata)
    return tuple(math.sqrt(max(0.0, value)) for value in eigenvalues)


def sample_transverse_matrix(
    net: ThreePlusOneMLP,
    x: Sequence[float],
    target: float,
    *,
    representative_unit: int = 0,
) -> Matrix:
    """
    Exact first-order transverse map for one SGD sample on the S3 manifold.

    Let one member of the three-copy group have local state

        q = (a, w0, w1, w2),

    and let xhat=(1,x1,x2).

    For any mean-zero difference among the three copies, the first-order
    perturbation of the network output vanishes.  Therefore the output delta
    is shared by all three copies and the local perturbation evolves by the
    same 4x4 matrix K:

        [ 1                 eta*d*g*xhat^T                  ]
        [ eta*d*g*xhat      I + eta*d*a*g'*xhat*xhat^T     ]

    where g=h(1-h) and g'=g(1-2h).

    This is the exact linearization of the existing ThreePlusOneMLP update,
    not a separate reduced model.
    """
    if len(x) != net.inputs:
        raise ValueError(f"expected {net.inputs} inputs, got {len(x)}")
    if net.inputs != 2:
        raise ValueError("current transverse matrix implementation expects 2 inputs")

    h, y = net._forward(x)
    unit = int(representative_unit)
    hv = float(h[unit])
    output_delta = (float(target) - y) * y * (1.0 - y)
    a = float(net.output_w[unit + 1])

    xhat = (1.0, float(x[0]), float(x[1]))
    g = hv * (1.0 - hv)
    g_prime = g * (1.0 - 2.0 * hv)
    eta = float(net.learning_rate)

    out = _identity(4)

    for j in range(3):
        value = eta * output_delta * g * xhat[j]
        out[0][j + 1] = value
        out[j + 1][0] = value

    coeff = eta * output_delta * a * g_prime
    for i in range(3):
        for j in range(3):
            out[i + 1][j + 1] += coeff * xhat[i] * xhat[j]

    return tuple(tuple(row) for row in out)


def epoch_transverse_matrix(
    net: ThreePlusOneMLP,
    samples: Iterable[Sample],
    *,
    representative_unit: int = 0,
) -> Matrix:
    """
    Compose exact sample transverse matrices over one ordered training epoch.

    The input network is not mutated.
    """
    data = list(samples)
    if not data:
        raise ValueError("samples must not be empty")

    work = deepcopy(net)
    total = _identity(4)

    for x, target in data:
        step = sample_transverse_matrix(
            work,
            x,
            target,
            representative_unit=representative_unit,
        )
        total = _matmul(step, total)
        work.train_one(x, target)

    return tuple(tuple(row) for row in total)


def scan_transverse_growth(
    net: ThreePlusOneMLP,
    samples: Iterable[Sample],
    *,
    epochs: int,
    instability_tolerance: float = 1e-12,
) -> Tuple[TransverseEpochRecord, ...]:
    """
    Follow the exact S3-symmetric learning trajectory and measure transverse
    amplification at every epoch.

    The one-epoch map is M_e.  The cumulative tangent map is

        C_e = M_e M_{e-1} ... M_1.

    singular_values(M_e) measure instantaneous finite-time amplification.
    singular_values(C_e) measure accumulated amplification from initialization.
    """
    if epochs < 1:
        raise ValueError("epochs must be positive")

    data = list(samples)
    if not data:
        raise ValueError("samples must not be empty")

    work = deepcopy(net)
    cumulative = _identity(4)
    records = []

    for epoch in range(1, epochs + 1):
        matrix = epoch_transverse_matrix(work, data)
        values = singular_values(matrix)
        cumulative = _matmul(matrix, cumulative)
        cumulative_values = singular_values(cumulative)

        for x, target in data:
            work.train_one(x, target)

        unstable = sum(
            value > 1.0 + float(instability_tolerance)
            for value in values
        )

        records.append(
            TransverseEpochRecord(
                epoch=epoch,
                mse=work.mse(data),
                singular_values=(
                    float(values[0]),
                    float(values[1]),
                    float(values[2]),
                    float(values[3]),
                ),
                unstable_dimension=int(unstable),
                cumulative_singular_values=(
                    float(cumulative_values[0]),
                    float(cumulative_values[1]),
                    float(cumulative_values[2]),
                    float(cumulative_values[3]),
                ),
            )
        )

    return tuple(records)


@dataclass(frozen=True)
class TransverseAnisotropyResult:
    """
    Dominant-channel nonlinear transverse reduction over a fixed training course.

    input_direction:
        dominant right singular direction of the cumulative linear map
    output_direction:
        corresponding dominant left singular direction
    linear_gain:
        projected +1 Fourier harmonic divided by amplitude
    quadratic_coefficient:
        projected -2 Fourier harmonic divided by amplitude^2

    The -2 harmonic is the C3-equivariant quadratic anisotropy:
        z -> lambda z + nu conjugate(z)^2 + O(|z|^3).
    """

    epochs: int
    amplitude: float
    input_direction: Tuple[float, float, float, float]
    output_direction: Tuple[float, float, float, float]
    linear_gain: complex
    quadratic_coefficient: complex


def add_transverse_vector_seed(
    net: ThreePlusOneMLP,
    *,
    direction: Sequence[float],
    amplitude: float,
    phase: float,
    group: Sequence[int] = (0, 1, 2),
) -> None:
    """
    Add an arbitrary four-channel complex transverse residual

        Z = amplitude * exp(i*phase) * direction

    where direction is real in parameter-channel space.
    """
    if len(group) != 3:
        raise ValueError("add_transverse_vector_seed requires exactly three units")
    if len(direction) != 4:
        raise ValueError("direction must contain four channel values")

    c = math.cos(float(phase))
    s = math.sin(float(phase))
    values = [float(amplitude) * float(v) for v in direction]

    for pos, unit in enumerate(group):
        unit = int(unit)
        copy_factor_re = _BRANCH_REAL[pos] * c + _BRANCH_IMAG[pos] * s
        copy_factor_im = 0.0
        # direction is real, so the desired complex residual phase is carried
        # entirely by the copy-space basis.
        del copy_factor_im

        for channel, value in enumerate(values):
            delta = value * copy_factor_re
            if channel == 0:
                net.output_w[unit + 1] += delta
            else:
                net.hidden_w[unit][channel - 1] += delta


def cumulative_transverse_matrix(
    net: ThreePlusOneMLP,
    samples: Iterable[Sample],
    *,
    epochs: int,
) -> Matrix:
    """Compose the exact linear transverse maps over a fixed training course."""
    if epochs < 1:
        raise ValueError("epochs must be positive")

    data = list(samples)
    if not data:
        raise ValueError("samples must not be empty")

    work = deepcopy(net)
    cumulative = _identity(4)

    for _ in range(epochs):
        matrix = epoch_transverse_matrix(work, data)
        cumulative = _matmul(matrix, cumulative)
        for x, target in data:
            work.train_one(x, target)

    return tuple(tuple(row) for row in cumulative)


def _matvec(
    matrix: Sequence[Sequence[float]],
    vector: Sequence[float],
) -> list[float]:
    return [
        sum(float(row[j]) * float(vector[j]) for j in range(len(vector)))
        for row in matrix
    ]


def _normalize_real(vector: Sequence[float]) -> list[float]:
    n2 = sum(float(v) * float(v) for v in vector)
    if n2 <= 0.0:
        raise ValueError("cannot normalize the zero vector")
    scale = 1.0 / math.sqrt(n2)
    return [float(v) * scale for v in vector]


def dominant_singular_pair(
    matrix: Sequence[Sequence[float]],
    *,
    iterations: int = 200,
) -> tuple[float, tuple[float, ...], tuple[float, ...]]:
    """
    Dependency-free dominant singular triplet (sigma, left, right).

    The sign convention is fixed by requiring the largest-magnitude component
    of the right singular vector to be positive.
    """
    ata = _matmul(_transpose(matrix), matrix)
    v = _normalize_real((1.0, 0.5, -0.25, 0.75))

    for _ in range(iterations):
        next_v = _matvec(ata, v)
        v = _normalize_real(next_v)

    pivot = max(range(len(v)), key=lambda i: abs(v[i]))
    if v[pivot] < 0.0:
        v = [-x for x in v]

    mv = _matvec(matrix, v)
    sigma = math.sqrt(sum(x * x for x in mv))
    if sigma == 0.0:
        raise ValueError("dominant singular value is zero")

    u = [x / sigma for x in mv]
    return sigma, tuple(u), tuple(v)


def projected_training_harmonic(
    net: ThreePlusOneMLP,
    samples: Iterable[Sample],
    *,
    epochs: int,
    input_direction: Sequence[float],
    output_direction: Sequence[float],
    amplitude: float,
    harmonic: int,
    phase_samples: int = 12,
) -> complex:
    """
    Fourier coefficient of the actual nonlinear training map.

    If the projected map has

        y(theta)
          = lambda * eps * exp(i theta)
          + nu * eps^2 * exp(-2 i theta)
          + ...

    then harmonic=1 extracts the linear term and harmonic=-2 extracts the
    C3-equivariant quadratic anisotropy.
    """
    if epochs < 1:
        raise ValueError("epochs must be positive")
    if amplitude <= 0.0:
        raise ValueError("amplitude must be positive")
    if phase_samples < 6 or phase_samples % 3 != 0:
        raise ValueError("phase_samples must be a multiple of 3 and at least 6")
    if len(input_direction) != 4 or len(output_direction) != 4:
        raise ValueError("input_direction and output_direction must have length 4")

    data = list(samples)
    if not data:
        raise ValueError("samples must not be empty")

    total = 0j

    for sample_index in range(phase_samples):
        phase = 2.0 * math.pi * sample_index / phase_samples
        work = deepcopy(net)
        add_transverse_vector_seed(
            work,
            direction=input_direction,
            amplitude=amplitude,
            phase=phase,
        )

        for _ in range(epochs):
            for x, target in data:
                work.train_one(x, target)

        residual = transverse_residual(work)
        projected = sum(
            float(output_direction[i]) * residual[i]
            for i in range(4)
        )
        total += projected * complex(
            math.cos(-harmonic * phase),
            math.sin(-harmonic * phase),
        )

    return total / phase_samples


def dominant_course_anisotropy(
    net: ThreePlusOneMLP,
    samples: Iterable[Sample],
    *,
    epochs: int,
    amplitude: float = 1e-4,
    phase_samples: int = 12,
) -> TransverseAnisotropyResult:
    """
    Reduce the actual fixed-course nonlinear map onto its dominant linear
    channel and extract the +1 and -2 copy-space Fourier harmonics.
    """
    cumulative = cumulative_transverse_matrix(
        net,
        samples,
        epochs=epochs,
    )
    _, output_direction, input_direction = dominant_singular_pair(cumulative)

    linear = projected_training_harmonic(
        net,
        samples,
        epochs=epochs,
        input_direction=input_direction,
        output_direction=output_direction,
        amplitude=amplitude,
        harmonic=1,
        phase_samples=phase_samples,
    ) / amplitude

    quadratic = projected_training_harmonic(
        net,
        samples,
        epochs=epochs,
        input_direction=input_direction,
        output_direction=output_direction,
        amplitude=amplitude,
        harmonic=-2,
        phase_samples=phase_samples,
    ) / (amplitude * amplitude)

    return TransverseAnisotropyResult(
        epochs=epochs,
        amplitude=float(amplitude),
        input_direction=(
            float(input_direction[0]),
            float(input_direction[1]),
            float(input_direction[2]),
            float(input_direction[3]),
        ),
        output_direction=(
            float(output_direction[0]),
            float(output_direction[1]),
            float(output_direction[2]),
            float(output_direction[3]),
        ),
        linear_gain=linear,
        quadratic_coefficient=quadratic,
    )


def projected_course_phase(
    net: ThreePlusOneMLP,
    samples: Iterable[Sample],
    *,
    epochs: int,
    input_direction: Sequence[float],
    output_direction: Sequence[float],
    amplitude: float,
    phase: float,
) -> float:
    """Projected output phase after a fixed nonlinear training course."""
    data = list(samples)
    work = deepcopy(net)
    add_transverse_vector_seed(
        work,
        direction=input_direction,
        amplitude=amplitude,
        phase=phase,
    )

    for _ in range(epochs):
        for x, target in data:
            work.train_one(x, target)

    residual = transverse_residual(work)
    projected = sum(
        float(output_direction[i]) * residual[i]
        for i in range(4)
    )
    return math.atan2(projected.imag, projected.real)
