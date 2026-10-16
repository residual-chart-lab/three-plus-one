# Hidden-tail closure: the 2/3 - 5/3 balance

Status: analytic reduction plus deterministic long-horizon evidence.

This note records the proposed hidden-tail reduction following
`ANALYTIC_SELECTOR_TAIL.md`.

The main correction is:

\[
\boxed{
|g'_N|
\not\sim
(\log N)^{-1}
}
\]

for the hidden support directions themselves.

The data and reduced dynamics instead support

\[
\boxed{
|g'_N|
\sim
C_g(\log N)^{-5/3}.
}
\]

The exact selector action nevertheless remains

\[
\boxed{
a_N
\sim
\frac{C_a}{N\log N},
}
\]

because the retained branch radius grows as

\[
\boxed{
R_N
\sim
C_R(\log N)^{2/3}.
}
\]

The surviving \(1/\log N\) therefore comes from the exponent balance

\[
\boxed{
\frac23-\frac53=-1,
}
\]

not from the hidden sigmoid derivative alone.

---

## 1. Notation

Write

\[
L_N=\log N,
\qquad
\ell_N=\log\log N.
\]

Let

- \(A_N\) be the magnitude of the relevant coarse trio output weight,
- \(R_N\) be the phase-0 transverse branch radius,
- \(d_N\) be the ordinary output delta scale,
- \(u_{01},u_{10},u_{11}\) be the coarse representative hidden preactivations,
- \(a_N\) be the exact one-epoch selector action
  \[
  a_N=-\frac13\log|\rho_N|.
  \]

---

## 2. The measured 2/3 law

The output-weight scale is extremely well described by

\[
\boxed{
A_N
\asymp
L_N^{2/3}.
}
\]

The branch radius obeys the same power:

\[
\boxed{
R_N
\asymp
L_N^{2/3}.
}
\]

Long-horizon measurements are:

| \(N\) | \(A_N/L_N^{2/3}\) | \(R_N/L_N^{2/3}\) | \(N L_N a_N\) |
|---:|---:|---:|---:|
| \(10^6\) | 1.057863 | 0.690202 | 0.114156 |
| \(2\times10^6\) | 1.058431 | 0.689387 | 0.113230 |
| \(5\times10^6\) | 1.060006 | 0.687245 | 0.111646 |
| \(10^7\) | 1.061746 | 0.684942 | 0.110185 |

The \(2/3\) law is at present an empirical asymptotic law of this deterministic
XNOR trajectory, not yet a theorem.

---

## 3. The effective hidden clock

The ordinary binary-sigmoid tail already gives

\[
\boxed{
|d_N|
\asymp
\frac{D}{N}.
}
\]

The hidden update contains the product

\[
A_N d_N.
\]

Therefore the natural hidden-learning clock is

\[
\tau_N
\sim
\sum_{n\le N}
A_n |d_n|.
\]

Using the measured \(2/3\) law,

\[
\tau_N
\asymp
\sum_{n\le N}
\frac{(\log n)^{2/3}}{n}.
\]

Hence

\[
\boxed{
\tau_N
\asymp
(\log N)^{5/3}.
}
\]

More precisely, the continuum primitive is

\[
\int
\frac{(\log x)^{2/3}}{x}\,dx
=
\frac35(\log x)^{5/3}.
\]

This is the source of the \(5/3\) exponent.

---

## 4. The three effective hidden support points

For the representative coarse trio unit, the relevant output weight is
negative in the observed branch.

The hidden-gradient signs then make the late active samples

\[
01:\ +,
\qquad
10:\ +,
\qquad
11:\ -.
\]

The \(00\) sample has the opposite preferred sign but becomes exponentially
suppressed because its hidden preactivation is much larger.

Ignoring that asymptotically negligible term, the effective augmented inputs
are

\[
x_{01}=(1,0,1),
\]

\[
x_{10}=(1,1,0),
\]

\[
x_{11}=(1,1,1),
\]

with signs \(+,+,-\).

The unit-margin equations are

\[
w\cdot x_{01}=1,
\]

\[
w\cdot x_{10}=1,
\]

\[
-w\cdot x_{11}=1.
\]

They have the unique solution

\[
\boxed{
\widehat w=(3,-2,-2).
}
\]

