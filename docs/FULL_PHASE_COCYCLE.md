# Full phase cocycle and the memory normal form

Status: direct deterministic evidence plus an exact finite-horizon coordinate
reduction for the four-channel antisymmetric equal-pair tangent sector.

This note continues FUTURE_PHASE_OBSERVABILITY.md.

The central correction is already established there:

\[
\Gamma_{N,n}
=
\ell_NJ_{N-1}\cdots J_n v_n
\]

is the actual cumulative phase derivative, whereas

\[
\prod_{j=n}^{N-1}\rho_j
\]

reprojects onto the instantaneous phase line after every epoch and therefore
drops tangent components that can return later.

The present note asks what happens when those components are kept.

---

## 1. Full cocycle scan

For a phase-zero branch state at epoch \(n\), set

\[
v_n=R_n,
\qquad
\ell_n=\frac{R_n^T}{\|R_n\|^2}.
\]

The full tangent is propagated without intermediate projection:

\[
t_{m+1}=J_mt_m,
\qquad
t_n=v_n,
\]

and

\[
\Gamma_{m,n}=\ell_mt_m.
\]

The same trajectory also records the local scalar product

\[
P_{m,n}
=
\prod_{j=n}^{m-1}\rho_j.
\]

Selected measurements are:

| start \(n\) | horizon | \(\Gamma_{n+h,n}\) | local product \(P_{n+h,n}\) | relative gap |
|---:|---:|---:|---:|---:|
| 728 | 1,000 | 0.9045903343 | 0.8714052376 | 0.0366852 |
| 728 | 10,000 | 0.8414555720 | 0.7911367358 | 0.0597998 |
| 728 | 100,000 | 0.7898265352 | 0.7327085755 | 0.0723171 |
| 728 | 1,000,000 | 0.7490854709 | 0.6881035977 | 0.0814084 |
| 10,000 | 100,000 | 0.9244271879 | 0.9210986947 | 0.00360060 |
| 10,000 | 1,000,000 | 0.8744928599 | 0.8671216230 | 0.00842916 |
| 100,000 | 100,000 | 0.9801101055 | 0.9799004597 | 0.000213900 |
| 100,000 | 1,000,000 | 0.9384220839 | 0.9367272454 | 0.00180605 |

The returned hidden components make the full derivative larger than the local
product in this experiment.

However, the discrepancy becomes much smaller when the starting epoch is
moved deeper into the SGD tail.

At a one-million-epoch horizon,

\[
\frac{\Gamma}{P}-1
\]

is approximately

\[
8.86\times10^{-2}
\]

for start epoch 728,

\[
8.50\times10^{-3}
\]

for start epoch 10,000, and

\[
1.81\times10^{-3}
\]

for start epoch 100,000.

Thus the scalar product is not exact, but the phase line becomes increasingly
close to an invariant asymptotic channel.

This is finite-horizon evidence, not yet a proof that
\(\Gamma_{N,n}\to0\).

---

## 2. Phase-hidden block decomposition

Let

\[
e_n=\frac{R_n}{\|R_n\|}
\]

and let

\[
P_n=I-e_ne_n^T
\]

be the orthogonal projector onto the three-dimensional tangent subspace hidden
from the instantaneous phase axis.

For the one-epoch tangent \(J_n\), define

\[
\alpha_n
=
e_{n+1}^TJ_ne_n,
\]

\[
c_n
=
P_{n+1}J_ne_n,
\]

and

\[
b_n
=
P_nJ_n^Te_{n+1}.
\]

Here

- \(c_n\) is phase-to-hidden leakage,
- \(b_n\) is hidden-to-phase coupling,
- \(\alpha_n\) is the normalized phase-line gain.

The phase readout derivative is

\[
\rho_n
=
\frac{\|R_n\|}{\|R_{n+1}\|}
\alpha_n.
\]

The first omitted two-step memory term is

\[
\ell_{n+2}J_{n+1}h_{n+1},
\]

where

\[
h_{n+1}
=
J_nv_n-\rho_nv_{n+1}.
\]

---

## 3. The memory coupling becomes rapidly weak

The measured coupling strengths are:

