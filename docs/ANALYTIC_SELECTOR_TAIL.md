# Analytic reduction of the selector tail

Status: exact local derivation + finite-horizon asymptotic verification.

> **Asymptotic correction (2026-09-23).** The exact quadratic map and exact
> branch-ray phase derivative derived here remain valid.  The provisional
> asymptotic identification \(a_N\asymp1/(N\log N)\) does not.  A longer
> scan shows
> \[
> a_N\sim C/[N(\log N)^{3/2}],
> \]
> consistent with a hidden log-log direction whose slow support margins have
> coefficient \(3/2\).  See
> [`HIDDEN_TAIL_CLOSURE.md`](HIDDEN_TAIL_CLOSURE.md).

This note sharpens SGD_TAIL_SCALING.md.

The late branch selector can now be written in two exact forms:

1. an exact second-order \(S_3\)-equivariant copy-space map on the symmetric three-copy manifold;
2. an exact infinitesimal phase derivative on the already-broken singleton branch ray.

The measured tail remains

\[
\boxed{
a_N
\asymp
\frac{1}{N\log N},
}
\]

but the route to that law is now more explicit.

---

## 1. Copy-space product identity

Use the residual three-copy basis

\[
c_R
=
\frac1{\sqrt6}(2,-1,-1),
\qquad
c_I
=
\frac1{\sqrt2}(0,1,-1).
\]

For a real mean-zero copy perturbation \(u_i\), define

\[
z_u
=
\sum_{i=1}^3
(c_{R,i}+ic_{I,i})u_i.
\]

Similarly define \(z_v\).

Direct substitution gives the exact identity

\[
\boxed{
\sum_{i=1}^3
(c_{R,i}+ic_{I,i})u_iv_i
=
\frac1{\sqrt6}\,
\overline{z_u}\,
\overline{z_v}.
}
\]

For \(u=v\),

\[
\boxed{
P_E(u_i^2)
=
\frac1{\sqrt6}\bar z_u^2.
}
\]

This is the concrete algebraic source of the \(\bar z^2\) harmonic in the current coordinates.

---

## 2. Exact one-sample quadratic map

For one member of the symmetric trio write the local state as

\[
q=(a,w),
\]

where

\[
w=(w_0,w_1,w_2),
\qquad
\hat x=(1,x_1,x_2).
\]

Let the complex transverse perturbation be

\[
z=(z_a,z_w),
\]

and define

\[
s
=
\hat x\cdot z_w.
\]

For the hidden sigmoid activation

\[
h=\sigma(w\cdot\hat x),
\]

write

\[
g=h(1-h),
\]

\[
g'
=
g(1-2h),
\]

\[
g''
=
g(1-6h+6h^2).
\]

The shared output delta is

\[
d=(t-y)y(1-y).
\]

The first-order map is

\[
K
=
\begin{pmatrix}
1 & \eta dg\,\hat x^T\\
\eta dg\,\hat x &
I+\eta dag'\,\hat x\hat x^T
\end{pmatrix}.
\]

At quadratic order, the exact copy-space contribution along one real transverse direction is

\[
\boxed{
Q_a
=
\frac{\eta d}{2\sqrt6}
g' s^2,
}
\]

and

\[
\boxed{
Q_w
=
\frac{\eta d}{\sqrt6}
\left[
g' z_a s
+
\frac12 a g'' s^2
\right]\hat x.
}
\]

Thus

\[
\boxed{
z^+
=
Kz
+
Q(\bar z,\bar z)
+
O(\|z\|^3).
}
\]

The perturbation of the common output delta begins at second order, but its contribution to the transverse projection begins only at third order. Therefore the coarse shared \(d\) above is exact through quadratic order.

---

## 3. Exact epoch composition

For a sequence of samples, let \(\ell\) be the linear response and \(q\) the quadratic response.

For each sample,

\[
\boxed{
q^+
=
Kq
+
Q(\ell,\ell),
}
\]

\[
\boxed{
\ell^+
=
K\ell.
}
\]

This gives an exact second-order epoch map without Fourier fitting.

The implementation is epoch_transverse_quadratic_direction in src/threeplusone/transverse.py.

