# Next-one selection

Status: structural necessity + minimal equivariant selection model.

The previous notes establish

$$
\text{centered 3+1}
\rightarrow
\text{tetrahedral axis}
\rightarrow
\text{transverse plane}
\rightarrow
\text{dual-frame relative rotation}.
$$

The remaining question is sharper:

> **How can one of the three equivalent residual directions become the next
> historically persistent 1 without simply inserting an external label?**

The answer separates into two parts.

1. A deterministic exactly symmetric present cannot choose by itself.
2. A hidden historical residual can become visible when the symmetric branch
   state loses stability.

The first statement is structural. The second is modeled explicitly below.

---

## 1. A no-selection result for an exactly symmetric present

Identify the transverse plane with

$$
P_a\cong\mathbb C.
$$

Let

$$
\omega=e^{2\pi i/3}
$$

generate the residual \(C_3\) action

$$
z\mapsto\omega z.
$$

Suppose a deterministic branch vector field \(F\) is \(C_3\)-equivariant:

$$
F(\omega z)=\omega F(z).
$$

At the exactly symmetric state \(z=0\),

$$
F(0)=\omega F(0).
$$

The only vector in the transverse plane fixed by a non-trivial \(120^\circ\)
rotation is the zero vector. Therefore

$$
\boxed{
F(0)=0.
}
$$

So, for a unique deterministic flow,

$$
\boxed{
z(0)=0
\quad\Longrightarrow\quad
z(t)=0.
}
$$

This means an exactly symmetric **current configuration alone** cannot
endogenously choose one of three equivalent branches.

Something else must survive:

- a hidden historical residual,
- noise,
- a non-unique evolution rule,
- or another degree of freedom that transforms non-trivially under the
  residual symmetry.

The model below follows the historical-residual route.

---

## 2. Minimal \(C_3\)-equivariant branch field

Let

$$
z=re^{i\theta}
$$

be the unresolved next-branch variable.

The lowest-degree real-reflection-symmetric \(C_3\)-equivariant polynomial
field is

$$
\boxed{
\dot z
=
\mu z
+
\nu\bar z^2
-
\beta |z|^2z,
}
$$

with

$$
\nu>0,
\qquad
\beta>0.
$$

In polar coordinates,

$$
\dot r
=
\mu r
+
\nu r^2\cos3\theta
-
\beta r^3,
$$

and

$$
\dot\theta
=
-\nu r\sin3\theta.
$$

The three stable angular rays are

$$
\boxed{
\theta_k
=
\frac{2\pi k}{3},
\qquad
k=0,1,2.
}
$$

They are precisely the three residual tetrahedral directions.

At the origin, the linearization is

$$
\dot z=\mu z.
$$

Therefore

- \(\mu<0\): the unresolved symmetric branch state is linearly stable,
- \(\mu>0\): the symmetric branch state is unstable.

Once \(\mu>0\), an arbitrarily small nonzero residual can be amplified and
locked to one of the three rays.

But if the residual is exactly zero, the no-selection result still applies.

---

## 3. The selector is history, not a label

Write the small unresolved residual as

$$
h
=
\varepsilon e^{i\theta_h},
\qquad
0<\varepsilon\ll1.
$$

Before instability, this residual can be dynamically negligible and invisible
to a coarse observer.

Nevertheless,

$$
h\neq0
$$

contains information that the current symmetric quotient has discarded.

When the branch mode becomes unstable, the old residual is amplified.

Thus the next branch is not created from nothing:

$$
\boxed{
\text{hidden historical difference}
\rightarrow
\text{instability}
\rightarrow
\text{amplified branch difference}.
}
$$

The moment of branch locking converts a previously sub-threshold difference
into a persistent distinction.

This is the model's precise sense in which the next 1 is history-selected.

---

## 4. Coupling the residual to the dual-frame rotor

Let

$$
\phi
$$

be the relative phase of the dual tetrahedral frames and

$$
\ell=I_r\dot\phi
$$

the relative angular momentum.

Add weak dissipation:

$$
\dot\phi
=
\frac{\ell}{I_r},
$$

$$
\dot\ell
=
-3\kappa\sin3\phi
-
\gamma\dot\phi,
\qquad
\gamma>0.
$$

The relative rotor energy is

$$
E_r
=
\frac{\ell^2}{2I_r}
+
\kappa(1-\cos3\phi).
$$

Its derivative is exact:

$$
\boxed{
\dot E_r
=
-\gamma\dot\phi^2
\le0.
}
$$

So a trajectory that begins above the conservative rotation barrier can
eventually lose enough energy to be captured.

The exact barrier from the dual-frame model is

$$
E_c=2\kappa.
$$

