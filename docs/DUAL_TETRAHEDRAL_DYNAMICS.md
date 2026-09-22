# Dual tetrahedral dynamics

Status: mathematical model + executable toy dynamics.

This note continues `AXIS_GENERATION.md`.  The goal is to make the next
step precise without confusing three different statements:

1. what follows exactly from the centered 3+1 geometry,
2. what follows exactly from a two-frame conservative rotor model,
3. what is still only a candidate mechanism for generating the next 1.

The central new object is **not** "second-order Markov memory".  The more
invariant object is an **oriented area form**.  A history pair, a velocity,
a momentum, or a second rotating frame are different ways of carrying that
orientation without collapsing it into one configuration snapshot.

---

## 1. The centered 3+1 directions already form a tetrahedron

In the zero-sum contrast space

[
V
=
left{
xinmathbb R^4:
sum_i x_i=0
ight}
congmathbb R^3,
]

define

[
v_i
=
rac{4e_i-mathbf 1}{sqrt{12}},
qquad
i=1,2,3,4.
]

Then

[
|v_i|=1,
]

and for (i
eq j),

[
langle v_i,v_jangle=-rac13.
]

So the four normalized centered singleton directions are the vertices of a
regular tetrahedron.

This is the geometric content hidden in the four possible centered 3+1
choices.

---

## 2. The first 1 generates an axis and a transverse plane

Choose one vertex as the first distinguished direction.  Write

[
a=v_4.
]

Then

[
V
=
operatorname{span}(a)
oplus
P_a,
]

where

[
P_a=a^perpcap V
congmathbb R^2.
]

The other three tetrahedral vertices decompose as

[
v_k
=
-rac13 a
+
rac{2sqrt2}{3}b_k,
qquad
k=1,2,3,
]

where

[
b_kin P_a,
qquad
|b_k|=1,
]

and

[
langle b_i,b_jangle=-rac12
qquad(i
eq j).
]

Thus the residual three-copy sector is an equilateral three-direction
geometry in a two-dimensional plane.

This makes 3+1 minimal in a precise sense.

For a centered ((n-1)+1) split,

[
dim V_n=n-1
]

and after the distinguished axis is removed,

[
dim P_n=n-2.
]

For 2+1, (P_n) is only one-dimensional: there is no continuous angle around
the new axis.

For 3+1,

[
oxed{dim P_4=2,}
]

so a genuine transverse phase first becomes possible.

---

## 3. Dual tetrahedral lift

Let (R_a(	heta)) denote rotation around the generated axis (a).

Define an upper tetrahedral frame

[
T_+(	heta_+)
=
left{
a,;
-rac13a
+
rac{2sqrt2}{3}
R_a(	heta_+)b_k
ight}_{k=1}^3
]

and an oppositely oriented lower frame

[
T_-(	heta_-)
=
left{
-a,;
rac13a
-
rac{2sqrt2}{3}
R_a(	heta_-)b_k
ight}_{k=1}^3.
]

When

[
	heta_+=	heta_-,
]

the two tetrahedra are exact central inversions:

[
T_-=-T_+.
]

The important extension is to allow

[
	heta_+
eq	heta_-.
]

The two frames now have independent rotations around one shared axis.

The fixed top/bottom inversion is part of the construction.  The dynamical
relative phase is therefore taken **after factoring out that fixed inversion**:

[
phi=	heta_+-	heta_-.
]

---

## 4. The universal object: oriented area

Once (a) orients the transverse plane (P_a), define

[
oxed{
omega_a(u,v)
=
acdot(u	imes v)
}
]

for (u,vin P_a).

This is the oriented area 2-form on the transverse plane.

It has the essential antisymmetry

[
omega_a(u,v)
=
-omega_a(v,u).
]

So reversing the order of two states reverses parity.

For a discrete trajectory,

[
mathcal A_t
=
omega_a(u_t,u_{t+1})
]

is the signed area spanned by two successive transverse states.

For a continuous trajectory (u(t)),

[
J(t)
=
omega_a(u,dot u)
]

is the infinitesimal oriented sweep.

If

[
u(t)
=
r
left(
cos	heta(t)e_1
+
sin	heta(t)e_2
ight),
]

