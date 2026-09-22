# XNOR quadratic anisotropy

Status: symmetry derivation + direct extraction from the existing centered-XNOR
training map.

Version 0.4 extracted the actual hidden residual

$$
Z\in\mathbb C^4
$$

and its exact linear transport.

The remaining question was whether the original network itself contains the
nonlinear threefold term that the reduced next-one model wrote as

$$
\nu\bar z^2.
$$

It does.

The result is strongest when stated in two layers:

1. symmetry forces the quadratic transverse term to have conjugate-square
   form,
2. direct Fourier extraction from the actual XNOR training map gives a
   nonzero coefficient and the expected threefold phase drift.

---

## 1. Why the quadratic term must be a conjugate square

Let

$$
\omega=e^{2\pi i/3}
$$

generate cyclic permutation of the three-copy sector.

In the branch-aligned complex coordinate,

$$
Z\mapsto\omega Z.
$$

The nonlinear transverse map \(F\) must satisfy

$$
F(\omega Z)=\omega F(Z).
$$

At quadratic order, the possible copy-space weights are

$$
ZZ\mapsto\omega^2 ZZ,
$$

$$
Z\bar Z\mapsto Z\bar Z,
$$

and

$$
\bar Z\bar Z
\mapsto
\bar\omega^2\bar Z\bar Z
=
\omega\bar Z\bar Z.
$$

Only the last transforms like the output \(Z\).

Therefore the second-order transverse map has the form

$$
\boxed{
F(Z)
=
LZ
+
Q(\bar Z,\bar Z)
+
O(\|Z\|^3),
}
$$

where

$$
Q:
\operatorname{Sym}^2(\mathbb R^4)
\rightarrow
\mathbb R^4
$$

is a real symmetric bilinear map in parameter-channel space.

So the reduced-model term

$$
\nu\bar z^2
$$

was not an arbitrary decorative choice.

It is the unique quadratic copy-space harmonic allowed by the residual
threefold symmetry.

Reflection of the three-copy group acts as complex conjugation, so the
quadratic channel tensor can be taken real in the chosen basis.

---

## 2. Fourier extraction

Seed a real channel direction \(v\in\mathbb R^4\) with complex copy-space
phase:

$$
Z_0
=
\varepsilon e^{i\theta}v.
$$

After a fixed training course, project the residual onto a real output channel
direction \(u\):

$$
y(\theta)
=
u^T Z_{\mathrm{out}}(\theta).
$$

The symmetry expansion is

$$
\boxed{
y(\theta)
=
\lambda\varepsilon e^{i\theta}
+
\nu\varepsilon^2e^{-2i\theta}
+
O(\varepsilon^3).
}
$$

Therefore the coefficients are separated directly by angular Fourier modes:

$$
\lambda
=
\frac{1}{\varepsilon}
\frac{1}{2\pi}
\int_0^{2\pi}
y(\theta)e^{-i\theta}\,d\theta,
$$

$$
\nu
=
\frac{1}{\varepsilon^2}
\frac{1}{2\pi}
\int_0^{2\pi}
y(\theta)e^{2i\theta}\,d\theta.
$$

The executable code uses a 12-point phase sum, which is sufficient to separate
these low harmonics cleanly.

---

## 3. Dominant 728-epoch channel

Let

$$
C_{728}
=
M_{728}\cdots M_1
$$

be the accumulated linear transverse map.

Choose its dominant right singular direction \(v_1\) and corresponding left
direction \(u_1\), with a fixed deterministic sign convention.

Using

$$
\varepsilon=10^{-4},
$$

the actual nonlinear 728-epoch XNOR map gives

$$
\boxed{
\lambda_1
\approx
34.70306,
}
$$

and

$$
\boxed{
\nu_1
\approx
-87.21614.
}
$$

The imaginary parts are numerical zero at the extraction precision.

At the same amplitude, the measured projected harmonic magnitudes are roughly

$$
|c_{+1}|
\approx
3.4703\times10^{-3},
$$

$$
|c_{-2}|
\approx
8.7216\times10^{-7},
$$

while the forbidden low harmonics

$$
-1,\;0,\;+2,\;+3
$$

are at numerical roundoff, around \(10^{-15}\).

So the \(-2\) harmonic is not a generic nonlinear leakage.

It is exactly the threefold anisotropy predicted by the symmetry.

The sign of \(\nu\) depends on the orientation convention of the reduced
channel coordinate. Its nonzero magnitude and harmonic type are the invariant
facts.

---

## 4. The original hidden-to-output channel

There is also a more physically direct probe.

Use the original hidden-to-output residual channel

$$
v_{\mathrm{out}}
=
(1,0,0,0).
$$

Project onto its normalized linear response

$$
u_{\mathrm{out}}
=
\frac{C_{728}v_{\mathrm{out}}}
{\|C_{728}v_{\mathrm{out}}\|}.
$$

Then the actual training map gives

$$
\boxed{
\lambda_{\mathrm{out}}
\approx
15.15569,
}
$$

and

$$
\boxed{
\nu_{\mathrm{out}}
\approx
+6.65860.
}
$$

