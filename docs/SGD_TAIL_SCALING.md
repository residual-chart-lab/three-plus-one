# Direct verification of the SGD tail

Status: finite-horizon verification of the scaling mechanism behind
`SELECTOR_ASYMPTOTICS.md`.

The previous long-horizon experiment found

\[
\mathcal A_N
\approx
b+c\log\log N.
\]

This note asks a more local question:

> Does the actual one-epoch XNOR update itself have the tail scaling required
> to generate \(\log\log N\) cumulative selector action?

Over \(10^4\le N\le10^6\), the answer is strongly **yes**.

The key directly measured law is

\[
\boxed{
a_N
=
-\frac13\log\rho_N^{(1)}
\asymp
\frac{C}{N\log N},
}
\]

where \(\rho_N^{(1)}\) is the one-epoch phase derivative on the phase-0
singleton ray.

---

## 1. Exact sigmoid tail identity

For one sample let

\[
\epsilon=|t-y|,
\qquad
t\in\{0,1\}.
\]

The output delta used by the implementation is

\[
d=(t-y)y(1-y).
\]

For either binary target,

\[
y(1-y)=\epsilon(1-\epsilon),
\]

so exactly

\[
\boxed{
|d|
=
\epsilon^2(1-\epsilon).
}
\]

Therefore in the saturated regime,

\[
\boxed{
|d|
=
\epsilon^2+O(\epsilon^3).
}
\]

The sample squared error is \(\epsilon^2\), so the output delta becomes
asymptotically equal to the squared-error scale.

---

## 2. Why a \(1/N\) task tail is natural

Let \(m\) be a correctly signed output margin.

In the saturated regime,

\[
\epsilon
\sim
e^{-m},
\]

hence

\[
\epsilon^2
\sim
e^{-2m}.
\]

If the bounded feature direction has a nonzero limiting projection onto the
output update, then the margin obeys schematically

\[
\frac{dm}{dN}
\sim
\kappa e^{-2m}.
\]

Therefore

\[
\frac{d}{dN}e^{2m}
\sim
2\kappa,
\]

so

\[
e^{2m}
\sim
2\kappa N,
\]

and

\[
\boxed{
m_N
=
\frac12\log N+O(1),
}
\]

which gives

\[
\boxed{
\epsilon_N^2
\asymp
\frac1N.
}
\]

This is a conditional asymptotic reduction, not a general theorem for all
multilayer networks.

---

## 3. Measured task tail

A phase-0 branch history with initial transverse amplitude \(0.1\) was trained
under the unmodified online XNOR rule.

| \(N\) | \(N\,\mathrm{MSE}\) | \(N\,\overline{|d|}\) | mean signed margin | \(\frac12\log N\) |
|---:|---:|---:|---:|---:|
| 10,000 | 1.18855 | 1.17540 | 4.51661 | 4.60517 |
| 20,000 | 1.09384 | 1.08565 | 4.90705 | 4.95174 |
| 50,000 | 1.02004 | 1.01539 | 5.40191 | 5.40989 |
| 100,000 | 0.98401 | 0.98089 | 5.76726 | 5.75646 |
| 200,000 | 0.95750 | 0.95539 | 6.12800 | 6.10304 |
| 500,000 | 0.93149 | 0.93021 | 6.60034 | 6.56118 |
| 1,000,000 | 0.91628 | 0.91539 | 6.95535 | 6.90776 |

Thus the measured tail supports

\[
\boxed{
\mathrm{MSE}_N
=
\Theta(N^{-1}),
}
\]

\[
\boxed{
\overline{|d|}_N
=
\Theta(N^{-1}),
}
\]

and

\[
\boxed{
m_N
\approx
\frac12\log N.
}
\]

The ratio between mean output delta and MSE also tends to one, as required by

\[
|d|=\epsilon^2(1-\epsilon).
\]

---

## 4. Output-parameter tail

The norm of one actual output-parameter epoch update satisfies:

| \(N\) | \(N\|\Delta\theta_{\rm out}\|\) |
|---:|---:|
| 10,000 | 1.30273 |
| 20,000 | 1.23966 |
| 50,000 | 1.19804 |
| 100,000 | 1.18207 |
| 200,000 | 1.17310 |
| 500,000 | 1.16730 |
| 1,000,000 | 1.16558 |

Thus

\[
\boxed{
\|\Delta\theta_{\rm out}\|
=
\Theta(N^{-1})
}
\]

over the measured tail.

Integration predicts logarithmic parameter growth. Consistently, the
non-bias output-weight norm rises from about \(14.96\) at \(10^4\) epochs to
\(19.94\) at \(10^6\).

---

## 5. Direct one-epoch selector action

The cumulative experiment can hide local structure, so the selector was also
measured one epoch at a time.

At checkpoint \(N\):

1. take the actual phase-0 branch state;
2. rotate its full three-copy transverse residual by
   \(\pm\delta\), with \(\delta=10^{-2}\);
3. apply exactly one ordinary XNOR epoch;
4. measure the outgoing phase difference;
5. define

\[
\rho_N^{(1)}
=
\frac{
\theta^+_{N+1}-\theta^-_{N+1}
}{
2\delta
},
\]

and

\[
\boxed{
a_N
=
-\frac13\log|\rho_N^{(1)}|.
}
\]

The result is:

