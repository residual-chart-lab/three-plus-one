# Prior art and project positioning

Status: literature map and claim boundary.

This project began from a historical 3+1 asymmetry observed in a small 1996
neural-network program.  The subsequent derivations rediscovered several
structures that already have established mathematical and neural-network
literatures.

This note separates those imported structures from the narrower results that
are specific to this repository.

---

## 1. What is already established

### 1.1 Random initialization as symmetry breaking

Random initialization has long been used to prevent hidden units from
remaining exact copies under gradient-based training.

A useful modern control is Blumenfeld, Gilboa & Soudry (ICML 2020),
*Beyond Signal Propagation: Is Feature Diversity Necessary in Deep Neural
Network Initialization?*

They show that broad random feature diversity is not necessary for successful
training, while some symmetry-breaking mechanism remains essential.  In their
construction, even nondeterministic GPU operations can provide sufficient
symmetry breaking.

Reference:

- https://proceedings.mlr.press/v119/blumenfeld20a.html

For this repository the consequence is:

> randomness itself is not the object of study; controlled nonzero transverse
> asymmetry is.

---

### 1.2 Hidden-unit permutation symmetry and specialization

Permutation symmetry among hidden units, and phases in which that symmetry is
broken, are much older than this project.

Barkai, Hansel & Sompolinsky (1992), *Broken symmetries in multilayered
perceptrons*, explicitly study global permutation symmetry among hidden units
and order parameters that signal its spontaneous breaking.

Reference:

- https://doi.org/10.1103/PhysRevA.45.4146

Related early committee-machine work also studies asymmetric hidden-unit
phases and specialization.

Therefore this project does not claim novelty for the statement

$$
\text{equivalent hidden units}
\rightarrow
\text{symmetry breaking / specialization}.
$$

---

### 1.3 The zero-sum difference space is the standard representation

For \(n\) interchangeable objects, the zero-sum subspace

$$
H_{n-1}
=
\left\{
x\in\mathbb R^n:
\sum_i x_i=0
\right\}
$$

is the standard representation of the symmetric group \(S_n\).

Arjevani & Field use exactly this representation in the analysis of
symmetry-breaking dynamics motivated by shallow neural networks.

Reference:

- Y. Arjevani and M. Field,
  *Equivariant bifurcation, quadratic equivariants, and symmetry breaking for
  the standard representation of \(S_n\)*,
  https://arxiv.org/abs/2107.02422

Thus the centered 3+1 contrast space used here is not a new representation.

For \(n=4\),

$$
H_3\cong\mathbb R^3.
$$

The four centered singleton contrasts

$$
v_i
=
\frac{4e_i-\mathbf 1}{\sqrt{12}}
$$

form a regular tetrahedron because

$$
\|v_i\|=1,
\qquad
\langle v_i,v_j\rangle=-\frac13
\quad(i\ne j).
$$

That tetrahedral geometry is an elementary consequence of the standard
representation, not a novelty claim.

---

### 1.4 Symmetry-based Hessian decomposition

Arjevani & Field (NeurIPS 2020) analytically characterize Hessian structure in
shallow ReLU models using permutation symmetry and representation theory.

Reference:

- *Analytic Characterization of the Hessian in Shallow ReLU Models:
  A Tale of Symmetry*
- https://proceedings.neurips.cc/paper/2020/hash/3a61ed715ee66c48bacf237fa7bb5289-Abstract.html

Accordingly, decomposing network curvature into symmetry-adapted modes is
established methodology.

The transverse Jacobian calculations in this repository should be read as an
explicit specialization to the deterministic sigmoid XNOR system, not as the
invention of symmetry-adapted curvature analysis.

---

### 1.5 Quadratic equivariants and the conjugate-square term

Equivariant bifurcation theory for the standard representation includes
quadratic equivariants.

For the residual threefold action

$$
z\mapsto\omega z,
\qquad
\omega=e^{2\pi i/3},
$$

a quadratic output transforming as \(z\) must carry the copy-space harmonic

$$
\bar z^2.
$$

Indeed,

$$
\bar z^2
\mapsto
\bar\omega^2\bar z^2
=
\omega\bar z^2.
$$

Therefore the appearance of a term of the form

$$
\nu\bar z^2
$$

is a standard equivariant-bifurcation structure.

This repository does **not** claim that the form itself is new.

The project-specific question is whether its coefficient can be extracted
directly from the actual learning map and whether it quantitatively predicts
the observed phase drift.

---

### 1.6 Exact symmetry cannot break itself under an equivariant deterministic map

If

$$
F(\omega z)=\omega F(z)
$$

and \(z=0\) is fixed by the group action, then

$$
F(0)=\omega F(0),
$$

so the only allowed transverse vector is

$$
F(0)=0.
$$

This is a standard fixed-point consequence of equivariance.

Related modern work discusses the general inability of exactly equivariant
functions to break sample-level symmetry without an additional mechanism.

Reference:

- S.-O. Kaba and S. Ravanbakhsh,
  *Symmetry Breaking and Equivariant Neural Networks*,
  https://arxiv.org/abs/2312.09016

Again, the theorem is not presented here as a novelty claim.

---

## 2. What this repository contributes more specifically

The narrower contribution is to keep the entire chain in one small,
reproducible learning system.

### 2.1 Controlled historical 3+1 intervention

The project isolates a specific historical asymmetry as

$$
a^{(0)}
=
a_0\mathbf 1
+
\varepsilon s,
$$

