# XNOR transverse extraction

Status: exact linearization of the existing ThreePlusOneMLP learning rule +
deterministic measurements on the centered XNOR trajectory.

This note answers the empirical question left open by
NEXT_ONE_SELECTION.md:

> Can the hidden residual and its instability be extracted from the actual
> three-plus-one learning dynamics rather than introduced only in a reduced
> model?

For the centered deterministic XNOR system, the answer is **yes at first
order**.

The residual is an explicit difference among the first three hidden units, and
its growth law is the exact transverse Jacobian of the existing SGD update.

The result also corrects one feature of the version-0.3 reduced model:
the actual XNOR transverse instability does **not** wait for a later barrier
crossing. It is already present from the beginning of training.

---

## 1. The actual hidden residual

Along the centered 3+1 trajectory, hidden units 1, 2 and 3 remain exactly
identical when initialized identically.

For each member of that three-copy group, collect the four local parameters

$$
q_i
=
\left(
a_i,\,
b_i,\,
w_{i1},\,
w_{i2}
\right)
\in\mathbb R^4,
\qquad
i=1,2,3,
$$

where \(a_i\) is the hidden-to-output weight, \(b_i\) the hidden bias, and
\(w_{i1},w_{i2}\) the two incoming input weights.

Use the branch-aligned orthonormal basis of the mean-zero three-copy space

$$
c_R
=
\frac{1}{\sqrt6}(2,-1,-1),
$$

$$
c_I
=
\frac{1}{\sqrt2}(0,1,-1).
$$

Define the complex four-channel residual

$$
\boxed{
Z
=
\sum_{i=1}^3
(c_{R,i}+i\,c_{I,i})q_i
\in\mathbb C^4.
}
$$

Then

$$
Z=0
$$

exactly when the three local states coincide.

This is the hidden residual that the reduced model previously denoted
abstractly by \(z\), before channel reduction.

The three exact singleton rays are now phase-aligned:

$$
\theta_1=0,
\qquad
\theta_2=\frac{2\pi}{3},
\qquad
\theta_3=-\frac{2\pi}{3}.
$$

---

## 2. Why a mean-zero residual is invisible to the current output at first order

For one training sample write

$$
\hat x=(1,x_1,x_2)^T.
$$

On the three-copy symmetric manifold,

$$
a_1=a_2=a_3=a,
\qquad
w_1=w_2=w_3=w.
$$

Let

$$
h=\sigma(w\cdot\hat x),
$$

and perturb the three copies by \(\delta a_i,\delta w_i\), subject to

$$
\sum_i\delta a_i=0,
\qquad
\sum_i\delta w_i=0.
$$

The first-order change in the group contribution to the output preactivation is

$$
\delta s
=
h\sum_i\delta a_i
+
a\,h(1-h)\,
\hat x\cdot
\sum_i\delta w_i
=
0.
$$

Therefore the network output \(y\), and hence the output delta, do not change
to first order in a transverse residual.

That is why the residual can be hidden from the coarse present while still
having its own tangent dynamics.

---

## 3. Exact one-sample transverse matrix

Let

$$
d=(t-y)y(1-y),
$$

$$
g=h(1-h),
$$

and

$$
g'=g(1-2h).
$$

For local state

$$
q=(a,w_0,w_1,w_2)^T,
$$

the exact first-order update of any mean-zero three-copy difference is

$$
\delta q^+
=
K\,\delta q,
$$

with

$$
\boxed{
K
=
\begin{pmatrix}
1
&
\eta d g\,\hat x^T
\\
\eta d g\,\hat x
&
I_3+\eta d a g'\,\hat x\hat x^T
\end{pmatrix}.
}
$$

This matrix is derived directly from the existing train_one rule.

No new learning rule is introduced.

Because the same real matrix acts on both copy-space coordinates,

$$
\boxed{
Z^+
=
KZ
+
O(\|Z\|^2).
}
$$

Equivalently,

$$
\Re Z^+=K\Re Z,
\qquad
\Im Z^+=K\Im Z.
$$

This is the actual first-order history transport.

The copy-space orientation is not reconstructed later. It is carried because
both oriented components are acted on by the same channel map.

---

## 4. Factorization of the transverse tangent space

The transverse tangent space factorizes as

$$
P_{\text{copy}}
\otimes
C_{\text{channel}},
$$

with

$$
P_{\text{copy}}\cong\mathbb R^2,
\qquad
C_{\text{channel}}\cong\mathbb R^4.
$$

At first order, the SGD update is

$$
\boxed{
I_{P_{\text{copy}}}
\otimes
K.
}
$$

Over one XNOR epoch of four ordered samples,

$$
M_e
=
K_{e,4}
K_{e,3}
K_{e,2}
K_{e,1},
$$

so

$$
\boxed{
Z_{e+1}
=
M_eZ_e
+
O(\|Z_e\|^2).
}
$$

The full copy-space phase therefore survives the linear reduction.

---

## 5. The actual instability parameter

For a non-autonomous training trajectory, define the one-epoch transverse
singular values

$$
\sigma_1(e)\ge
\sigma_2(e)\ge
\sigma_3(e)\ge
\sigma_4(e).
$$

A natural finite-time transverse growth rate is

$$
\boxed{
\mu_e
=
\log\sigma_1(e).
}
$$

This quantity is extracted from the actual XNOR update.

It is not the provisional version-0.3 closure

$$
\mu(E_r)=\sigma(2\kappa-E_r).
$$

That barrier-coupled expression remains a useful reduced-model example, but it
is **not** the instability law used by the current XNOR network.