Therefore the three active hidden margins are equal at leading order, while

\[
u_{00}
=
3\times
\text{support margin}.
\]

This also explains the observed asymptotic hidden-gradient coefficient ratio

\[
\boxed{
5:5:7.
}
\]

Indeed,

\[
5x_{01}
+
5x_{10}
-
7x_{11}
=
(3,-2,-2)
=
\widehat w.
\]

So the late hidden update is internally consistent with the same support
geometry that generates the branch direction.

---

## 5. Hidden-margin growth in the effective clock

For saturated sigmoid units,

\[
g(u)
=
\sigma(u)(1-\sigma(u))
\sim
e^{-|u|}.
\]

In the effective clock \(\tau\), the support dynamics therefore has the
standard exponential-tail form

\[
\frac{dw}{d\tau}
\sim
\sum_s
c_s y_s x_s
e^{-y_s w\cdot x_s}.
\]

Because the three support vectors span the hidden parameter space, the leading
solution has

\[
\boxed{
w(\tau)
=
\widehat w\log\tau
+
O(1)
}
\]

up to slowly varying coefficient corrections.

Thus the active margins satisfy

\[
u_{01}
=
\log\tau+O(1),
\]

\[
u_{10}
=
\log\tau+O(1),
\]

\[
-u_{11}
=
\log\tau+O(1).
\]

Since

\[
\tau_N
\asymp
L_N^{5/3},
\]

we obtain

\[
\boxed{
u_{01},
u_{10},
-u_{11}
=
\frac53\ell_N+O(1).
}
\]

Meanwhile

\[
u_{00}
=
5\ell_N+O(1).
\]

---

## 6. Direct long-horizon check of the 5/3 law

At the latest checkpoints, subtracting

\[
\frac53\ell_N
\]

from each active margin gives:

| \(N\) | \(u_{01}-\frac53\ell_N\) | \(u_{10}-\frac53\ell_N\) | \(|u_{11}|-\frac53\ell_N\) |
|---:|---:|---:|---:|
| \(10^6\) | -2.407274 | -2.403769 | -2.387452 |
| \(2\times10^6\) | -2.418002 | -2.415151 | -2.414789 |
| \(5\times10^6\) | -2.430803 | -2.428624 | -2.445982 |
| \(10^7\) | -2.439483 | -2.437698 | -2.466335 |

The three support offsets have nearly coalesced.

The actual derivatives with respect to \(\ell=\log\log N\) are also moving
toward the predicted value \(5/3\):

| \(N\) | \(du_{01}/d\ell\) | \(du_{10}/d\ell\) | \(d|u_{11}|/d\ell\) |
|---:|---:|---:|---:|
| \(10^6\) | 1.4437 | 1.4292 | 1.0863 |
| \(2\times10^6\) | 1.4516 | 1.4394 | 1.1301 |
| \(5\times10^6\) | 1.4641 | 1.4543 | 1.1844 |
| \(10^7\) | 1.4745 | 1.4663 | 1.2228 |

The slowest \(11\) margin is still catching up, but the support values
themselves have already become nearly equal.

---

## 7. The hidden sigmoid derivative

For large positive \(u\),

\[
g'(u)
=
g(u)(1-2\sigma(u))
=
-e^{-u}(1+o(1)).
\]

For large negative \(u\),

\[
g'(u)
=
e^{u}(1+o(1)).
\]

Therefore, on each active support sample,

\[
\boxed{
|g'_N|
\asymp
e^{-(5/3)\ell_N}
=
(\log N)^{-5/3}.
}
\]

The \(00\) sample is smaller:

\[
|g'_{00}|
=
O((\log N)^{-5}).
\]

This corrects the earlier provisional shorthand

\[
|g'_N|\sim(\log N)^{-1}.
\]

That earlier law was a finite-window appearance, not the deeper factorization.

---

## 8. Why the selector still has the 1/(N log N) tail