and supplies:

- exact symmetric control \(\varepsilon=0\),
- default singleton seed,
- centered zero-sum singleton seed,
- arbitrary seed patterns,
- deterministic XNOR reproduction.

The centered seed separates symmetry breaking from a simultaneous initial
output shift.

---

### 2.2 Exact transverse residual of the actual XNOR network

For the first three hidden units, define local states

$$
q_i=(a_i,b_i,w_{i1},w_{i2})\in\mathbb R^4.
$$

Using an orthonormal basis of their mean-zero copy space gives

$$
Z\in\mathbb C^4.
$$

This is an explicit residual extracted from the existing network parameters,
not an auxiliary memory variable added to the optimizer.

---

### 2.3 Exact sample and epoch transverse maps

For the current sigmoid SGD implementation, the one-sample first-order
transverse map is derived explicitly.

Over an epoch,

$$
Z_{e+1}
=
M_eZ_e
+
O(\|Z_e\|^2).
$$

The repository then measures the actual finite-time singular growth of
\(M_e\) along the deterministic XNOR trajectory.

This is a system-specific exact calculation.

---

### 2.4 Measured transverse amplification

For the centered XNOR run through the ordinary convergence point at epoch 728:

- the largest one-epoch transverse singular value is \(>1\) at every measured
  epoch,
- the number of expanding channel directions follows
  \(2\to3\to2\to1\),
- the accumulated top transverse gain is about \(34.7\),
- an actual \(10^{-6}\) mean-zero hidden-to-output residual is amplified by
  about \(15.16\times\) under the unmodified training rule.

These are measurements of this concrete model, not general claims about neural
networks.

---

### 2.5 Direct nonlinear harmonic extraction

The repository performs a phase-Fourier decomposition of the actual nonlinear
728-epoch XNOR map.

In the original hidden-to-output residual channel it measures approximately

$$
\lambda_{\mathrm{out}}\approx15.15569,
$$

$$
\nu_{\mathrm{out}}\approx6.65860.
$$

The extracted coefficient predicts the small-amplitude phase shift

$$
\Delta\theta
=
-\frac{\nu}{\lambda}
r\sin3\theta
+
O(r^2),
$$

and agrees quantitatively with the full nonlinear network run.

The novelty claim, if any, belongs to this explicit extraction-and-verification
pipeline for this controlled model, not to the abstract \(\bar z^2\) normal
form.

---

## 3. Separate model layer: dual tetrahedral dynamics

The repository also contains a dual-tetrahedral rotor construction motivated
by earlier Spark Engine geometry.

That layer is intentionally separated from the established neural-network
symmetry literature.

It is a mathematical model used to study:

- oriented area / parity,
- relative frame motion,
- persistent rotation,
- recursive axis generation.

It should not be presented as a mechanism already derived from standard SGD.

The XNOR transverse calculations are the empirical neural-network layer.
The dual-tetrahedral construction is a separate modeling layer that may or may
not ultimately connect to it.

---

## 4. Current claim boundary

### Imported / established

- random initialization as a symmetry-breaking device,
- hidden-unit permutation symmetry,
- specialization / broken permutation phases,
- the standard representation \(H_{n-1}\),
- symmetry-adapted Hessian / curvature analysis,
- quadratic equivariants,
- the \(C_3\) conjugate-square harmonic,
- the fact that exact deterministic equivariance cannot choose a branch from
  an exactly symmetric state.

### Repository-specific results

- the controlled historical 3+1 / centered-3+1 experiment,
- the exact sigmoid-XNOR transverse residual and Jacobian used here,
- the measured epoch-by-epoch transverse growth sequence,
- direct amplification of a tiny seeded residual in this implementation,
- direct extraction of the nonlinear \(-2\) harmonic from this training map,
- quantitative prediction of its measured phase drift,
- the current dual-tetrahedral exploratory model.

---

## 5. Current research question

After importing the established symmetry theory, the remaining issue is
narrower and cleaner:

> **What dynamical mechanism keeps a retained transverse difference active long
> enough to become a persistent specialized state, rather than merely a
> finite-training deviation?**

That is the next problem.

---

## References

1. E. Barkai, D. Hansel, H. Sompolinsky,
   *Broken symmetries in multilayered perceptrons*,
   Phys. Rev. A 45, 4146 (1992).
   https://doi.org/10.1103/PhysRevA.45.4146

2. Y. Blumenfeld, D. Gilboa, D. Soudry,
   *Beyond Signal Propagation: Is Feature Diversity Necessary in Deep Neural
   Network Initialization?*
   ICML / PMLR 119 (2020).
   https://proceedings.mlr.press/v119/blumenfeld20a.html

3. Y. Arjevani, M. Field,
   *Analytic Characterization of the Hessian in Shallow ReLU Models:
   A Tale of Symmetry*,
   NeurIPS 2020.
   https://proceedings.neurips.cc/paper/2020/hash/3a61ed715ee66c48bacf237fa7bb5289-Abstract.html

4. Y. Arjevani, M. Field,
   *Equivariant bifurcation, quadratic equivariants, and symmetry breaking for
   the standard representation of \(S_n\)*,
   2021.
   https://arxiv.org/abs/2107.02422

5. S.-O. Kaba, S. Ravanbakhsh,
   *Symmetry Breaking and Equivariant Neural Networks*,
   2023.
   https://arxiv.org/abs/2312.09016