---

## 5. Barrier-coupled branch instability

The simplest closure using the rotor's already existing scalar threshold is

$$
\boxed{
\mu(E_r)
=
\sigma(E_c-E_r),
\qquad
\sigma>0.
}
$$

With

$$
E_c=2\kappa,
$$

the branch state is stable while the rotor is above the barrier and becomes
unstable after the rotor energy falls below it.

This particular coupling is a **modeling closure**, not yet a theorem of the
original XNOR network.

Its value is that it introduces no new arbitrary switching time. The only
threshold used is the barrier already present in the relative-rotation model.

---

## 6. Transporting the hidden residual

While the relative frames rotate, the hidden residual should not be treated as
a frozen arrow in an unrelated coordinate system.

The minimal parity-respecting transport term is

$$
i\eta\dot\phi\,z,
$$

with real transport coefficient \(\eta\).

The coupled branch equation becomes

$$
\boxed{
\dot z
=
\left[
\mu(E_r)
+
i\eta\dot\phi
\right]z
+
\nu\bar z^2
-
\beta|z|^2z.
}
$$

This term has the desired mirror behavior:

$$
(\phi,\ell,z)
\mapsto
(-\phi,-\ell,\bar z)
$$

reverses the transported orientation.

It also preserves \(C_3\) equivariance.

The accumulated rotor history therefore changes the phase of the hidden
residual before the residual becomes macroscopically visible.

---

## 7. The full minimal selection system

The resulting reduced model is

$$
\boxed{
\begin{aligned}
\dot\phi
&=
\frac{\ell}{I_r},
\\
\dot\ell
&=
-3\kappa\sin3\phi
-
\gamma\frac{\ell}{I_r},
\\
E_r
&=
\frac{\ell^2}{2I_r}
+
\kappa(1-\cos3\phi),
\\
\mu
&=
\sigma(2\kappa-E_r),
\\
\dot z
&=
\left(
\mu
+
i\eta\frac{\ell}{I_r}
\right)z
+
\nu\bar z^2
-
\beta|z|^2z.
\end{aligned}
}
$$

The model separates three roles:

- \((\phi,\ell)\): carried dual-frame history,
- \(E_r\): scalar control of the rotation/capture regime,
- \(z\): hidden branch residual that can later become the next 1.

---

## 8. What the model does

With the reference parameters used by the executable implementation,

$$
I_r=0.5,
\quad
\kappa=1,
\quad
\gamma=0.05,
$$

$$
\sigma=0.5,
\quad
\eta=0.3,
\quad
\nu=0.4,
\quad
\beta=1,
$$

take the same visible rotor state

$$
\phi(0)=0,
\qquad
\ell(0)=1.8,
$$

but three \(C_3\)-related hidden residuals

$$
z_k(0)
=
10^{-4}e^{2\pi i k/3}.
$$

All three begin with the same rotor energy

$$
E_r(0)=3.24>2.
$$

The rotor dissipates through the barrier. The hidden residual is transported,
then amplified, and finally locks to one of the three stable branch rays.

The three \(C_3\)-related hidden histories produce the three \(C_3\)-related
branch outcomes.

By contrast, if

$$
z(0)=0
$$

exactly, then

$$
z(t)=0
$$

for the entire deterministic run, even after the rotor crosses the barrier.

So the extra historical degree of freedom is not cosmetic. It is required by
the symmetry.

---

## 9. The next 1

Once the branch variable locks to

$$
\theta_k=\frac{2\pi k}{3},
$$

the corresponding tetrahedral child axis is

$$
\boxed{
a'_k
=
-\frac13a
+
\frac{2\sqrt2}{3}
R_a(\theta_k)b_0.
}
$$

At that point the residual three-way interchangeability has been broken:

$$
S_3
\longrightarrow
S_2.
$$

The interpretation is

$$
\boxed{
\text{hidden replaceable difference}
\rightarrow
\text{history transport}
\rightarrow
\text{instability}
\rightarrow
\text{one persistent branch}
\rightarrow
\text{next 1}.
}
$$

The new 1 then supplies the next axis and the construction can recurse.

---

## 10. Why this is different from an argmax rule

A rule such as

> choose whichever candidate is currently largest

would merely rename an already visible asymmetry.

That is not what this model does.

Before the instability, the residual can be arbitrarily small and absent from
the coarse present.

The visible branch appears because the dynamics changes the status of that
old difference:

$$
\boxed{
\text{sub-threshold}
\longrightarrow
\text{unstable}
\longrightarrow
\text{macroscopically persistent}.
}
$$

So the branch event is a change in dynamical significance, not a post-hoc
classification.

---

## 11. What is structural and what is provisional