A unit test compares this analytic coefficient against the nonlinear Fourier extraction and finds agreement to numerical precision.

---

## 4. Exact phase derivative on a broken singleton branch

The previous selector measurement used two finite rotations \(\pm\delta\). That approximation can now be removed.

On the phase-0 branch, one member of the trio is singled out and the other two remain exactly equal.

Let

\[
R_N\in\mathbb R^4
\]

be the real copy-space residual vector at epoch \(N\).

An infinitesimal copy-space rotation produces

\[
\frac{dZ_N}{d\theta}
=
iR_N.
\]

At phase zero, this is exactly an antisymmetric split of the equal pair.

Let

\[
M_{\mathrm{pair},N}
\]

be the exact one-epoch tangent map of that antisymmetric pair mode, evaluated on the actual broken branch state.

Let

\[
R_{N+1}
\]

be the ordinary nonlinear branch residual after one epoch.

Then the outgoing infinitesimal phase derivative is exactly

\[
\boxed{
\rho_N
=
\frac{
\langle
R_{N+1},
M_{\mathrm{pair},N}R_N
\rangle
}{
\|R_{N+1}\|^2
}.
}
\]

Therefore the exact local selector action is

\[
\boxed{
a_N
=
-\frac13\log|\rho_N|.
}
\]

No small-radius approximation appears in this formula.

The implementation is branch_ray_phase_derivative, and a unit test verifies agreement with the finite-rotation diagnostic.

---

## 5. Exact branch action still has the same tail

The exact branch-tangent action gives:

| \(N\) | exact \(a_N\) | \(N\log N\,a_N\) |
|---:|---:|---:|
| 10,000 | \(1.34452\times10^{-6}\) | 0.123835 |
| 20,000 | \(6.01609\times10^{-7}\) | 0.119161 |
| 50,000 | \(2.15808\times10^{-7}\) | 0.116750 |
| 100,000 | \(1.00764\times10^{-7}\) | 0.116009 |
| 200,000 | \(4.73263\times10^{-8}\) | 0.115534 |
| 500,000 | \(1.75059\times10^{-8}\) | 0.114859 |
| 1,000,000 | \(8.26287\times10^{-9}\) | 0.114156 |

Hence the finite-difference result was not an artifact.

The exact tangent quantity itself satisfies

\[
\boxed{
a_N
=
\Theta((N\log N)^{-1})
}
\]

over the measured tail.

---

## 6. Where the extra \(1/\log N\) comes from

The task-scale factor is

\[
|d_N|
=
\Theta(N^{-1}).
\]

The hidden sigmoid derivative supplies the additional slow factor.

Measured on the corresponding coarse three-copy state:

