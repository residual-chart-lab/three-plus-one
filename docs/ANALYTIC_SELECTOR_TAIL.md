# Analytic reduction of the selector tail

Status: exact local derivation + finite-horizon asymptotic verification.

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

## 6. Hidden-tail correction

A later tail reduction shows that the provisional estimate

\[
|g'_N|
=
\Theta((\log N)^{-1})
\]

is not the correct factorization.

The relevant output-weight scale and retained branch radius obey

\[
A_N
=
\Theta((\log N)^{2/3}),
\]

\[
R_N
=
\Theta((\log N)^{2/3})
\]

over the deterministic tail through \(10^7\) epochs.

Together with

\[
|d_N|
=
\Theta(N^{-1}),
\]

this gives the effective hidden clock

\[
\tau_N
\asymp
\sum_{n\le N}
\frac{(\log n)^{2/3}}{n}
=
\Theta((\log N)^{5/3}).
\]

The three active hidden support margins satisfy

\[
u_{01},
u_{10},
-u_{11}
=
\log\tau_N+O(1)
=
\frac53\log\log N+O(1).
\]

Therefore

\[
\boxed{
|g'_N|
=
\Theta((\log N)^{-5/3})
}
\]

on the active support directions.

The selector still has the observed \(1/(N\log N)\) tail because the broken
branch radius multiplies the local hidden sensitivity:

\[
R_N|d_N||g'_N|
\asymp
(\log N)^{2/3}
\frac1N
(\log N)^{-5/3}
=
\boxed{
\frac1{N\log N}
}.
\]

See
[`HIDDEN_TAIL_CLOSURE.md`](HIDDEN_TAIL_CLOSURE.md)
for the derivation and the \(10^7\)-epoch check.

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

## 9. A corrected conditional divergence proposition

The exact formulas now isolate the proof obligation more sharply.

Suppose that for all sufficiently large \(N\):

\[
|d_N|
\ge
\frac{c_d}{N},
\]

\[
R_N
\ge
c_R(\log N)^{2/3},
\]

\[
|g'_N|
\ge
c_g(\log N)^{-5/3},
\]

the branch geometry remains nondegenerate, and the projected higher-order
terms do not cancel the stable selector beyond a fixed fraction.

Then

\[
\boxed{
a_N
\ge
\frac{c}{N\log N}.
}
\]

Hence

\[
\sum_N a_N
=
\infty
\]

and

\[
\boxed{
\mathcal A_\infty
=
\infty.
}
\]

The important change is that non-summability no longer rests on
\(g'_N\sim1/\log N\) by itself.

It rests on the compensated product

\[
\boxed{
R_N g'_N
\asymp
(\log N)^{2/3-5/3}
=
(\log N)^{-1}.
}
\]

---

## 10. What remains unproved

The exact selector action is now verified through \(10^7\) epochs, with

\[
N\log N\,a_N
:
0.11416
\rightarrow
0.11019.
\]

The strongest remaining upstream gap is the \(2/3\) law itself:

\[
A_N
\asymp
(\log N)^{2/3},
\qquad
R_N
\asymp
(\log N)^{2/3}.
\]

Given that law and the ordinary

\[
d_N\asymp N^{-1}
\]

tail, the effective-clock reduction yields the \(5/3\) hidden-margin and
hidden-sensitivity exponents.

A full theorem would still require rigorous control of those \(2/3\) scales
and the higher-order remainder in the exact branch-tangent map.

---

## 11. Current chain

The corrected mechanism is

\[
\boxed{
A_N,\ R_N
\sim
(\log N)^{2/3}
}
\]

together with

\[
\boxed{
d_N
\sim
N^{-1}.
}
\]

Therefore the effective hidden clock is

\[
\boxed{
\tau_N
\sim
(\log N)^{5/3}.
}
\]

The active hidden margins obey

\[
\boxed{
\gamma_N
\sim
\frac53\log\log N
}
\]

and hence

\[
\boxed{
|g'_N|
\sim
(\log N)^{-5/3}.
}
\]

Finally,

\[
\boxed{
R_N d_N g'_N
\sim
\frac1{N\log N},
}
\]

so the exact branch action remains

\[
\boxed{
a_N
\sim
\frac1{N\log N}
}
\]

and the cumulative action remains non-summable.

The \(1/\log N\) factor is therefore an exponent cancellation in the full
history-bearing branch geometry, not the decay law of \(g'_N\) alone.

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