| epoch \(n\) | \(1-\rho_n\) | \(\|c_n\|\) | \(\|b_n\|\) | two-step hidden return | return / local defect |
|---:|---:|---:|---:|---:|---:|
| 728 | \(5.0820\times10^{-4}\) | \(1.3150\times10^{-3}\) | \(2.3833\times10^{-3}\) | \(2.8694\times10^{-6}\) | \(5.6462\times10^{-3}\) |
| 10,000 | \(4.0335\times10^{-6}\) | \(4.5570\times10^{-6}\) | \(1.1403\times10^{-5}\) | \(4.3593\times10^{-11}\) | \(1.0808\times10^{-5}\) |
| 100,000 | \(3.0229\times10^{-7}\) | \(2.0140\times10^{-7}\) | \(6.6703\times10^{-7}\) | \(1.1633\times10^{-13}\) | \(3.8481\times10^{-7}\) |
| 1,000,000 | \(2.4789\times10^{-8}\) | \(1.2472\times10^{-8}\) | \(5.0777\times10^{-8}\) | \(4.3613\times10^{-16}\) | \(1.7594\times10^{-8}\) |

So two statements coexist:

\[
\boxed{
\text{all three hidden directions are exactly future-observable}
}
\]

at the certified checkpoints, while

\[
\boxed{
\text{their local coupling back into phase becomes extremely weak in the tail}.
}
\]

Exact retained dimension and asymptotic coupling strength are therefore
different questions.

This distinction is essential.

---

## 4. Exact future-readout coordinates

At a checkpoint where

\[
\operatorname{rank}\mathcal O_n^{(3)}=4,
\]

define

\[
\mathcal O_n
=
\begin{pmatrix}
\ell_n\\
\ell_{n+1}J_n\\
\ell_{n+2}J_{n+1}J_n\\
\ell_{n+3}J_{n+2}J_{n+1}J_n
\end{pmatrix}.
\]

Since \(\mathcal O_n\) is invertible, every tangent state \(x_n\in\mathbb R^4\)
can be represented exactly by the four consecutive phase readouts

\[
\boxed{
z_n
=
\mathcal O_nx_n
=
\begin{pmatrix}
y_n\\
y_{n+1}\\
y_{n+2}\\
y_{n+3}
\end{pmatrix}.
}
\]

Thus the four-dimensional internal tangent state is locally equivalent to a
four-sample temporal state.

This is the ordinary observable canonical construction, applied to the actual
time-varying SGD tangent.

---

## 5. Companion memory form

Let

\[
z_{n+1}
=
C_nz_n.
\]

By construction, the first three coordinates shift exactly:

\[
C_n
=
\begin{pmatrix}
0&1&0&0\\
0&0&1&0\\
0&0&0&1\\
c_{0,n}&c_{1,n}&c_{2,n}&c_{3,n}
\end{pmatrix}.
\]

Therefore every tangent phase sequence satisfies the exact local recurrence

\[
\boxed{
y_{n+4}
=
c_{0,n}y_n
+
c_{1,n}y_{n+1}
+
c_{2,n}y_{n+2}
+
c_{3,n}y_{n+3}.
}
\]

The hidden three-dimensional tangent state has not disappeared.

It has been converted into temporal memory.

This gives an exact meaning, inside the tested tangent system, to the statement
that a component invisible now can reappear in later readouts.

---

## 6. Measured companion coefficients

High-precision calculations from exact-binary training checkpoints give:

| epoch | \(c_0\) | \(c_1\) | \(c_2\) | \(c_3\) |
|---:|---:|---:|---:|---:|
| 728 | -0.9450050860 | 3.8343085689 | -5.8335999498 | 3.9442964668 |
| 10,000 | -0.9987627867 | 3.9962880164 | -5.9962876728 | 3.9987624431 |
| 100,000 | -0.9998902261 | 3.9996706755 | -5.9996706729 | 3.9998902234 |
| 1,000,000 | -0.9999895419 | 3.9999686258 | -5.9999686258 | 3.9999895419 |

The shift rows agree with the exact companion form to more than one hundred
decimal digits in the high-precision calculation.

The late recurrence approaches

\[
\boxed{
y_{n+4}
=
-y_n
+
4y_{n+1}
-
6y_{n+2}
+
4y_{n+3},
}
\]

or equivalently

\[
\boxed{
\Delta^4 y_n=0
}
\]

in the frozen leading form.

Because the true coefficients remain time-dependent, this does **not** by
itself imply a fourfold unit eigenvalue for the long cocycle.

It is a local memory normal form.

---

## 7. The leading defect is cubic

Write

\[
c_n
=
(-1,4,-6,4)
+
\delta c_n.
\]

Numerically,

