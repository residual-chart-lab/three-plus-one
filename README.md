# three-plus-one
## Controlled symmetry breaking in a tiny neural network

`three-plus-one` is a small research laboratory for one concrete question:

> What exactly happens to a symmetric hidden population when one controlled
> difference is retained, transported, amplified, and nonlinearly sorted?

The project began from a 3+1 asymmetry observed while reconstructing a small
1996 AMOS neural-network example. It now separates three things that are easy
to mix together:

1. **established symmetry theory** that should be imported rather than
   rediscovered,
2. **exact measurements of one deterministic sigmoid-XNOR network**,
3. **exploratory geometric models** that go beyond what has been derived from
   SGD.

The current package version is **0.5.0**.

---

## 1. What is not new

Several central ingredients have established literature.

Neural-network initialization has long used asymmetry to prevent hidden units
from remaining exact copies. Hidden-unit permutation symmetry and its breaking
have been studied for decades. The zero-sum difference space is the standard
representation of the symmetric group, and equivariant bifurcation theory
already contains the quadratic structures relevant to the residual
threefold symmetry.

In particular, this project does **not** claim novelty for:

- random initialization as symmetry breaking,
- hidden-unit permutation symmetry or specialization,
- the standard representation
  \[
  H_{n-1}=\{x\in\mathbb R^n:\sum_i x_i=0\},
  \]
- symmetry-adapted Hessian / curvature decompositions,
- the existence of quadratic equivariants,
- the \(C_3\) conjugate-square form \(\bar z^2\),
- the fact that an exactly equivariant deterministic map cannot select a
  branch from an exactly symmetric fixed state.

See [`docs/PRIOR_ART_AND_POSITIONING.md`](docs/PRIOR_ART_AND_POSITIONING.md)
for the literature map and claim boundary.

---

## 2. The controlled 3+1 experiment

All hidden units begin with identical incoming weights,

\[
B_i^{(0)}=b_0.
\]

The hidden-to-output weights are

\[
a^{(0)}
=
a_0\mathbf 1+\varepsilon s.
\]

The default four-unit seed is

\[
s=(0,0,0,1).
\]

The exact symmetric control is

\[
\varepsilon=0.
\]

A cleaner centered control subtracts the seed mean:

\[
s_c
=
\left(
-\frac14,-\frac14,-\frac14,\frac34
\right).
\]

Because

\[
\sum_i s_{c,i}=0,
\]

the centered seed preserves the initial network output while still breaking
the hidden-unit permutation symmetry.

Run the basic controls:

~~~bash
python -m pip install -e .

three-plus-one demo --epsilon 0
three-plus-one demo --epsilon 1
three-plus-one demo --epsilon 1 --centered
~~~

For the deterministic XNOR setup, the symmetric control does not reach the
default target MSE within the same budget, while the 3+1 and centered-3+1 runs
do.

This is a controlled example, not a universal claim that a 3+1 seed is
generally optimal.

---

## 3. Standard-representation geometry

For four interchangeable units, the centered contrast space is

\[
V
=
\left\{
x\in\mathbb R^4:
\sum_i x_i=0
\right\}
\cong\mathbb R^3.
\]

The four normalized singleton contrasts are

\[
v_i
=
\frac{4e_i-\mathbf1}{\sqrt{12}}.
\]

They satisfy

\[
\|v_i\|=1,
\qquad
\langle v_i,v_j\rangle=-\frac13
\quad(i\neq j),
\]

so they form a regular tetrahedron.

This tetrahedral geometry is an elementary realization of the
\(S_4\) standard representation. It is not presented as a new mathematical
object.

Choosing one singleton direction creates a distinguished axis. The residual
three-copy sector is the orthogonal two-dimensional plane carrying the
standard representation of \(S_3\).

See [`docs/AXIS_GENERATION.md`](docs/AXIS_GENERATION.md).

---

## 4. The actual hidden residual in XNOR