then

[
oxed{
J=r^2dot	heta.
}
]

So the sign of the oriented area sweep is exactly the local rotation
orientation.

### Why this is not fundamentally a Markov-order claim

A configuration-only state (u_t) cannot determine an oriented sweep by
itself:

[
omega_a(u_t,u_t)=0.
]

A second time slice (u_{t-1}), a tangent (dot u_t), a momentum, or a
second frame can restore the missing orientation.

But nothing requires the final theory to be non-Markovian.  The dynamics may
be first-order Markov on a sufficiently rich phase space.

The invariant content is:

> **do not close the state description in a way that quotients out the
> oriented area/parity needed by the motion.**

---

## 5. Unlabeled relative order of two tetrahedral frames

Each base triangle is unchanged, up to relabeling, under

[
	hetamapsto	heta+rac{2pi}{3}.
]

Therefore the raw phase (phi) contains label gauge.

The lowest unlabeled relative order parameter is

[
oxed{
q
=
e^{3iphi}.
}
]

Write

[
C=Re q=cos3phi,
]

[
Pi=Im q=sin3phi.
]

Then:

- (C) is even under frame exchange,
- (Pi) is odd under frame exchange,
- both are invariant under independent (2pi/3) relabelings of either
  triangular base.

Thus (Pi) is a natural tetrahedral parity observable.

It is important to distinguish this static parity observable from the
dynamical chirality (J).  A rotating trajectory can pass through
(Pi=0) while retaining a definite sign of (J).

---

## 6. Minimal conservative relative-rotation model

Give the two frames inertias

[
I_+>0,
qquad
I_->0,
]

angles (	heta_+,	heta_-), and conjugate momenta (p_+,p_-).

The lowest interaction compatible with the unlabeled threefold symmetry is

[
V(phi)
=
kappa
left(
1-cos3phi
ight),
qquad
kappage0.
]

Take the Hamiltonian

[
H
=
rac{p_+^2}{2I_+}
+
rac{p_-^2}{2I_-}
+
kappa
left(
1-cos3phi
ight).
]

Hamilton's equations give

[
dot	heta_+
=
rac{p_+}{I_+},
qquad
dot	heta_-
=
rac{p_-}{I_-},
]

[
dot p_+
=
-3kappasin3phi,
]

[
dot p_-
=
+3kappasin3phi.
]

Immediately,

[
oxed{
P=p_++p_-
}
]

is conserved.

So the absolute common rotation separates from the relative rotation.

---

## 7. Relative reduction and the rotation threshold

Define the reduced inertia

[
I_r
=
rac{I_+I_-}{I_++I_-},
]

and

[
ell
=
I_rdotphi.
]

The relative energy is

[
oxed{
E_r
=
rac{ell^2}{2I_r}
+
kappa
left(
1-cos3phi
ight).
}
]

The threefold potential has barrier height

[
V_{max}=2kappa.
]

Therefore the conservative model has three exact regimes:

### Libration

[
E_r<2kappa.
]

The relative phase remains trapped in one well.  The relative angular momentum
reaches zero at turning points and reverses sign.

### Separatrix

[
E_r=2kappa.
]

The trajectory lies on the boundary between trapped and circulating motion.

### Persistent relative rotation

[
oxed{
E_r>2kappa.
}
]

The kinetic term can never vanish because

[
E_r-V(phi)>0
]

for every phase.

Therefore (ell) cannot change sign continuously, and (phi) winds
indefinitely in one direction.

This produces sustained rotation without inserting a one-way angular drift
term by hand.

For the symmetric case

[
I_+=I_-=1,
]

with initial state

[
phi(0)=0,
qquad
p_+(0)=p,
qquad
p_-(0)=-p,
]

one has

[
E_r=p^2.
]

So the exact rotation threshold is

[
oxed{
|p|>sqrt{2kappa}.
}
]

---

## 8. What the dual frame contributes

A single generated axis plus one transverse ray contains a direction but not a
persistent handed relational structure.

The dual construction supplies two independently evolving frames.

The relevant quantity is not "two tetrahedra" as an object count.  It is the
relative transformation between them.

