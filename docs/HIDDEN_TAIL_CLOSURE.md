# Hidden-tail closure and selector summability

Status: asymptotic correction and closure note.

This note corrects the provisional interpretation in SELECTOR_ASYMPTOTICS.md,
SGD_TAIL_SCALING.md, and ANALYTIC_SELECTOR_TAIL.md.

The earlier finite-window fit

\[
a_N \sim \frac{C}{N\log N}
\]

was too optimistic as an asymptotic law.

A longer-horizon disambiguation shows that the better current asymptotic model
is

\[
\boxed{
a_N
\sim
\frac{C}{N(\log N)^{3/2}},
}
\]

which is summable.

Therefore the base centered-XNOR SGD dynamics appears to retain and continue
sorting the historical residual for a very long time, but does **not** supply
infinite cumulative selector action.

That distinction restores a genuine persistence / locking gap.

---

## 1. Why the previous fit was deceptive

Over \(10^4\) to \(10^6\) epochs,

\[
\frac1{\log N}
\]

and a weak negative power of \(N\) are numerically difficult to distinguish.

The quantity

\[
N\log N\,a_N
\]

looked almost constant, leading to the provisional hypothesis

\[
a_N\asymp\frac1{N\log N}.
\]

However the exact branch-ray phase derivative, extended far beyond the original
window, shows a systematic downward drift in this normalization.

The competing normalization

\[
\boxed{
N(\log N)^{3/2}a_N
}
\]

stabilizes instead.

Representative exact branch-tangent values are:

| \(N\) | \(a_N\) | \(N\log N\,a_N\) | \(N(\log N)^{3/2}a_N\) |
|---:|---:|---:|---:|
| \(10^6\) | \(8.26287\times10^{-9}\) | 0.11416 | 0.42431 |
| \(10^7\) | \(6.83613\times10^{-10}\) | 0.11019 | 0.44236 |
| \(2\times10^7\) | \(3.22758\times10^{-10}\) | 0.10852 | 0.44495 |
| \(5\times10^7\) | \(1.19632\times10^{-10}\) | 0.10604 | 0.44647 |
| \(10^8\) | \(5.64501\times10^{-11}\) | 0.10399 | 0.44630 |

Thus the best current finite-horizon asymptotic law is

\[
\boxed{
a_N
\approx
\frac{0.446}{N(\log N)^{3/2}}.
}
\]

This is still numerical asymptotics, not a theorem.

---

## 2. Hidden state moves on a log-log scale

The coarse hidden three-copy state continues moving after task convergence.

Its epoch-scale drift is nearly collinear with its accumulated displacement.

On the measured tail the hidden update has the form

\[
\Delta w_N
=
O\!\left(
\frac1{N\log N}
\right),
\]

so integration gives

\[
\boxed{
w_N
=
v\,\log\log N
+
O(1)
}
\]

for an asymptotic direction \(v\), provided the direction converges.

The direction does in fact stabilize numerically: the cosine between the
hidden epoch update and the accumulated hidden displacement is close to one.

This is the correct sense in which the hidden state has a log-log tail.

It is the **hidden parameter vector**, not the selector action itself, that
naturally carries the \(\log\log N\) growth.

---

## 3. The hidden logits reveal the asymptotic direction

For the coarse representative hidden unit write

\[
w=(w_0,w_1,w_2),
\]

with augmented-input logits

\[
u_{00}=w_0,
\]

\[
u_{01}=w_0+w_2,
\]

\[
u_{10}=w_0+w_1,
\]

\[
u_{11}=w_0+w_1+w_2.
\]

Late local slopes with respect to

\[
L=\log\log N
\]

move toward the pattern

\[
\boxed{
\frac{d}{dL}
(u_{00},u_{01},u_{10},u_{11})
\approx
\left(
\frac92,
\frac32,
\frac32,
-\frac32
\right).
}
\]

Equivalently the hidden weight direction is approaching

\[
\boxed{
v
\propto
(3,-2,-2).
}
\]

This direction is geometrically natural for the XNOR corner structure:

\[
(3,-2,-2)\cdot(1,0,0)=3,
\]

\[
(3,-2,-2)\cdot(1,0,1)=1,
\]

\[
(3,-2,-2)\cdot(1,1,0)=1,
\]

\[
(3,-2,-2)\cdot(1,1,1)=-1.
\]

Thus one corner has a larger margin and the remaining three approach equal
absolute hidden margins.

The observed coefficient is consistent with

\[
w_N
\sim
\frac32(3,-2,-2)\log\log N
+
O(1).
\]

This rational coefficient pattern is a strong asymptotic conjecture, not yet
a proved limit.

---

## 4. Exact sigmoid conversion

For hidden preactivation \(u\),

\[
g(u)
=
\sigma(u)(1-\sigma(u))
=
\frac1{2+2\cosh u}.
\]

Hence for \(|u|\to\infty\),

