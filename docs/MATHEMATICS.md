# Mathematics

This note keeps the core formulas used by the repository in one place and
marks which parts are standard theory versus system-specific derivations.

For literature positioning, see
[\`PRIOR_ART_AND_POSITIONING.md\`](PRIOR_ART_AND_POSITIONING.md).

---

## 1. Permutation symmetry and the standard representation

Let a hidden layer contain \(n\) interchangeable units.

Write the local incoming parameter vector of unit \(i\) as

\[
B_i\in\mathbb R^{d+1},
\]

including bias.

The fully symmetric state is

\[
B_1=B_2=\cdots=B_n.
\]

The natural copy-difference space is the zero-sum subspace

\[
\boxed{
H_{n-1}
=
\left\{
x\in\mathbb R^n:
\sum_i x_i=0
\right\}.
}
\]

This is the standard representation of \(S_n\).

That representation, and equivariant bifurcation theory on it, are established
mathematics. The project uses them as imported structure.

---

## 2. Controlled symmetry seed

For one output unit, let the hidden-to-output weights be

\[
a=(a_1,\dots,a_n).
\]

The package initializes

\[
\boxed{
a^{(0)}
=
a_0\mathbf 1+\varepsilon s.
}
\]

The default singleton seed is

\[
s=(0,\dots,0,1).
\]

The exact symmetric control is

\[
\varepsilon=0.
\]

A centered singleton seed is

\[
s_c
=
s-\frac1n\mathbf1
=
\left(
-\frac1n,\dots,-\frac1n,1-\frac1n
\right),
\]

so

\[
\sum_i s_{c,i}=0.
\]

At a symmetric hidden state with common activation \(h\),

\[
h\sum_i a_i
=
h\left(
na_0+\varepsilon\sum_i s_{c,i}
\right)
=
hna_0.
\]

Therefore the centered seed preserves the initial network function while
breaking hidden-unit permutation symmetry.

For \(n=4\),

\[
s_c=(-0.25,-0.25,-0.25,0.75).
\]

---

## 3. First-step divergence

For sigmoid hidden activation \(h_i\) and output delta
\(\delta^{(o)}\),

\[
\delta_i^{(h)}
=
h_i(1-h_i)\delta^{(o)}a_i.
\]

At the symmetric hidden state,

\[
h_i=h_j=h,
\]

so

\[
\delta_i^{(h)}-\delta_j^{(h)}
=
h(1-h)\delta^{(o)}(a_i-a_j).
\]

With the seed family,

\[
\boxed{
\delta_i^{(h)}-\delta_j^{(h)}
=
h(1-h)\delta^{(o)}
\varepsilon(s_i-s_j).
}
\]

This is the immediate symmetry-breaking mechanism in the package.

It is not claimed as a general novelty; random initialization has long been
used to avoid exact hidden-unit symmetry.

---

## 4. The four centered singleton directions

For \(n=4\), define

\[
v_i
=
\frac{4e_i-\mathbf1}{\sqrt{12}}.
\]

Then

\[
\sum_j (v_i)_j=0,
\]

\[
\|v_i\|=1,
\]

and for \(i\neq j\),

\[
\langle v_i,v_j\rangle=-\frac13.
\]

Thus the four centered singleton directions form a regular tetrahedron inside

\[
H_3\cong\mathbb R^3.
\]

This is a standard-representation geometry, not a separate novelty claim.

Choosing one singleton axis leaves the residual three-copy standard
representation

\[
H_2\cong\mathbb R^2.
\]

See [\`AXIS_GENERATION.md\`](AXIS_GENERATION.md).

---

## 5. Complex coordinate on the residual three-copy space

For the first three units, use the orthonormal copy-space basis

\[
c_R
=
\frac1{\sqrt6}(2,-1,-1),
\]

\[
c_I
=
\frac1{\sqrt2}(0,1,-1).
\]

For local parameter vectors

\[
q_i=(a_i,b_i,w_{i1},w_{i2})\in\mathbb R^4,
\]

define

\[
\boxed{
Z
=
\sum_{i=1}^{3}
(c_{R,i}+ic_{I,i})q_i
\in\mathbb C^4.
}
\]

Then

\[
Z=0
\]

exactly when the three local states coincide.

The copy-space phase of \(Z\) records which direction in the residual
three-copy standard representation is occupied.

---

## 6. First-order transverse dynamics of the actual XNOR update

For one sample define

\[
\hat x=(1,x_1,x_2)^T,
\]

\[
d=(t-y)y(1-y),
\]

\[
g=h(1-h),
\]

\[
g'=g(1-2h).
\]

For one representative member of the three-copy group, write the local state

\[
q=(a,w_0,w_1,w_2)^T.
\]

The exact first-order mean-zero transverse update used in this repository is

\[
\boxed{
\delta q^+
=
K\,\delta q,
}
\]

with

\[
\boxed{
K
=
\begin{pmatrix}
1 & \eta d g\,\hat x^T\\
\eta d g\,\hat x &
I_3+\eta d a g'\,\hat x\hat x^T
\end{pmatrix}.
}
\]

For an ordered epoch,

\[
M_e=K_{e,m}\cdots K_{e,2}K_{e,1},
\]

and

\[
\boxed{
Z_{e+1}
=
M_eZ_e+O(\|Z_e\|^2).
}
\]

This matrix is a system-specific exact linearization of the current sigmoid
XNOR implementation.

See
[\`XNOR_TRANSVERSE_EXTRACTION.md\`](XNOR_TRANSVERSE_EXTRACTION.md).

---

## 7. Finite-time transverse growth

Let

\[
\sigma_1(M_e)\ge\cdots\ge\sigma_4(M_e)
\]

be the singular values of the epoch transverse map.

Define the finite-time top growth rate

\[
\boxed{
\mu_e=\log\sigma_1(M_e).
}
\]

For the centered XNOR trajectory through epoch 728,

\[
\mu_e>0
\]

at every measured epoch.

The accumulated map

\[
C_e=M_eM_{e-1}\cdots M_1
\]

has top singular gain approximately

\[
34.703
\]

at epoch 728.

These are concrete measurements of this model, not universal neural-network
constants.

---

## 8. Quadratic equivariance

Let the residual cyclic action be

\[
Z\mapsto\omega Z,
\qquad
\omega=e^{2\pi i/3}.
\]

A quadratic equivariant output must transform in the same way.

The copy-space weights of the elementary quadratic combinations are

\[
ZZ\mapsto\omega^2 ZZ,
\]

\[
Z\bar Z\mapsto Z\bar Z,
\]

\[
\bar Z\bar Z
\mapsto
\bar\omega^2\bar Z\bar Z
=
\omega\bar Z\bar Z.
\]

Therefore the quadratic transverse term has the form

\[
\boxed{
F(Z)
=
LZ+Q(\bar Z,\bar Z)+O(\|Z\|^3).
}
\]

The existence of this conjugate-square harmonic is established equivariant
theory.

The repository-specific calculation is the direct extraction of its coefficient
from the actual XNOR training map.

---

## 9. Phase reduction in one channel

For a projected scalar complex mode,

\[
z=re^{i\theta},
\]

suppose

\[
z'
=
\lambda z+\nu\bar z^2+O(|z|^3).
\]

Then

\[
z'
=
\lambda r e^{i\theta}
\left[
1+
\frac{\nu}{\lambda}
r e^{-3i\theta}
+
O(r^2)
\right].
\]

For real \(\lambda,\nu\), the small-amplitude phase change is

\[
\boxed{
\Delta\theta
=
-\frac{\nu}{\lambda}
r\sin3\theta
+
O(r^2).
}
\]

In the original hidden-to-output residual channel of the current XNOR run,

\[
\lambda\approx15.15569,
\]

\[
\nu\approx6.65860.
\]

The corresponding phase law agrees with the measured nonlinear training map.

See
[\`XNOR_QUADRATIC_ANISOTROPY.md\`](XNOR_QUADRATIC_ANISOTROPY.md).

---

## 10. Exact symmetry and branch creation

If an equivariant deterministic map satisfies

\[
F(\omega z)=\omega F(z),
\]

then at the exactly symmetric point

\[
F(0)=\omega F(0).
\]

The only transverse vector fixed by a nontrivial \(120^\circ\) rotation is zero,
so

\[
\boxed{
F(0)=0.
}
\]

Thus exact deterministic symmetry does not create a branch from nothing.

A nonzero residual, noise source, non-unique rule, or another symmetry-breaking
degree of freedom is required.

This is standard equivariance, not a project-specific theorem.

---

## 11. Current boundary

The current deterministic XNOR system demonstrates

\[
\boxed{
\text{residual}
\rightarrow
\text{transport}
\rightarrow
\text{amplification}
\rightarrow
\text{threefold directional sorting}.
}
\]

It does not yet supply a general persistence mechanism that forces an
arbitrarily small off-ray residual to complete asymptotic locking before task
updates vanish.

That persistence question is the present open problem.
