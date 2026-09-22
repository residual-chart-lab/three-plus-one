# Axis generation from the 3+1 split

Status: research note.

This note separates three layers deliberately:

1. geometry that follows directly from the centered 3+1 construction,
2. an interpretation in terms of replaceability and historical originality,
3. a candidate dynamical extension for rotation and the next symmetry break.

The third layer is not yet established by the current deterministic XNOR model.

---

## 1. Established geometry: 3+1 creates a distinguished axis

For four hidden units, work in the zero-sum contrast space

[
V
=
left{
xinmathbb{R}^4:
x_1+x_2+x_3+x_4=0
ight}
cong mathbb{R}^3.
]

The centered 3+1 seed is proportional to

[
(-1,-1,-1,3).
]

Normalize it as

[
a_1
=
rac{1}{sqrt{12}}
(-1,-1,-1,3).
]

This vector is fixed by permutations of the first three coordinates. Therefore
the original permutation symmetry is reduced from

[
S_4
longrightarrow
S_3.
]

The 3+1 split does more than mark one unit as different: it selects the
one-dimensional subspace

[
A_1=operatorname{span}(a_1),
]

which is a distinguished axis inside the three-dimensional contrast space.

The transverse space is

[
P_1
=
A_1^perpcap V
=
left{
(u_1,u_2,u_3,0):
u_1+u_2+u_3=0
ight}
congmathbb{R}^2.
]

Thus the centered 3+1 construction yields, canonically,

[
oxed{
	ext{one axis}
;+;
	ext{one two-dimensional transverse plane}.
}
]

This is the first structural result of the present note.

### Three equivalent directions inside the transverse plane

The remaining three interchangeable units define three equivalent rays:

[
b_1
=
rac{1}{sqrt6}(2,-1,-1,0),
]

[
b_2
=
rac{1}{sqrt6}(-1,2,-1,0),
]

[
b_3
=
rac{1}{sqrt6}(-1,-1,2,0).
]

They satisfy

[
b_1+b_2+b_3=0,
]

and

[
langle b_i,b_jangle=-rac12
qquad(i
eq j),
]

so the three candidate directions are separated by (120^circ) in (P_1).

Geometrically, after the first 3+1 split has generated the axis (A_1), the
remaining three-copy sector already contains the minimal geometry needed for
a next selection.

---

## 2. Interpretation: copy, original, and the birth of a coordinate axis

The following is an interpretive hypothesis, not yet a theorem of the neural
network package.

Read

[
(0,0,0,1)
]

as follows:

- (0): a member of a replaceable copy class,
- (1): the first historically non-replaceable original.

Before the first (1) is established, the copies are interchangeable:

[
0_1sim0_2sim0_3.
]

When the first (1) is established, two descriptions become true at the same
event:

[
oxed{
	ext{the first }1	ext{ appears}
}
]

and

[
oxed{
	ext{replaceability is broken}.
}
]

No causal ordering between those two statements is assumed here. They are two
readings of the same transition.

The stronger observation is geometric:

[
oxed{
	ext{the }+1	ext{ does not merely add one more state; it creates a new axis}.
}
]

Once the axis exists, previously interchangeable copies can acquire positions,
distances, phases, or histories relative to it.

In this reading, originality is not introduced first as an intrinsic substance.
It is approached through the change it causes in the surrounding relation
structure.

This motivates the working sequence

[
oxed{
	ext{symmetry breaking}
ightarrow
	ext{axis generation}
ightarrow
	ext{transverse dynamics}
ightarrow
	ext{next persistent distinction}.
}
]

The last two arrows remain research questions.

---

## 3. A minimal transverse order parameter

Choose an orthonormal basis of (P_1) and identify the transverse plane with
the complex plane:

[
z=re^{i	heta}inmathbb C.
]

Here

- (r) measures the magnitude of departure from the residual three-copy
  manifold,
- (	heta) records which direction inside the residual threefold geometry is
  being explored.

A simple threefold-symmetric normal form is

[
dot z
=
mu z
-
eta |z|^2z
+
kappa overline{z}^{,2}.
]

In polar coordinates,