\[
\delta c_n
\]

becomes almost parallel to

\[
\boxed{
(1,-3,3,-1).
}
\]

Projecting onto this direction gives

\[
\delta c_n
=
\varepsilon_n(1,-3,3,-1)
+
r_n.
\]

Measured values are:

| epoch | \(\varepsilon_n\) | \(n\varepsilon_n\) | \(\|r_n\|\) |
|---:|---:|---:|---:|
| 728 | \(5.5349\times10^{-2}\) | 40.2938 | \(7.0862\times10^{-4}\) |
| 10,000 | \(1.2374\times10^{-3}\) | 12.3739 | \(3.4362\times10^{-7}\) |
| 100,000 | \(1.0978\times10^{-4}\) | 10.9775 | \(2.6871\times10^{-9}\) |
| 1,000,000 | \(1.0458\times10^{-5}\) | 10.4581 | \(2.4275\times10^{-11}\) |

For a frozen recurrence, this leading deformation changes the characteristic
polynomial from

\[
(\lambda-1)^4
\]

to

\[
(\lambda-1)^4
+
\varepsilon_n(\lambda-1)^3
=
(\lambda-1)^3
(\lambda-1+\varepsilon_n).
\]

Again, the actual map is time-varying and the future-readout basis itself
changes with \(n\). Frozen roots are therefore descriptive, not a proof of
the long-time cocycle spectrum.

What is robust is the observed hierarchy:

\[
\boxed{
\text{four-sample memory form}
\quad+\quad
\text{near-fourth-difference structure}
\quad+\quad
\text{rapidly shrinking phase-hidden coupling}.
}
\]

---

## 8. Exact dimension versus effective dimension

At epochs 728, 10,000 and 100,000, the certified future-observable dimension is

\[
\boxed{4}.
\]

No tangent direction can be discarded if exact future phase readouts are
required.

At the same time, the smallest observability singular value and the measured
phase-hidden couplings collapse rapidly with training.

Thus the system has two distinct notions of dimension:

\[
\boxed{
\text{exact future-observable dimension}=4
}
\]

and a tail-dependent notion of effective or tolerance-dependent dimension.

The latter can approach one without the exact rank ever dropping.

---

## 9. The remaining asymptotic theorem

In the moving phase-hidden splitting, write schematically

\[
\begin{pmatrix}
p_{n+1}\\
h_{n+1}
\end{pmatrix}
=
\begin{pmatrix}
a_n&b_n^T\\
c_n&D_n
\end{pmatrix}
\begin{pmatrix}
p_n\\
h_n
\end{pmatrix}.
\]

Eliminating \(h_n\) produces a scalar Volterra-type equation whose memory
kernel contains terms of the form

\[
b_m^T
D_{m-1}\cdots D_{j+1}
c_j.
\]

The local scalar selector corresponds to retaining only the instantaneous
\(a_n\) channel.

A sufficient route to a full locking result is therefore:

1. control the hidden propagators generated by \(D_n\);
2. prove summable bounds on the phase-hidden memory kernel;
3. show that the full derivative differs from the scalar product by only a
   finite nonzero renormalization;
4. then apply the existing \(2/3\)--\(5/3\) local tail law.

The present data strongly motivate this route: the first two-step memory
correction falls from about \(5.6\times10^{-3}\) of the local defect at epoch
728 to about \(1.8\times10^{-8}\) at epoch \(10^6\).

But the summability theorem has not yet been proved.

---

## 10. Current independent 3+1 chain

The empirical / derived chain now reads

\[
\boxed{
\text{controlled nonzero difference}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{transverse transport and amplification}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\bar z^2\text{ threefold endogenous selector}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{phase projection creates hidden temporal memory}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{all four tangent channels are future-observable}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{full phase dynamics has an exact four-sample memory form}.
}
\]

The remaining tangent-level completion problem is the asymptotic control of
that memory kernel.

No appeal to Free Numbers or to a future-causal interpretation is required for
this statement.

---

## 11. Reproduction

Run

~~~bash
python examples/xnor_full_phase_cocycle.py
python examples/xnor_phase_hidden_coupling.py
python -m pip install mpmath==1.4.1
python examples/xnor_future_phase_coordinates.py
~~~

The full-cocycle scan cross-checks its two-epoch value against the independent
high-precision result in FUTURE_PHASE_OBSERVABILITY.md.

All 33 ordinary unit tests pass on the research branch.
