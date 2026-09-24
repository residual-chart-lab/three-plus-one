# Future phase observability requires all four tangent channels

2026-09-24. Base: `a88922c79941a4a4be1e69d1b53be3ea21c57748`.

**Result.** At the prescribed XNOR checkpoints 728, 10,000 and 100,000,
current-through-three-epoch phase readouts have exact rank four in the
four-dimensional antisymmetric equal-pair tangent sector. The rank sequence
as the horizon increases is **1, 2, 3, 4** at every tested checkpoint.
Outward-rounded interval minors exclude zero. Thus all three currently
invisible directions become distinguishable within three further epochs.

This also corrects an inference in the earlier tail notes: the product of
local scalar phase derivatives does not equal the cumulative phase derivative.
The local one-epoch derivative remains valid.

## 1. Fixed trajectory and readout

Use the existing deterministic ordered XNOR SGD with learning rate 1,
`centered_singleton_seed(4)`, and a phase-zero output-channel transverse seed
of amplitude 0.1. On this branch, copy units 1 and 2 (zero-based) are equal.
Write their local four-channel states as

$$
q_i=(a_i,b_i,w_{i1},w_{i2}),\qquad
R_n=\sqrt{2/3}\,(q_0-q_1).
$$

An imaginary transverse perturbation splits the equal pair with opposite
signs. Its tangent space is $T_n=\mathbb R^4$. It is invariant under the
linearized update by the pair-exchange symmetry. The pure phase tangent
$v_n=R_n$ spans only one line in this space.

Let $J_n:T_n\to T_{n+1}$ be the exact one-epoch tangent of the smooth SGD
map in this sector, and define the phase readout

$$
\ell_n=\frac{R_n^T}{\|R_n\|^2},\qquad \ell_n v_n=1.
$$

All subsequent readouts use the actual continued branch residual. This fixes
the projector convention; a coarse linear reference projector defines a
different phase diagnostic. The base trajectory is supplied externally here.
The four-dimensional claim concerns this tangent sector, not the complete
network state.

## 2. The dropped component returns

Define

$$
\rho_n=\ell_{n+1}J_nv_n,\qquad
h_{n+1}=J_nv_n-\rho_n v_{n+1}.
$$

Then, exactly,

$$
\ell_{n+1}h_{n+1}=0,
$$

but

$$
\ell_{n+2}J_{n+1}J_nv_n
=\rho_{n+1}\rho_n+\ell_{n+2}J_{n+1}h_{n+1}.
$$

At checkpoint 728 the two-epoch values are:

| Quantity | Value |
|---|---:|
| Full propagated phase derivative | 0.998989829102497239 |
| Product of local phase derivatives | 0.998986959696540323 |
| Returned hidden contribution | 0.000002869405956915665 |

The last row equals the difference of the first two. In particular, the pure
phase line is not invariant under this tangent dynamics. A finite phase
rotation followed by two epochs independently checks the full derivative in
the regression test. The scalar product omits this response.

## 3. Future-observable quotient

For a fixed horizon $k$, set

$$
\mathcal O_n^{(k)}=
\begin{pmatrix}
\ell_n\\
\ell_{n+1}J_n\\
\ell_{n+2}J_{n+1}J_n\\
\vdots\\
\ell_{n+k}J_{n+k-1}\cdots J_n
\end{pmatrix},\qquad
K_n^{(k)}=\ker\mathcal O_n^{(k)}.
$$

The minimal linear retained state supporting all these readouts is

$$
T_n/K_n^{(k)},\qquad
\dim(T_n/K_n^{(k)})=\operatorname{rank}\mathcal O_n^{(k)}.
$$

Indeed, every linear encoding $q$ from which these readouts can be recovered
must satisfy $\ker q\subseteq K_n^{(k)}$. The quotient map attains equality
and the stated dimension. This is the ordinary observability construction,
and the same kernel-intersection construction used for minimal retention in
Free Numbers. Here the future operation family is supplied concretely by
actual SGD and its phase readouts.

Since the present readout is included, $K_n^{(k)}\subseteq\ker\ell_n$.
The currently invisible but future-visible quotient is consequently