This sign convention is aligned with the original positive singleton seed.

For small amplitude,

$$
y
=
\lambda r e^{i\theta}
+
\nu r^2e^{-2i\theta}
+
O(r^3).
$$

Factor out the linear term:

$$
y
=
\lambda r e^{i\theta}
\left[
1+
\frac{\nu}{\lambda}
r e^{-3i\theta}
+
O(r^2)
\right].
$$

Therefore the phase shift is

$$
\boxed{
\Delta\theta
=
-\frac{\nu}{\lambda}
r\sin3\theta
+
O(r^2).
}
$$

For

$$
r=0.01,
\qquad
\theta=\frac{\pi}{6},
$$

this predicts

$$
\theta_{\mathrm{out}}
\approx
0.5192053.
$$

The full nonlinear XNOR training run gives

$$
\boxed{
\theta_{\mathrm{out}}
\approx
0.5192082.
}
$$

The difference is about

$$
2.9\times10^{-6}\text{ rad}.
$$

So the extracted \(\bar z^2\) coefficient quantitatively predicts the actual
nonlinear phase motion.

---

## 5. Threefold angular attraction

For positive \(\nu_{\mathrm{out}}\), the small-amplitude phase law

$$
\dot{\theta}_{\mathrm{effective}}
\propto
-\sin3\theta
$$

points toward the oriented singleton rays

$$
\boxed{
0,\quad
+\frac{2\pi}{3},\quad
-\frac{2\pi}{3}.
}
$$

The separating reflection axes are

$$
\frac{\pi}{3},
\quad
\pi,
\quad
-\frac{\pi}{3}.
$$

A direct phase sweep of the full 728-epoch XNOR map confirms this angular
contraction in the original output-weight residual channel.

For 72 phase samples placed away from the exact reflection boundaries:

- at input amplitude \(0.01\), every sampled phase ends closer to its nearest
  oriented singleton ray,
- at amplitude \(0.05\), the same is true,
- at amplitude \(0.1\), the same is true,
- at amplitude \(0.2\), the same is true.

For example,

$$
\frac{\pi}{6}
\longmapsto
0.4829
$$

at amplitude \(0.1\), moving toward the phase-0 singleton ray, while

$$
\frac{\pi}{2}
\longmapsto
1.6115
$$

moves toward the \(2\pi/3\) singleton ray.

Thus the actual XNOR nonlinearity does not merely amplify a historical
residual.

It also contains a genuine threefold directional bias that sorts residual
phases into three symmetry-related sectors.

---

## 6. What this means for the next 1

The actual network now supplies all of the local ingredients that were
previously separated across the reduced model:

$$
\boxed{
\text{hidden residual}
\rightarrow
\text{linear transport}
\rightarrow
\text{transverse amplification}
\rightarrow
\text{quadratic threefold anisotropy}.
}
$$

The last term supplies the branch identity.

In the original output-weight residual channel,

$$
\nu_{\mathrm{out}}>0
$$

means the three oriented singleton rays are the locally attracting phase
directions.

So the network contains an endogenous answer to

> which of the three residual identities does a nonzero history tend toward?

The answer is encoded in the phase of the retained residual and sharpened by
the actual nonlinear learning map.

---

## 7. But finite-time XNOR does not create history from exact zero

The no-selection result remains intact.

If

$$
Z_0=0,
$$

then exact deterministic symmetry gives

$$
Z_e=0
$$

for every epoch.

The quadratic anisotropy does not manufacture a branch from zero.

It sorts and sharpens a **nonzero** historical residual.

This distinction remains essential:

$$
\boxed{
\text{anisotropy selects among histories;}
\quad
\text{it does not create history from nothing}.
}
$$

---

## 8. Nor does the present XNOR task complete exact asymptotic locking

Another boundary should remain explicit.

The 728-epoch course produces measurable angular contraction, but ordinary
XNOR learning eventually makes its updates small.

For a \(0.01\) output-weight residual at initial phase \(\pi/6\),

$$
\theta_{728}
\approx0.51921,
$$

$$
\theta_{5000}
\approx0.51600,
$$

and

$$
\theta_{10000}
\approx0.51533.
$$

The motion slows as the task converges.

So the current small XNOR system demonstrates:

- hidden-history transport,
- transverse growth,
- the correct quadratic \(C_3\) anisotropy,
- three-sector angular attraction,

but not complete finite-task collapse onto an exact singleton ray from a
generic off-ray initial phase.

In dynamical language, the branch basin is already visible before the exact
attractor is reached.

A separate persistence mechanism or continued update source would be required
for full asymptotic locking.

---

## 9. Current boundary

The previous sharp edge was:

$$
\text{does the actual network contain the }\bar z^2\text{ term?}
$$

That question is now answered:

$$
\boxed{\text{yes}.}
$$

The next sharper problem is no longer branch geometry or branch anisotropy.

It is:

> **What mechanism keeps the update alive long enough for a tiny retained
> residual to become a fully persistent next 1, rather than merely an
> amplified and directionally sorted residual?**

That is now the remaining dynamical gap.