The quadratic / tangent selector is not controlled by \(g'_N\) alone.

The broken branch itself has radius

\[
R_N
\asymp
L_N^{2/3}.
\]

The symmetry-breaking difference between radial and angular transport is first
order in that retained radius and first order in the hidden sensitivity.

Schematically,

\[
1-\rho_N
\asymp
R_N\,|d_N|\,|g'_N|.
\]

Insert the three tail laws:

\[
R_N
\asymp
L_N^{2/3},
\]

\[
|d_N|
\asymp
N^{-1},
\]

\[
|g'_N|
\asymp
L_N^{-5/3}.
\]

Then

\[
\boxed{
1-\rho_N
\asymp
\frac{1}{N L_N}.
}
\]

Since \(\rho_N\to1\),

\[
-\log\rho_N
\sim
1-\rho_N,
\]

and therefore

\[
\boxed{
a_N
=
-\frac13\log|\rho_N|
\asymp
\frac{C}{N\log N}.
}
\]

This agrees with the exact branch-tangent measurement through \(10^7\)
epochs:

\[
N\log N\,a_N
:
0.11416
\rightarrow
0.11019.
\]

Thus the non-summability result survives the hidden-tail correction.

---

## 9. The actual cancellation

The decisive balance is

\[
\boxed{
(\log N)^{2/3}
\times
(\log N)^{-5/3}
=
(\log N)^{-1}.
}
\]

The first factor is the growth of the retained branch difference.

The second is the decay of hidden sigmoid sensitivity.

The selector survives because the history-bearing residual itself grows while
the local hidden response saturates.

Therefore the persistent selector is not produced by a hidden derivative that
stays unusually large.

It is produced by a compensation between

\[
\boxed{
\text{retained-difference growth}
}
\]

and

\[
\boxed{
\text{local-sensitivity decay}.
}
\]

This is the sharper mechanism.

---

## 10. Consequence for the local action sum

Conditional on the positive asymptotic comparison

\[
a_N\asymp\frac{1}{N\log N},
\]

the sum of local actions satisfies

\[
\mathcal A_N^{\mathrm{local}}:=\sum_{n\le N}a_n
=\Theta(\log\log N)\longrightarrow\infty.
\]

This is the action of the product of one-epoch scalar projections. The
actual cumulative phase derivative propagates a four-component tangent.
Components invisible to one phase readout can return in the next epoch,
so the local sum does not by itself establish asymptotic branch locking.
See [the future-observability check](FUTURE_PHASE_OBSERVABILITY.md).

---

## 11. Claim boundary

### Exact / derived

- the hidden support geometry \((01+,10+,11-)\);
- the unit-margin direction
  \[
  (3,-2,-2);
  \]
- the coefficient identity
  \[
  5x_{01}+5x_{10}-7x_{11}=(3,-2,-2);
  \]
- given \(A_N\asymp L_N^{2/3}\) and \(d_N\asymp N^{-1}\),
  \[
  \tau_N\asymp L_N^{5/3};
  \]
- given the exponential-tail hidden reduction,
  \[
  |g'_N|\asymp L_N^{-5/3};
  \]
- combining this with \(R_N\asymp L_N^{2/3}\),
  \[
  a_N\asymp(NL_N)^{-1}.
  \]

### Strong deterministic evidence

- \(A_N/L_N^{2/3}\) is nearly constant through \(10^7\);
- \(R_N/L_N^{2/3}\) is nearly constant through \(10^7\);
- the three active hidden margins align with
  \[
  (5/3)\log\log N+O(1);
  \]
- exact branch-tangent action satisfies
  \[
  N\log N\,a_N\approx0.11
  \]
  through \(10^7\).

### Still not a theorem

The upstream \(2/3\) law itself has not yet been proved from the full SGD
recurrence.

The coupled four-channel tangent has now been propagated directly through
one-million-epoch future windows, and its phase/hidden blocks have been
measured. The hidden return is nonzero but becomes rapidly weak in the SGD
tail. Rank-four observability also gives an exact four-sample scalar memory
form for the tangent phase.

See [FULL_PHASE_COCYCLE.md](FULL_PHASE_COCYCLE.md).

A full asymptotic theorem would now need control of the \(2/3\) law, a
summable bound on the induced phase-hidden memory kernel, and the nonlinear
finite-perturbation remainder.

---

## 12. Reproduction

Run

~~~bash
python examples/xnor_hidden_tail_closure.py
~~~

The diagnostic uses the unmodified deterministic XNOR training rule and
checkpoints through \(10^7\) epochs.