### Structural

- an exactly \(C_3\)-symmetric deterministic present cannot choose a branch by
  itself,
- the next-branch order parameter transforms as the two-dimensional \(C_3\)
  representation,
- the minimal branch field contains the symmetry-allowed
  \(\bar z^2\) anisotropy,
- three equivalent stable branch rays result,
- a retained nonzero residual can determine which basin is entered,
- once a branch is selected, the next tetrahedral axis is fixed.

### Provisional closure

- weak linear damping of the relative rotor,
- identifying the branch instability threshold with
  \(E_r=2\kappa\),
- the specific transport coefficient \(\eta\),
- the claim that the current XNOR network carries exactly this hidden residual.

Those points are now testable rather than implicit.

---

## 12. New sharp edge

The previous open problem was:

$$
\text{what selects the next 1?}
$$

The model now answers that at the minimal dynamical level:

$$
\boxed{
\text{a retained historical residual selects the basin when the symmetric
branch state becomes unstable}.
}
$$

The next empirical question is stronger:

> **Can the hidden residual \(z\), its transport, and the instability parameter
> \(\mu\) be extracted from the actual three-plus-one learning dynamics rather
> than introduced only in the reduced model?**

That is the next test.


---

## 13. Version 0.4 update: the XNOR residual and instability are now explicit

The abstract residual and instability from this note have now been extracted
from the actual centered XNOR learning rule.

For the first three hidden units define local states

$$
q_i=(a_i,b_i,w_{i1},w_{i2})\in\mathbb R^4,
$$

and branch-aligned copy-space basis vectors

$$
c_R=\frac1{\sqrt6}(2,-1,-1),
\qquad
c_I=\frac1{\sqrt2}(0,1,-1).
$$

The actual hidden residual is

$$
\boxed{
Z=
\sum_{i=1}^3
(c_{R,i}+i c_{I,i})q_i
\in\mathbb C^4.
}
$$

On the exact three-copy symmetric trajectory, the existing SGD rule gives

$$
\boxed{
Z_{e+1}
=
M_e Z_e
+
O(\|Z_e\|^2),
}
$$

where \(M_e\) is the exact four-channel transverse Jacobian of epoch \(e\).

Thus the actual XNOR counterpart of the reduced growth parameter is

$$
\boxed{
\mu_e=\log\sigma_1(M_e).
}
$$

For the centered XNOR run, \(\mu_e>0\) at every epoch through the ordinary
convergence point at epoch 728.

Therefore the barrier-coupled law

$$
\mu(E_r)=\sigma(2\kappa-E_r)
$$

should **not** be read as the XNOR mechanism. It remains one toy closure for
the dual-rotor model.

The actual XNOR system has a more striking structure:

$$
\boxed{
Z=0\text{ is exactly invariant, while every observed epoch has a transverse
expanding direction.}
}
$$

So exact symmetry survives only because the historical residual is exactly
zero. A nonzero residual can be amplified by the unmodified training rule.

See XNOR_TRANSVERSE_EXTRACTION.md for the derivation and measurements.

The remaining bridge to a fully endogenous next 1 is now narrower:
the nonlinear \(S_3\)-equivariant terms must be extracted and tested for true
three-basin locking.


---

## 14. Version 0.5 update: the branch anisotropy is also present in XNOR

The nonlinear threefold term is no longer only a reduced-model assumption.

Residual \(C_3\) symmetry forces the actual quadratic transverse map into

$$
\boxed{
F(Z)
=
LZ
+
Q(\bar Z,\bar Z)
+
O(\|Z\|^3).
}
$$

Direct phase-Fourier extraction from the centered-XNOR training course finds
the expected nonzero \(-2\) harmonic.

In the original hidden-to-output residual channel,

$$
\lambda_{\mathrm{out}}
\approx15.15569,
\qquad
\nu_{\mathrm{out}}
\approx+6.65860.
$$

The induced phase motion is

$$
\Delta\theta
=
-\frac{\nu}{\lambda}r\sin3\theta
+
O(r^2),
$$

and it points toward the three oriented singleton rays.

The full nonlinear network quantitatively matches this phase law at small
amplitude and shows three-sector angular contraction at finite amplitude.

So the reduced next-one chain now has direct XNOR counterparts for:

$$
\boxed{
\text{residual}
\rightarrow
\text{transport}
\rightarrow
\text{amplification}
\rightarrow
\text{threefold directional sorting}.
}
$$

The remaining limitation is persistence, not branch anisotropy.

Centered XNOR eventually converges and its updates become too small to drive a
generic off-ray residual all the way to exact asymptotic locking.

See XNOR_QUADRATIC_ANISOTROPY.md.