| \(N\) | \(a_N\) | \(N\log N\,a_N\) |
|---:|---:|---:|
| 10,000 | \(1.34433\times10^{-6}\) | 0.123818 |
| 20,000 | \(6.01526\times10^{-7}\) | 0.119144 |
| 50,000 | \(2.15778\times10^{-7}\) | 0.116734 |
| 100,000 | \(1.00751\times10^{-7}\) | 0.115994 |
| 200,000 | \(4.73199\times10^{-8}\) | 0.115518 |
| 500,000 | \(1.75035\times10^{-8}\) | 0.114844 |
| 1,000,000 | \(8.26176\times10^{-9}\) | 0.114140 |

Over two decades,

\[
\boxed{
N\log N\,a_N
}
\]

is nearly constant.

Thus the actual local selector obeys

\[
\boxed{
a_N
\approx
\frac{C_s}{N\log N},
\qquad
C_s\approx0.11\text{--}0.12
}
\]

over the measured range.

---

## 6. Summation gives the observed \(\log\log N\)

If

\[
a_N
\sim
\frac{C_s}{N\log N},
\]

then

\[
\sum_{n\le N}a_n
\sim
C_s\log\log N.
\]

Therefore the local measurement independently predicts

\[
\boxed{
\mathcal A_N
=
\Theta(\log\log N),
}
\]

which is exactly the class found by the previous cumulative experiment.

The two diagnostics use different finite-amplitude phase coordinates, so their
fitted coefficients need not coincide exactly. What matters here is that both
independently select the same non-summable asymptotic class.

---

## 7. Direct connection to the quadratic selector

The next check asks whether the local action is still generated by the
threefold quadratic term rather than by an unrelated late-time effect.

At each branch-ray checkpoint:

1. remove the three-copy residual while preserving its coarse mean state;
2. use the current branch residual channel as the input direction;
3. extract the one-epoch harmonics of the actual nonlinear map,

\[
z'
=
\lambda_N z
+
\nu_N\bar z^2
+
\cdots;
\]

4. restore the actual branch radius \(r_N\).

For a small quadratic phase reduction,

\[
\boxed{
a_N^{(2)}
\approx
\frac{\nu_N}{\lambda_N}r_N.
}
\]

Using a Fourier probe amplitude \(10^{-2}\), the extraction gives:

| \(N\) | \(r_N\) | \(\nu_N/\lambda_N\) | \(a_N^{(2)}\) | actual \(a_N\) | ratio |
|---:|---:|---:|---:|---:|---:|
| 10,000 | 2.90668 | \(5.943\times10^{-7}\) | \(1.727\times10^{-6}\) | \(1.344\times10^{-6}\) | 1.285 |
| 100,000 | 3.49767 | \(3.724\times10^{-8}\) | \(1.302\times10^{-7}\) | \(1.008\times10^{-7}\) | 1.293 |
| 1,000,000 | 3.97394 | \(2.676\times10^{-9}\) | \(1.063\times10^{-8}\) | \(8.262\times10^{-9}\) | 1.287 |

The quadratic truncation overpredicts the finite-radius local action by about
\(29\%\), but the ratio is remarkably stable over two decades.

More importantly,

\[
N\log N\,a_N^{(2)}
\]

changes only from approximately \(0.159\) to \(0.147\).

Thus the late selector is still the same quadratic threefold mechanism to
leading scaling order.

The mismatch is consistent with finite-radius higher-order corrections; the
actual branch radius is not infinitesimal.

---

## 8. Numerical extraction boundary

At late epochs the one-epoch quadratic coefficient is tiny.

With a Fourier probe amplitude \(10^{-4}\), the \(-2\) harmonic eventually
falls close to the floating-point subtraction floor and the extracted
coefficient becomes noisy.

Raising the probe to \(10^{-2}\) restores a stable signal.

This is a numerical issue, not evidence that the quadratic term disappears.

Probe-amplitude stability is checked separately before treating the late-time
coefficient itself as a precision constant.

---

## 9. What has now been verified

The following chain is directly supported by the actual unmodified XNOR
update:

\[
\boxed{
m_N
\sim
\frac12\log N
}
\]

\[
\Downarrow
\]

\[
\boxed{
\mathrm{MSE}_N,\ |d_N|
=
\Theta(N^{-1})
}
\]

\[
\Downarrow
\]

\[
\boxed{
\|\Delta\theta_{\rm out}\|
=
\Theta(N^{-1})
}
\]

while independently

\[
\boxed{
a_N
=
\Theta((N\log N)^{-1})
}
\]

and therefore

\[
\boxed{
\mathcal A_N
=
\Theta(\log\log N)
}
\]

over the measured tail.

The quadratic normal-form extraction tracks the same local selector class.

---

## 10. What is not yet proved

The finite-window data are strong, but the following theorem has **not** yet
been established:

\[
\boxed{
\lim_{N\to\infty}
N\log N\,a_N
=
C_s>0.
}
\]

To prove divergence of total selector action from the actual equations, one
still needs an analytic late-time estimate showing a positive lower bound of
the form

\[
a_N
\ge
\frac{c}{N\log N}
\]

for all sufficiently large \(N\), or an equivalent asymptotic expansion.

The remaining mathematical work is therefore no longer to guess the scaling.
It is to derive the measured scaling from the exact one-sample sigmoid SGD
map.

---

## 11. Reproduction

Run:

~~~bash
python examples/xnor_sgd_tail_scaling.py
python examples/xnor_selector_tail_normal_form.py
~~~

Both diagnostics use the ordinary network update without optimizer
modification.

The recorded runs were executed in GitHub Actions on Python 3.12 after the
full unit-test suite passed.