$$
\mathcal H_n^{(k)}=\ker\ell_n/K_n^{(k)},\qquad
\dim\mathcal H_n^{(k)}=\operatorname{rank}\mathcal O_n^{(k)}-1.
$$

The time-varying update has the horizon-shift compatibility

$$
J_nK_n^{(k+1)}\subseteq K_{n+1}^{(k)}.
$$

A fixed finite horizon alone does not ensure that the same-horizon quotients
carry a closed update. For all future readouts, $K_n^{(\infty)}$ does satisfy
$J_nK_n^{(\infty)}\subseteq K_{n+1}^{(\infty)}$.

## 4. Certified dimensions

| Checkpoint | $k=0$ | $k=1$ | $k=2$ | $k=3$ | $\dim\mathcal H_n^{(3)}$ |
|---:|---:|---:|---:|---:|---:|
| 728 | 1 | 2 | 3 | 4 | 3 |
| 10,000 | 1 | 2 | 3 | 4 | 3 |
| 100,000 | 1 | 2 | 3 | 4 | 3 |

At each horizon a square minor of size $k+1$ is nonzero. The row count gives
the matching upper bound. In particular:

| Checkpoint | $\det\mathcal O_n^{(3)}$ | Smallest singular value, approximately |
|---:|---:|---:|
| 728 | $3.9515957962\times10^{-16}$ | $6.0164180\times10^{-9}$ |
| 10,000 | $3.1357898194\times10^{-29}$ | $8.1958359\times10^{-15}$ |
| 100,000 | $8.2457614995\times10^{-37}$ | $1.8165813\times10^{-18}$ |

The singular values describe conditioning; the interval minors establish
rank. At 100,000 a usual binary64 rank threshold can lose the fourth direction.
Exact retention and a tolerance-based approximation are different questions.

Here $K_n^{(3)}=0$, so $K_n^{(\infty)}=0$ at these starting states as well.
This follows from inclusion, without assuming that a finite plateau persists.
Thus phase plus one or two extra scalars cannot be an exact linear sufficient
state for arbitrary tangent perturbations at these checkpoints. All four
channels are required. Three checkpoints on this trajectory do not prove
this at every epoch or for other initializations.

## 5. Arithmetic and reproduction

Run from the repository root:

```bash
python -m pip install mpmath==1.4.1
PYTHONPATH=src python examples/xnor_future_observability.py --output results/xnor_future_observability.json
PYTHONPATH=src python -m unittest discover -s tests
```

`mpmath` is an optional diagnostic dependency; the package remains
standard-library-only. The diagnostic:

1. Generates the three checkpoints using the existing binary64 training code.
2. Treats each stored binary checkpoint value as an exact binary rational and
   continues the smooth real SGD map for three epochs.
3. Locates nonzero minors at 80 decimal digits and recomputes at 120 digits.
4. Encloses the same calculation with 100-digit outward-rounded interval
   arithmetic and verifies that each selected minor excludes zero.
5. Cross-checks the independent first-epoch tangent and local derivative
   against the existing package implementation.

The certificate concerns the smooth real map from these frozen checkpoints.
It does not enclose the whole exact-real training orbit from initialization,
and does not differentiate the discontinuous floating-point rounding map.
The JSON records checkpoint values as hexadecimal floats, exact binary
interval endpoints, selected minor columns, singular values, source hashes,
and the two-epoch decomposition. Approximate decimal interval endpoints may
print identically; their distinct exact bounds are retained in the JSON.

## 6. Consequence for branch locking

The next asymptotic quantity is

$$
\Gamma_{N,n}=\ell_NJ_{N-1}\cdots J_n v_n.
$$

Divergence of the local sum $\sum_n(-\log|\rho_n|)/3$ alone does not prove
$\Gamma_{N,n}\to0$: the discarded components can return. The proposed
$2/3$--$5/3$ balance remains a candidate description of local coefficients.
Its application to locking needs estimates for the coupled four-channel
cocycle. Nonlinear locking additionally needs control of finite perturbations
and remainders.

The practical bridge to Free Numbers is precise: a presently invisible
kernel direction has a nonzero allowed future response, and the intersection
of future kernels determines what must be retained. This experiment instantiates
that retention question in SGD and answers it for the specified tangent
sector and checkpoints.