For the first three hidden units, collect local parameter states

\[
q_i=(a_i,b_i,w_{i1},w_{i2})\in\mathbb R^4.
\]

Using an orthonormal basis of the mean-zero three-copy space,

\[
c_R=\frac1{\sqrt6}(2,-1,-1),
\qquad
c_I=\frac1{\sqrt2}(0,1,-1),
\]

define

\[
\boxed{
Z
=
\sum_{i=1}^3
(c_{R,i}+ic_{I,i})q_i
\in\mathbb C^4.
}
\]

Then

\[
Z=0
\]

exactly when those three local states coincide.

A mean-zero transverse residual is invisible to the network output at first
order, but it has its own tangent dynamics.

For one ordered XNOR epoch,

\[
\boxed{
Z_{e+1}
=
M_eZ_e+O(\|Z_e\|^2).
}
\]

\(M_e\) is derived from the existing SGD update; no auxiliary memory variable or
modified optimizer is introduced.

See
[`docs/XNOR_TRANSVERSE_EXTRACTION.md`](docs/XNOR_TRANSVERSE_EXTRACTION.md).

---

## 5. Measured transverse growth

Along the centered deterministic XNOR trajectory through ordinary convergence
at epoch 728,

\[
\sigma_1(M_e)>1
\]

at every measured epoch.

The number of instantaneously expanding channel directions follows

\[
2\rightarrow3\rightarrow2\rightarrow1
\]

over epochs

- 1–8,
- 9–131,
- 132–558,
- 559–728.

At epoch 728, the accumulated transverse singular values are approximately

\[
(34.7030,\;24.1998,\;0.3200,\;7.18\times10^{-8}).
\]

A direct \(10^{-6}\) mean-zero hidden-to-output residual is amplified by about

\[
15.156\times
\]

under the unmodified training rule by epoch 728.

So the exact symmetric manifold is invariant,

\[
Z=0\Rightarrow Z'=0,
\]

while nearby nonzero histories are transversely amplified.

Run:

~~~bash
python examples/xnor_transverse_scan.py
~~~

---

## 6. The actual nonlinear threefold term

Residual threefold symmetry acts by

\[
Z\mapsto\omega Z,
\qquad
\omega=e^{2\pi i/3}.
\]

At quadratic order, equivariance forces the copy-space structure

\[
\boxed{
F(Z)
=
LZ+Q(\bar Z,\bar Z)+O(\|Z\|^3).
}
\]

The abstract existence of this conjugate-square harmonic is established
equivariant theory. The repository-specific step is to extract its coefficient
from the actual nonlinear XNOR training map.

For the original hidden-to-output residual channel, a phase-Fourier
decomposition of the 728-epoch course gives approximately

\[
\lambda_{\rm out}\approx15.15569,
\qquad
\nu_{\rm out}\approx6.65860.
\]

The induced small-amplitude phase shift is

\[
\boxed{
\Delta\theta
=
-\frac{\nu}{\lambda}r\sin3\theta
+
O(r^2).
}
\]

For

\[
r=0.01,
\qquad
\theta=\frac{\pi}{6},
\]

the quadratic reduction predicts

\[
\theta_{\rm pred}\approx0.5192053,
\]

while the full nonlinear network gives

\[
\theta_{\rm actual}\approx0.5192082.
\]

The full map also shows angular attraction toward the three oriented singleton
rays

\[
0,\qquad
+\frac{2\pi}{3},\qquad
-\frac{2\pi}{3}.
\]

See
[`docs/XNOR_QUADRATIC_ANISOTROPY.md`](docs/XNOR_QUADRATIC_ANISOTROPY.md).

Run:

~~~bash
python examples/xnor_quadratic_anisotropy.py
~~~

---

## 7. What remains open

The current XNOR system now supplies:

\[
\boxed{
\text{nonzero residual}
\rightarrow
\text{transport}
\rightarrow
\text{amplification}
\rightarrow
\text{threefold directional sorting}.
}
\]