\[
\boxed{
g(u)
=
e^{-|u|}
\left(
1+O(e^{-|u|})
\right).
}
\]

Likewise

\[
g'(u)
=
g(u)(1-2\sigma(u))
\]

has the same leading magnitude:

\[
\boxed{
|g'(u)|
\sim
e^{-|u|}.
}
\]

Therefore if the slow hidden support logits satisfy

\[
|u_N|
=
\frac32\log\log N
+
O(1),
\]

then

\[
\boxed{
g_N,\ |g'_N|
=
\Theta\!\left(
(\log N)^{-3/2}
\right).
}
\]

This replaces the provisional finite-window reading

\[
g'_N
\sim
(\log N)^{-1}.
\]

---

## 5. Selector tail

The task output delta remains on the established tail

\[
\boxed{
|d_N|
=
\Theta(N^{-1}).
}
\]

The exact quadratic copy-space selector contains the positive \(dg'\) sector.

Combining the two tails gives

\[
\boxed{
d_N g'_N
=
\Theta\!\left(
\frac1{N(\log N)^{3/2}}
\right).
}
\]

The exact branch-ray tangent measurement follows the same class:

\[
\boxed{
a_N
=
\Theta\!\left(
\frac1{N(\log N)^{3/2}}
\right).
}
\]

This matches the long-horizon numerical normalization directly.

---

## 6. The series now converges

Unlike

\[
\sum_N\frac1{N\log N},
\]

the series

\[
\boxed{
\sum_N
\frac1{N(\log N)^{3/2}}
}
\]

converges.

Indeed,

\[
\int^\infty
\frac{dx}{x(\log x)^{3/2}}
<
\infty.
\]

Therefore, if the \(3/2\) tail is the true asymptotic regime,

\[
\boxed{
\mathcal A_\infty
=
\sum_N a_N
<
\infty.
}
\]

So a generic off-ray history retains a finite angular offset.

The original deterministic XNOR SGD keeps sorting for a very long time, but
does not produce exact asymptotic branch locking by itself.

---

## 7. What survives from the earlier result

Several earlier conclusions remain intact:

\[
\boxed{
\text{task convergence}
\not\Rightarrow
\text{selector death}
}
\]

remains true.

The residual remains present.

The selector continues acting long after ordinary task convergence.

The difference still becomes an endogenous selector.

What changes is only the final persistence claim.

The selector action appears to have a **finite total budget**.

Thus:

\[
\boxed{
\text{long-lived selector}
\neq
\text{self-locking selector}.
}
\]

---

## 8. Consequence for the persistence gap

This restores the missing mechanism in a sharper form.

Free Numbers can identify the difference that future continuation must retain.

Three-plus-one shows that this retained difference can become an endogenous
selector.

The ordinary XNOR SGD then supplies a long-lived but apparently summable
selector action.

Therefore a complete persistent specialization requires one more ingredient if
the intended endpoint is exact locking:

\[
\boxed{
\text{a mechanism that changes the selector tail from summable to
non-summable, or otherwise freezes the selected branch.}
}
\]

This is now a much narrower and better-defined persistence gap than the
original vague "keep the drive alive" question.

---

## 9. Current closed chain

The current evidence supports

\[
\boxed{
\text{output task tail}
\sim
N^{-1}
}
\]

together with

\[
\boxed{
\text{hidden parameter drift}
\sim
(N\log N)^{-1}
}
\]

so that

\[
\boxed{
w_N
\sim
v\log\log N.
}
\]

The XNOR hidden geometry then gives slow support logits of order

\[
\boxed{
|u_N|
\sim
\frac32\log\log N,
}
\]

hence

\[
\boxed{
|g'_N|
\sim
(\log N)^{-3/2}.
}
\]

Finally,

\[
\boxed{
a_N
\sim
\frac{C}{N(\log N)^{3/2}},
}
\]

and therefore

\[
\boxed{
\mathcal A_\infty<\infty.
}
\]

This is the current stopping point.

---

## 10. Claim boundary

### Exact

- the sigmoid identity
  \[
  g(u)=1/(2+2\cosh u);
  \]
- the exact quadratic copy-space map;
- the exact branch-ray phase derivative;
- convergence of
  \[
  \sum 1/[N(\log N)^{3/2}].
  \]

### Strong numerical evidence

- hidden state motion on a \(\log\log N\) scale;
- asymptotic hidden direction near
  \[
  (3,-2,-2);
  \]
- slow support-logit coefficient near \(3/2\);
- selector normalization
  \[
  N(\log N)^{3/2}a_N
  \to
  \text{positive constant}
  \]
  over the extended measured range.

### Not yet proved

- the exact rational coefficient \(3/2\);
- convergence of the hidden direction;
- a rigorous asymptotic theorem for the full online SGD trajectory.

The next theoretical task, when work resumes, is to derive the
\((3,-2,-2)\) hidden direction and the \(3/2\) coefficient directly from the
late XNOR update.