If (R_+) and (R_-) are the two frame rotations, define

[
oxed{
Q
=
R_-^{-1}R_+.
}
]

For the shared-axis model, (Q) reduces to the relative phase (phi).

In a future non-coaxial extension, (Qin SO(3)) remains meaningful even when
a single scalar phase no longer does.

This is the natural route from the present planar transverse dynamics to a
full moving-frame model.

---

## 9. Exact geometry of a possible next 1

The current model does **not** yet derive the event that chooses the next
distinguished member.

But once a branch (kin{1,2,3}) is selected at phase (	heta_*), the
next axis is already fixed by tetrahedral geometry:

[
oxed{
a'_k
=
-rac13a
+
rac{2sqrt2}{3}
R_a(	heta_*)b_k.
}
]

It is unit length and satisfies

[
acdot a'_k=-rac13.
]

Thus every child axis leaves its parent at the fixed tetrahedral angle

[
oxed{
alpha_T
=
arccosleft(-rac13ight)
approx109.47^circ.
}
]

So the geometry of the next axis is solved.

What is not solved yet is the **selection law**:

> what dynamical event turns one of the three equivalent candidate directions
> into the next historically persistent 1?

This should not be inserted by hand and is kept as the next open problem.

---

## 10. Recursive spring extension

Suppose a branch event has produced an axis (a_n) with transverse basis
(e_{n,1},e_{n,2}).

A local trajectory can be written

[
X_n(s)
=
c_n
+
h_n(s)a_n
+
r_n
left(
cos	heta_n(s)e_{n,1}
+
sin	heta_n(s)e_{n,2}
ight).
]

If

[
h_n(s)=v_ns,
qquad
	heta_n(s)=omega_ns,
]

this is a helix around (a_n).

At a selected event (s=s_*), choose one tetrahedral child axis (a_{n+1}),
set

[
c_{n+1}=X_n(s_*),
]

construct its new transverse plane, and repeat.

If the dimensionless generation law is reused and the scales obey

[
r_{n+1}=lambda r_n,
qquad
v_{n+1}=lambda v_n,
qquad
0<lambda<1,
]

then the resulting geometry is self-similar by construction:

[
oxed{
	ext{helix}
ightarrow
	ext{tetrahedral branch}
ightarrow
	ext{smaller helix}
ightarrow
cdots
}
]

This gives a mathematically explicit route to a multiscale spring/tree
geometry.

It is an extension of the current model, not yet an empirical result of the
XNOR network.

---

## 11. Executable checks

The package now includes:

- `threeplusone.geometry.centered_contrast_vertices`
- `threeplusone.geometry.tetrahedron_vertices`
- `threeplusone.geometry.dual_tetrahedra`
- `threeplusone.geometry.oriented_area`
- `threeplusone.geometry.tetrahedral_relative_order`
- `threeplusone.geometry.child_axes`
- `threeplusone.dynamics.DualRotorState`
- `threeplusone.dynamics.DualRotorParams`
- `threeplusone.dynamics.simulate_dual_rotor`

The regression tests check:

1. exact regular-tetrahedron inner products,
2. central inversion of the dual frames,
3. (C_3) gauge invariance of the relative order parameter,
4. odd parity under frame exchange,
5. the tetrahedral child angle,
6. momentum conservation of the symplectic rotor integrator,
7. bounded relative-energy error,
8. libration below the barrier,
9. sustained winding above the barrier.

---

## 12. Current boundary

Established by geometry:

[
oxed{
	ext{centered 3+1}
ightarrow
	ext{regular tetrahedron}
ightarrow
	ext{axis}
ightarrow
	ext{two-dimensional transverse plane}.
}
]

Established by the dual-frame model:

[
oxed{
	ext{dual frames}
ightarrow
	ext{oriented area/parity}
ightarrow
	ext{relative angular momentum}
ightarrow
	ext{persistent rotation above an exact threshold}.
}
]

Established as an exact conditional branch geometry:

[
oxed{
	ext{selected branch}
ightarrow
	ext{next tetrahedral axis}.
}
]

Still open:

[
oxed{
	ext{what endogenous event selects the next 1?}
}
]

That is now the sharp edge of the model.