But two boundaries remain explicit.

First, exact deterministic symmetry still cannot create a branch from
nothing:

\[
Z_0=0
\Rightarrow
Z_e=0.
\]

Second, a direct persistence scan shows that ordinary task convergence does
**not** immediately terminate branch sorting.  For a finite off-ray residual,
the branch-ray phase contraction continues to accumulate through at least
100,000 epochs while the residual itself remains present.

The sharp question is therefore no longer simply whether the drive survives.
It is whether cumulative selector action is summable:

\[
\boxed{
\mathcal A_\infty<\infty
\quad\text{or}\quad
\mathcal A_\infty=\infty.
}
\]

If the action diverges, the existing XNOR dynamics can in principle produce
asymptotic branch locking even though the instantaneous updates tend to zero.

See
[`docs/SELECTOR_PERSISTENCE.md`](docs/SELECTOR_PERSISTENCE.md).

---

## 8. Exploratory geometric layer

The repository also contains a dual-tetrahedral rotor model derived from
earlier Spark Engine geometry.

That model studies:

- oriented area / parity,
- relative frame motion,
- persistent rotation,
- recursive axis generation.

It is intentionally separated from the empirical XNOR layer.

Nothing in the current repository establishes that standard SGD literally
implements the dual-tetrahedral rotor.

See
[`docs/DUAL_TETRAHEDRAL_DYNAMICS.md`](docs/DUAL_TETRAHEDRAL_DYNAMICS.md).

---

## 9. Documentation map

Start here:

- [`PRIOR_ART_AND_POSITIONING.md`](docs/PRIOR_ART_AND_POSITIONING.md) —
  established theory vs repository-specific claims
- [`MATHEMATICS.md`](docs/MATHEMATICS.md) —
  symmetry decomposition and controlled seed
- [`EXPERIMENTS.md`](docs/EXPERIMENTS.md) —
  reproducible controls
- [`AXIS_GENERATION.md`](docs/AXIS_GENERATION.md) —
  tetrahedral contrast geometry
- [`XNOR_TRANSVERSE_EXTRACTION.md`](docs/XNOR_TRANSVERSE_EXTRACTION.md) —
  exact hidden residual and tangent dynamics
- [`XNOR_QUADRATIC_ANISOTROPY.md`](docs/XNOR_QUADRATIC_ANISOTROPY.md) —
  nonlinear phase harmonic
- [`NEXT_ONE_SELECTION.md`](docs/NEXT_ONE_SELECTION.md) —
  reduced branch-selection model and its corrections
- [`DUAL_TETRAHEDRAL_DYNAMICS.md`](docs/DUAL_TETRAHEDRAL_DYNAMICS.md) —
  separate exploratory geometry
- [`SCALING_HYPOTHESIS.md`](docs/SCALING_HYPOTHESIS.md) —
  unverified scaling questions
- [`FUTURE_ADMISSIBILITY_HANDOFF.md`](docs/FUTURE_ADMISSIBILITY_HANDOFF.md) —
  handoff from symmetry-constrained future operations to retained differences and the persistence gap
- [`SELECTOR_PERSISTENCE.md`](docs/SELECTOR_PERSISTENCE.md) —
  direct test of residual survival and cumulative branch-selector action after task convergence
- [`PROVENANCE.md`](docs/PROVENANCE.md) —
  historical source separation

---

## 10. Historical provenance

The project was inspired by study of a 1996 AMOS neural-network program by
Lee Atkins recovered from Aminet.

The original source is not included or relicensed here.

`three-plus-one` is a new implementation using conventional backpropagation
and a controlled seed family

\[
a^{(0)}
=
a_0\mathbf1+\varepsilon s.
\]

See [`docs/PROVENANCE.md`](docs/PROVENANCE.md).

---

## License

The new implementation and documentation in this repository are released
under the MIT License.

That license does not apply to the historical 1996 source.
