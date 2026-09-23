# Selector-action asymptotics

Status: long-horizon finite-time evidence from the actual centered-XNOR
dynamics.

This note follows `SELECTOR_PERSISTENCE.md`.

The question is now narrower:

\[
\boxed{
\mathcal A_N\to A_\infty<\infty
\quad\text{or}\quad
\mathcal A_N\to\infty?
}
\]

The present data strongly favor **slow divergence**, with

\[
\boxed{
\mathcal A_N
\approx
b+c\log\log N,
\qquad
c\approx0.09425,
}
\]

over the measured window \(2\times10^4\le N\le10^6\).

This is evidence, not yet an asymptotic theorem.


> **Tail-closure update.** A later exact branch-tangent and hidden-tail
> analysis extends the deterministic check through \(10^7\) epochs.  The
> selector still satisfies
>
> \[
> a_N\asymp(N\log N)^{-1},
> \]
>
> but the deeper factorization is
>
> \[
> (\log N)^{2/3}
> \times
> N^{-1}
> \times
> (\log N)^{-5/3}
> =
> (N\log N)^{-1}.
> \]
>
> Thus the earlier finite-window appearance \(|g'_N|\sim1/\log N\) should
> not be used as the final mechanism.  See
> [`HIDDEN_TAIL_CLOSURE.md`](HIDDEN_TAIL_CLOSURE.md).

---

## 1. Measured long-horizon course

Using the same branch-ray phase derivative

\[
\rho_N
=
\left.
\frac{\partial\theta_{\rm out}}
{\partial\theta_{\rm in}}
\right|_{\theta=0}
\]

and cumulative selector action

\[
\mathcal A_N
=
-\frac13\log|\rho_N|,
\]

the actual deterministic XNOR run gives:

| epoch \(N\) | MSE | \(\rho_N\) | \(\mathcal A_N\) | finite probe phase |
|---:|---:|---:|---:|---:|
| 10,000 | \(1.17124\times10^{-4}\) | 0.7773282 | 0.0839642 | 0.4431109 |
| 20,000 | \(5.37750\times10^{-5}\) | 0.7616152 | 0.0907713 | 0.4369952 |
| 50,000 | \(2.00112\times10^{-5}\) | 0.7428999 | 0.0990646 | 0.4296447 |
| 100,000 | \(9.63858\times10^{-6}\) | 0.7299860 | 0.1049100 | 0.4245341 |
| 200,000 | \(4.68429\times10^{-6}\) | 0.7179911 | 0.1104327 | 0.4197610 |
| 500,000 | \(1.82089\times10^{-6}\) | 0.7033964 | 0.1172782 | 0.4139210 |
| 1,000,000 | \(8.95113\times10^{-7}\) | 0.6932261 | 0.1221330 | 0.4098315 |

The selector action continues to increase throughout the window.

---

## 2. Local log-log slope

If

\[
\mathcal A_N
=
b+c\log\log N+o(1),
\]

then the local slope

\[
c_{\rm eff}
=
\frac{\Delta\mathcal A}
{\Delta\log\log N}
\]

should approach a constant.

Measured values are:

| interval | \(c_{\rm eff}\) |
|---|---:|
| \(10^4\to2\times10^4\) | 0.0938127 |
| \(2\times10^4\to5\times10^4\) | 0.0937221 |
| \(5\times10^4\to10^5\) | 0.0941357 |
| \(10^5\to2\times10^5\) | 0.0944652 |
| \(2\times10^5\to5\times10^5\) | 0.0945721 |
| \(5\times10^5\to10^6\) | 0.0943155 |

This is much flatter than expected from either a linear-in-\(\log N\) law or
simple saturation over the same window.

---

## 3. Competing simple fits

Using the late window \(N\ge2\times10^4\):

\[
\mathcal A_N\approx a+b\,x(N)
\]

gives:

| model coordinate \(x(N)\) | RMSE |
|---|---:|
| \(\log N\) | \(5.12\times10^{-4}\) |
| \(\log\log N\) | \(\boxed{1.94\times10^{-5}}\) |
| \(1/\log N\) | \(5.52\times10^{-4}\) |

The \(\log\log N\) fit is therefore about an order of magnitude tighter in
residual scale over this finite window.

The fitted law is

\[
\boxed{
\mathcal A_N
\approx
-0.125366
+
0.0942515\,\log\log N.
}
\]

Again, this is a finite-window empirical fit, not proof of the \(N\to\infty\)
limit.

---

## 4. Consequence for the branch-ray derivative

From

\[
\mathcal A_N
=
-\frac13\log\rho_N
\]

and

\[
\mathcal A_N
\sim
c\log\log N,
\]

we obtain

\[
\boxed{
\rho_N
\sim
C(\log N)^{-p},
\qquad
p=3c.
}
\]

The measured slope gives

\[
\boxed{
p\approx0.282754.
}
\]

Thus the branch-ray contraction tends toward zero extremely slowly if the
observed scaling persists.

---

## 5. What this means for locking

For the ideal reduced phase equation

\[
\dot\theta=-a(t)\sin3\theta,
\]

the exact transformed coordinate

\[
u=\tan\frac{3\theta}{2}
\]

obeys

\[
u(T)=u(0)e^{-3\mathcal A(T)}.
\]

Therefore a logarithmic-logarithmic action law would imply

\[
\boxed{
u_N
\sim
C(\log N)^{-p}.
}
\]

So complete locking can occur even though the instantaneous selector strength
vanishes.

It would simply be **extremely slow**.

This matters conceptually:

\[
\boxed{
\text{vanishing drive}
\not\Rightarrow
\text{finite total selector action}.
}
\]

The correct criterion is cumulative non-summability.

---

## 6. Current conclusion

The original persistence question has now split into three distinct statements.

### A. Does the residual survive?

For the tested channel and horizon:

\[
\boxed{\text{yes}.}
\]

### B. Does selector action continue after ordinary task convergence?

Through \(10^6\) epochs:

\[
\boxed{\text{yes}.}
\]

### C. Is the total selector action infinite?

The measured data strongly support

\[
\boxed{
\mathcal A_N
\sim
c\log\log N
}
\]

with \(c>0\), which would imply

\[
\mathcal A_\infty=\infty.
\]

But that final asymptotic statement remains unproved.

---

## 7. Consequence for the earlier missing-mechanism hypothesis

The previous working hypothesis was that an additional persistence mechanism
might be needed because ordinary task training would cease before branch
locking completed.

The long-horizon result weakens that hypothesis.

The actual SGD dynamics already contains:

\[
\boxed{
\text{retained residual}
\rightarrow
\text{continued selector action}
\rightarrow
\text{slow ongoing branch contraction}.
}
\]

Therefore an additional mechanism should **not** be introduced merely to keep
the selector alive.

It becomes necessary only if one can show that

\[
\mathcal A_\infty<\infty
\]

or that another required branch-conditioned residual is erased.

At present, the simpler model is that at least this part of persistence is
already internal to the original learning dynamics.

---

## 8. Relation to future admissibility

Free Numbers identifies differences that some allowed continuation can later
detect.

The XNOR dynamics now supplies a concrete example in which such a retained
difference is not only preserved but continues to alter the orientation of its
own future continuation long after the present task criterion has effectively
been satisfied.

The current chain is therefore

\[
\boxed{
\text{retained difference}
\rightarrow
\text{endogenous selector}
\rightarrow
\text{non-summable candidate action}
\rightarrow
\text{asymptotic branch selection candidate}.
}
\]

This remains an ordinary forward dynamical process.

Its relevance to a later future-causal theory is structural: it provides a
minimal mechanism by which a difference classified by future continuation can
remain active enough to shape which continuation is realized.

---

## 9. Reproduction

Run:

~~~bash
python examples/xnor_selector_asymptotics.py
~~~

The long-horizon script uses the unmodified centered-XNOR training rule and
checkpoints through \(10^6\) epochs.

The run recorded here was executed in GitHub Actions on Python 3.12 after all
30 unit tests passed.

---

## 10. Direct local verification

A follow-up one-epoch diagnostic now finds

\[
\mathrm{MSE}_N
=
\Theta(N^{-1})
\]

and, independently,

\[
\boxed{
a_N
=
-\frac13\log\rho_N^{(1)}
=
\Theta((N\log N)^{-1})
}
\]

over \(10^4\le N\le10^6\).

Thus the local actual update has exactly the summation class required for

\[
\mathcal A_N
=
\Theta(\log\log N).
\]

A one-epoch Fourier extraction on the current coarse state also shows that the
same quadratic \(\bar z^2\) selector tracks this tail scaling.

See [`SGD_TAIL_SCALING.md`](SGD_TAIL_SCALING.md).

The remaining task is no longer to guess the tail class. It is to derive a
positive asymptotic lower bound, or equivalent expansion, from the exact
one-sample sigmoid SGD equations.

That analytic step would turn the finite-horizon non-summability evidence into
a proof.
