# Selector persistence after task convergence

Status: direct diagnostic on the actual deterministic centered-XNOR training
dynamics.

This note tests one specific assumption from the future-admissibility handoff:

> Does the threefold selector effectively stop once the ordinary XNOR task has
> converged, leaving an off-ray residual frozen before branch locking?

The finite-horizon answer is **no**.

The residual remains present and the selector action continues to accumulate
well after the ordinary task target has been reached.

---

## 1. Diagnostic

Work in the original hidden-to-output transverse input channel and follow the
phase-0 singleton ray.

Seed two nearby histories at

\[
\theta_{\pm}=\pm\delta,
\qquad
\delta=10^{-4}.
\]

After \(N\) epochs, project the nonlinear transverse residual onto the
normalized linear response direction of the cumulative tangent map.

Define the finite-course branch-ray phase derivative

\[
\boxed{
\rho_N
=
\left.
\frac{\partial \theta_{\mathrm{out}}}
{\partial \theta_{\mathrm{in}}}
\right|_{\theta=0}
}
\]

using the centered finite difference

\[
\rho_N
\approx
\frac{
\theta_N(+\delta)-\theta_N(-\delta)
}{
2\delta
}.
\]

Define cumulative selector action

\[
\boxed{
\mathcal A_N
=
-\frac13\log|\rho_N|.
}
\]

A finite probe is also seeded at

\[
\theta_0=\frac{\pi}{6}
\]

to check whether an actual off-ray history continues moving toward the
phase-0 singleton ray.

The seed amplitude used below is

\[
r=0.1.
\]

---

## 2. Why this quantity matters

For the ideal reduced phase law

\[
\dot\theta
=
-a(t)\sin 3\theta,
\]

set

\[
u=\tan\frac{3\theta}{2}.
\]

Then

\[
\dot u=-3a(t)u,
\]

so

\[
u(T)
=
u(0)
\exp\left(
-3\int_0^T a(t)\,dt
\right).
\]

Therefore exact asymptotic branch locking requires cumulative selector action
to diverge:

\[
\boxed{
\int_0^\infty a(t)\,dt=\infty.
}
\]

In discrete form, if \(\rho_e\) is the local branch-ray phase derivative,

\[
\boxed{
\prod_e|\rho_e|=0
\iff
\sum_e-\log|\rho_e|=\infty.
}
\]

Thus the correct persistence question is not whether the instantaneous drive
remains bounded away from zero.

A drive can decay to zero and still produce complete locking if its cumulative
action is non-summable.

---

## 3. Measured result

For the current deterministic centered-XNOR implementation:

| Epoch | MSE | \(\rho_N\) | \(\mathcal A_N\) | phase of \(\pi/6\) probe | projected residual amplitude |
|---:|---:|---:|---:|---:|---:|
| 728 | 0.0099993 | 0.8840931 | 0.0410643 | 0.4829183 | 1.4967043 |
| 5,000 | 0.00026837 | 0.7949240 | 0.0765029 | 0.4498922 | 2.5139422 |
| 10,000 | 0.00011712 | 0.7773282 | 0.0839642 | 0.4431109 | 2.7027781 |
| 100,000 | \(9.64\times10^{-6}\) | 0.7299860 | 0.1049100 | 0.4245341 | 3.1973292 |

The ordinary task target is already reached at epoch 728.

Nevertheless,

\[
\boxed{
\mathcal A_{100000}
>
\mathcal A_{10000}
>
\mathcal A_{5000}
>
\mathcal A_{728}.
}
\]

The finite probe also continues moving toward the singleton ray:

\[
\frac{\pi}{6}
\approx0.523599
\rightarrow
0.482918
\rightarrow
0.449892
\rightarrow
0.443111
\rightarrow
0.424534.
\]

At the same time the projected residual amplitude increases rather than being
erased.

---

## 4. What the test falsifies

The following finite-horizon story is not supported:

\[
\text{task converges}
\rightarrow
\text{updates die}
\rightarrow
\text{selector freezes immediately}.
\]

At least through \(10^5\) epochs, ordinary task convergence does **not**
terminate the branch-sorting dynamics.

The difference survives, and the phase contraction continues.

So the earlier persistence gap must be split.

---

## 5. Two different persistence questions

### 5.1 State persistence

Does the retained historical difference itself survive?

For this tested channel and horizon:

\[
\boxed{\text{yes}.}
\]

The residual is not erased; its projected amplitude continues to grow.

### 5.2 Selector-action persistence

Does the accumulated directional sorting become large enough to force exact
asymptotic branch locking?

This remains open.

The relevant question is now

\[
\boxed{
\lim_{N\to\infty}\mathcal A_N
=
\infty
\quad\text{or}\quad
<\infty?
}
\]

This is sharper than asking whether a raw "drive" persists.

---

## 6. The persistence gap becomes a summability gap

The current open problem is therefore better named the

\[
\boxed{\text{selector-action summability gap}.}
\]

If

\[
\mathcal A_\infty<\infty,
\]

then a generic off-ray history retains a finite angular offset.

If

\[
\mathcal A_\infty=\infty,
\]

then even a selector whose instantaneous strength tends to zero can still
produce asymptotic branch locking.

The present finite-horizon data distinguish these possibilities from the
previous "updates simply stop" picture, but do not yet prove which asymptotic
case holds.

---

## 7. Relation to retained-difference quotients

Free Numbers supplies the operation-based criterion for which differences must
remain distinguishable under future continuation.

The present XNOR test adds a dynamical fact:

\[
\boxed{
\text{a branch-relevant residual can remain present and continue to be sorted
after the current task loss is already small.}
}
\]

Thus "future-relevant information is retained" and "future-relevant
information receives enough cumulative selector action to lock" are distinct
questions.

The first is already observed here for the tested residual.

The second is the remaining asymptotic problem.

---

## 8. Reproduction

Run

~~~bash
python examples/xnor_selector_persistence.py
~~~

The unit test

~~~text
tests/test_selector_persistence.py
~~~

checks the deterministic values at epochs 728, 5,000, 10,000, and 100,000.

The implementation is in

~~~text
src/threeplusone/transverse.py
~~~

as

~~~text
scan_selector_persistence
~~~

and uses the unmodified network training rule.

---

## 9. Next exact test

The next test should estimate the late-time behavior of

\[
\mathcal A_N.
\]

Do not ask merely whether it is still increasing at another arbitrary finite
epoch.

Test candidate asymptotic classes, for example

\[
\mathcal A_N\to A_\infty,
\]

\[
\mathcal A_N\sim c\log\log N,
\]

or

\[
\mathcal A_N\sim c\log N.
\]

The immediate mathematical target is to determine whether the effective local
selector action is summable.

That decides whether the current XNOR dynamics already contains asymptotic
branch locking, or whether an additional persistence mechanism is genuinely
required.