[
dot r
=
mu r
-
eta r^3
+
kappa r^2cos 3	heta,
]

[
dot	heta
=
-kappa rsin 3	heta.
]

The (overline z^{,2}) term is compatible with the three equivalent
directions in the transverse plane. It can select one of three persistent
branches.

This model describes

[
	ext{axis}
ightarrow
	ext{transverse differentiation}
ightarrow
	ext{three-way branch selection},
]

but by itself it does **not** produce sustained circulation around the axis.

That distinction matters.

---

## 4. Rotation requires an additional orienting mechanism

To model genuine circulation before locking, one can add an orienting term:

[
dot z
=
(mu+iOmega)z
-
eta |z|^2z
+
kappaoverline z^{,2}.
]

Then

[
dot r
=
mu r
-
eta r^3
+
kappa r^2cos3	heta,
]

[
dot	heta
=
Omega
-
kappa rsin3	heta.
]

For small (r), the (Omega) term can dominate and the phase circulates.
As (r) grows, the threefold term can become strong enough for phase locking
to occur when solutions of

[
Omega=kappa rsin3	heta
]

become available and stable.

This gives the candidate sequence

[
oxed{
	ext{axis generation}
ightarrow
	ext{rotation}
ightarrow
	ext{phase locking}
ightarrow
	ext{next persistent branch}.
}
]

However, (Omega
eq0) is not free: it explicitly introduces an orientation
that is absent from the fully reflection-symmetric (S_3) transverse problem.

Therefore the important research question is not merely whether this equation
can rotate. It can.

The question is:

> **What mechanism in the actual learning dynamics can generate the orienting
> term, or an equivalent higher-dimensional rotational effect?**

Possible sources to test include ordered updates, optimizer state, delay,
additional internal dimensions, stochastic forcing, or another history-bearing
degree of freedom.

No source is assumed at present.

---

## 5. Constraint from the current deterministic model

The existing deterministic 3+1 XNOR experiment preserves the residual
permutation symmetry of the first three units when they are initialized
identically.

Therefore, if the transverse component starts at

[
z=0,
]

exact deterministic symmetry keeps it there.

So the current package already establishes the first transition

[
S_4ightarrow S_3
]

and its associated axis, but it does **not** yet establish a spontaneous next
split

[
S_3ightarrow S_2
]

or a rotation around the generated axis.

This is useful, not a failure: it isolates the missing mechanism sharply.

The next experiment must probe the transverse sector rather than assume it.

---

## 6. Next experiment

Project a suitable centered network state onto

[
V=A_1oplus P_1.
]

Track

[
A(t)=langle x(t),a_1angle
]

for the axis component and

[
z(t)=x_{P_1}^{(1)}(t)+i,x_{P_1}^{(2)}(t)
]

for the transverse component.

Then perturb the residual three-copy sector by a controlled small transverse
seed and measure:

- whether (r(t)) decays, remains neutral, or grows,
- whether (	heta(t)) is stationary, drifts, or circulates,
- whether one of the three rays becomes persistently selected,
- whether the selected identity remains replaceable or becomes historically
  persistent under later updates.

Useful observables include the winding rate

[
W_T
=
rac{	heta(T)-	heta(0)}{2pi T},
]

and the threefold phase-lock statistic

[
Q_3(T)
=
rac1Tint_0^T e^{3i	heta(t)},dt.
]

A circulating regime should show nonzero winding over a finite interval.
A phase-locked regime should show persistent threefold order.

---

## 7. Current boundary

Established now:

[
oxed{
	ext{centered 3+1 split}
ightarrow
	ext{distinguished axis}
ightarrow
	ext{canonical two-dimensional transverse space}
}
]

and the transverse plane contains three equivalent candidate directions for a
subsequent persistent distinction.

Interpretive working hypothesis:

[
oxed{
	ext{replaceable copies}
ightarrow
	ext{first non-replaceable original}
ightarrow
	ext{new coordinate axis}.
}
]

Not yet established:

[
oxed{
	ext{axis}
ightarrow
	ext{rotation}
ightarrow
	ext{next symmetry breaking}.
}
]

That is the next target.