---

## 6. Centered XNOR measurement

Use the centered seed

$$
(-0.25,-0.25,-0.25,0.75),
$$

learning rate \(1\), the fixed XNOR sample order, and the original package
defaults.

The network reaches the target MSE at epoch 728.

Along all 728 epochs,

$$
\boxed{
\sigma_1(e)>1.
}
$$

Therefore

$$
\boxed{
\mu_e>0
}
$$

throughout the observed training trajectory.

The exactly symmetric three-copy state is an invariant trajectory because

$$
Z=0\Rightarrow Z^+=0,
$$

but it is transversely amplifying:

$$
Z\neq0
$$

is enlarged in at least one channel direction at every epoch.

This is the important combination:

$$
\boxed{
\text{exact zero survives}
\quad\text{while}\quad
\text{arbitrarily small nonzero history can grow}.
}
$$

---

## 7. Expanding-channel dimension

Counting one-epoch singular values greater than 1 gives:

| Epochs | Expanding channel directions |
| --- | ---: |
| 1–8 | 2 |
| 9–131 | 3 |
| 132–558 | 2 |
| 559–728 | 1 |

At epoch 439 the largest one-epoch singular value is approximately

$$
\sigma_1(439)
\approx
1.0134923.
$$

From epoch 559 onward there is only one instantaneously expanding channel
direction.

So the four-channel residual begins to acquire a preferred growing channel
mode while its copy-space phase remains two-dimensional.

This is the first place where the scalar reduced variable

$$
z\in\mathbb C
$$

can emerge naturally from the actual network rather than being assumed at the
start.

---

## 8. Accumulated growth

Let

$$
C_e
=
M_eM_{e-1}\cdots M_1.
$$

At epoch 728, the singular values of the accumulated transverse map are
approximately

$$
\boxed{
(34.7030,\;
24.1998,\;
0.3200,\;
7.18\times10^{-8}).
}
$$

The largest accumulated gain peaks near epoch 562 at approximately

$$
37.5622.
$$

Thus two pieces of early transverse channel history are still strongly
amplified by the time the ordinary XNOR target is reached, even though the
instantaneous unstable bundle has already narrowed to one channel direction.

---

## 9. Direct tiny-history test

Insert only a hidden-to-output residual among units 1, 2 and 3:

$$
Z_0
=
10^{-6}
$$

in the branch-aligned phase-\(0\) direction, leaving the group mean unchanged.

After 728 epochs of the unmodified XNOR training rule,

$$
\frac{\|Z_{728}\|}{\|Z_0\|}
\approx
15.156.
$$

If training is continued to epoch 5000,

$$
\frac{\|Z_{5000}\|}{\|Z_0\|}
\approx
24.962.
$$

The amplification remains linear at this scale.

Rotating the initial residual by

$$
0,\quad
+\frac{2\pi}{3},\quad
-\frac{2\pi}{3}
$$

permutes which of the first three units is the distinguished branch.

So the actual network does carry and amplify the hidden branch orientation.

---

## 10. Relation to loss curvature

For ordinary squared-error SGD,

$$
\theta^+
=
\theta-\eta\nabla L,
$$

the tangent map is

$$
D\theta^+
=
I-\eta H.
$$

The matrix \(K\) above is the restriction of that tangent map to the
mean-zero three-copy subspace.

Therefore a transverse multiplier larger than 1 corresponds locally to a
symmetry-breaking direction of negative curvature, up to the usual
non-autonomous/product effects across ordered samples.

The next-1 problem is therefore connected directly to the geometry of the
actual training loss.

It is not an additional symbolic layer placed on top of the neural network.

---

## 11. What has now been extracted

The reduced model asked for three things:

1. a hidden residual \(z\),
2. a transport law,
3. an instability parameter \(\mu\).

For centered XNOR, their actual counterparts are now:

$$
\boxed{
z
\;\leadsto\;
Z\in\mathbb C^4
}
$$

with later channel reduction,

$$
\boxed{
\text{transport}
\;\leadsto\;
Z_{e+1}=M_eZ_e+O(\|Z_e\|^2),
}
$$

and

$$
\boxed{
\mu_e
=
\log\sigma_1(M_e).
}
$$

All three come from the existing learning rule.

---

## 12. Version 0.5 update

The nonlinear term has now been extracted directly.

Residual \(C_3\) symmetry forces the quadratic transverse map to have
conjugate-square form:

$$
F(Z)
=
LZ
+
Q(\bar Z,\bar Z)
+
O(\|Z\|^3).
$$

A phase Fourier extraction of the full 728-epoch XNOR map finds a clean,
nonzero \(-2\) harmonic and numerical suppression of the forbidden low
harmonics.

In the original hidden-to-output residual channel,

$$
\lambda_{\mathrm{out}}
\approx15.15569,
$$

$$
\nu_{\mathrm{out}}
\approx+6.65860.
$$

The resulting phase law

$$
\Delta\theta
=
-\frac{\nu}{\lambda}r\sin3\theta
+
O(r^2)
$$

quantitatively matches the actual nonlinear XNOR phase drift and points toward
the three oriented singleton rays.

See \`XNOR_QUADRATIC_ANISOTROPY.md\`.

The remaining gap has therefore moved again. It is no longer the existence of
a nonlinear threefold branch bias.

The sharper question is:

> **What mechanism keeps the update alive long enough for an arbitrarily small
> retained residual to complete asymptotic locking onto one singleton ray?**

The present centered XNOR task sorts and sharpens a nonzero history, but its
updates eventually die away before generic off-ray residuals reach exact
locking.