| \(N\) | \(N\overline{|d|}\) | \((\log N)\bar g\) | \((\log N)\overline{|g'|}\) |
|---:|---:|---:|---:|
| 10,000 | 1.39968 | 1.08346 | 0.68211 |
| 100,000 | 1.18978 | 1.11059 | 0.78339 |
| 1,000,000 | 1.11028 | 1.11636 | 0.84689 |

Thus

\[
\boxed{
d_N
=
\Theta(N^{-1}),
}
\]

while

\[
\boxed{
g_N,\ |g'_N|
=
\Theta((\log N)^{-1})
}
\]

over the measured tail.

The two explicitly positive \(g'\)-sector quadratic terms are therefore naturally of size

\[
\boxed{
d_N g'_N
=
\Theta((N\log N)^{-1}).
}
\]

This is the local analytic origin of the selector tail.

---

## 7. Source decomposition of the quadratic selector

Project the exact epoch quadratic map onto the outgoing linear response.

The quadratic coefficient separates into

\[
\nu_N
=
\nu_N^{\mathrm{out}}
+
\nu_N^{\mathrm{cross}}
+
\nu_N^{\mathrm{curv}},
\]

where

\[
\nu^{\mathrm{out}}
\leftrightarrow
\frac12 d g' s^2,
\]

\[
\nu^{\mathrm{cross}}
\leftrightarrow
d g' z_a s,
\]

and

\[
\nu^{\mathrm{curv}}
\leftrightarrow
\frac12 d a g'' s^2.
\]

At \(N=10^6\),

\[
\nu^{\mathrm{out}}
\approx
9.96\times10^{-10},
\]

\[
\nu^{\mathrm{cross}}
\approx
1.99\times10^{-9},
\]

\[
\nu^{\mathrm{curv}}
\approx
-3.12\times10^{-10},
\]

so

\[
\boxed{
\nu_N
\approx
2.67\times10^{-9}>0.
}
\]

The two \(g'\)-sector terms dominate the late positive selector. The curvature term is smaller and changes sign in the measured window.

This decomposition explains why a naive dimensional estimate of the \(a g''\) term alone is misleading: the epoch geometry and XNOR sample balance matter.

---

## 8. Quadratic prediction versus exact broken-branch action

The quadratic coarse-state approximation predicts

\[
a_N^{(2)}
\approx
\frac{\nu_N}{\lambda_N}r_N.
\]

The exact broken-branch tangent action is smaller because the actual branch radius is finite and higher-order terms contribute.

At the measured checkpoints,

\[
\frac{a_N^{(2)}}{a_N^{\mathrm{exact}}}
\approx
1.28\text{--}1.29.
\]

The ratio is nearly constant across two decades.

Thus the quadratic map is not an exact finite-radius amplitude formula, but it does capture the same asymptotic selector class.

---

## 9. A conditional divergence proposition

The exact formulas isolate the remaining proof obligation.

Suppose that along the phase-0 branch there exist positive constants and a sufficiently large \(N_0\) such that for all \(N\ge N_0\),

\[
|d_N|
\ge
\frac{c_d}{N},
\]

\[
|g'_N|
\ge
\frac{c_g}{\log N},
\]

the normalized branch geometry remains nondegenerate, and the total projected quadratic / higher-order correction does not cancel the positive \(g'\)-sector contribution beyond a fixed fraction.

Then there is a constant \(c>0\) such that

\[
\boxed{
a_N
\ge
\frac{c}{N\log N}.
}
\]

Therefore

\[
\sum_{N=N_0}^{\infty}a_N
=
\infty,
\]

and hence

\[
\boxed{
\mathcal A_\infty
=
\infty.
}
\]

So the asymptotic locking problem has now been reduced to proving tail bounds for ordinary sigmoid-SGD quantities and one non-cancellation condition.

No additional persistence force is required by the mathematics if those bounds hold.

---

## 10. What remains unproved

Three empirical tail statements still need analytic control:

\[
N|d_N|
\to
D>0,
\]

\[
(\log N)|g'_N|
\to
G>0
\quad\text{or at least stays bounded below},
\]

and

\[
N\log N\,a_N
\to
C>0
\quad\text{or at least stays bounded below}.
\]

The first is strongly tied to the exact binary-sigmoid identity

\[
|d|
=
\epsilon^2(1-\epsilon)
\]

and the observed margin law

\[
m_N
\sim
\frac12\log N.
\]

The second is tied to the hidden-weight tail.

The third now has an exact branch-tangent formula rather than a finite-angle proxy.

The remaining proof problem is therefore much narrower than before.

---

## 11. Current chain

The selector mechanism can now be written as

\[
\boxed{
\text{output margin}
\sim
\frac12\log N
}
\]

\[
\Downarrow
\]

\[
\boxed{
d_N
\sim
N^{-1}
}
\]

while hidden saturation gives

\[
\boxed{
g'_N
\sim
(\log N)^{-1}
}
\]

and the exact copy-space quadratic map gives

\[
\boxed{
Q_N
\sim
d_Ng'_N
\sim
\frac1{N\log N}.
}
\]

The exact broken-branch tangent then measures

\[
\boxed{
a_N
\sim
\frac1{N\log N},
}
\]

so

\[
\boxed{
\mathcal A_N
\sim
\log\log N.
}
\]

This is now the cleanest current account of why the selector keeps acting after ordinary task convergence.

---

## 12. Reproduction

Run

~~~bash
python examples/xnor_analytic_selector_tail.py
~~~

The exact quadratic and branch-tangent implementations are in src/threeplusone/transverse.py as

~~~text
sample_transverse_quadratic_direction
epoch_transverse_quadratic_direction
branch_ray_phase_derivative
~~~

The full unit-test suite currently contains 32 passing tests.
