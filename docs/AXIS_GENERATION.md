# Axis generation from the 3+1 split

Status: established geometric step + interpretive working hypothesis.

This note records the first geometric layer of the project. The later
dual-frame rotation model is developed in
\`docs/DUAL_TETRAHEDRAL_DYNAMICS.md\`.

---

## 1. Centered 3+1 creates a distinguished axis

For four hidden units, work in the zero-sum contrast space

$$
V
=
\left\{
x\in\mathbb R^4:
x_1+x_2+x_3+x_4=0
\right\}
\cong\mathbb R^3.
$$

The centered 3+1 direction is proportional to

$$
(-1,-1,-1,3).
$$

Normalize it as

$$
a_1
=
\frac{1}{\sqrt{12}}
(-1,-1,-1,3).
$$

This vector is fixed by permutations of the first three coordinates, so the
initial permutation symmetry is reduced from

$$
S_4
\longrightarrow
S_3.
$$

The split therefore does more than mark one unit as different. It selects the
one-dimensional subspace

$$
A_1=\operatorname{span}(a_1),
$$

a distinguished axis inside the three-dimensional contrast space.

---

## 2. The transverse plane

The orthogonal complement of the axis inside \(V\) is

$$
P_1
=
A_1^\perp\cap V
=
\left\{
(u_1,u_2,u_3,0):
u_1+u_2+u_3=0
\right\}
\cong\mathbb R^2.
$$

Thus the centered 3+1 construction gives, canonically,

$$
\boxed{
\text{one axis}
+
\text{one two-dimensional transverse plane}.
}
$$

The remaining three interchangeable directions can be represented by

$$
b_1
=
\frac{1}{\sqrt6}(2,-1,-1,0),
$$

$$
b_2
=
\frac{1}{\sqrt6}(-1,2,-1,0),
$$

$$
b_3
=
\frac{1}{\sqrt6}(-1,-1,2,0).
$$

They satisfy

$$
b_1+b_2+b_3=0,
$$

and

$$
\langle b_i,b_j\rangle=-\frac12
\qquad(i\neq j),
$$

so the three residual directions are separated by \(120^\circ\) in \(P_1\).

This is why 3+1 is the first centered singleton split that leaves a genuine
two-dimensional phase plane after the new axis is generated.

---

## 3. Copy/original interpretation

The following remains an interpretation rather than a theorem of the neural
network package.

Read

$$
(0,0,0,1)
$$

as:

- \(0\): a member of a replaceable copy class,
- \(1\): the first historically non-replaceable original.

Before the first \(1\) is established,

$$
0_1\sim0_2\sim0_3.
$$

At the transition, two descriptions become true at once:

$$
\boxed{
\text{the first 1 appears}
}
$$

and

$$
\boxed{
\text{replaceability is broken}.
}
$$

No causal priority between those statements is assumed. They are two readings
of the same event.

The geometric strengthening is:

$$
\boxed{
\text{the }+1\text{ does not merely add one more state; it creates a new axis}.
}
$$

Once the axis exists, previously interchangeable copies can acquire positions,
phases, distances, and histories relative to it.

---

## 4. What changed after this note

The first version of this note asked whether an additional orienting term had
to be inserted to make the transverse plane rotate.

The subsequent dual-frame construction sharpened that question.

The key object is the oriented area form

$$
\omega_a(u,v)=a\cdot(u\times v),
$$

not a manually imposed angular drift and not "second-order memory" by itself.

A second time slice, a tangent, a momentum, or an independently rotating
second tetrahedral frame can all carry the orientation that a
configuration-only snapshot discards.

The resulting model now separates:

$$
\boxed{
\text{3+1}
\rightarrow
\text{axis generation}
\rightarrow
\text{transverse plane}
}
$$

from the next layer

$$
\boxed{
\text{dual frames}
\rightarrow
\text{oriented area/parity}
\rightarrow
\text{persistent relative rotation}.
}
$$

See \`docs/DUAL_TETRAHEDRAL_DYNAMICS.md\` for the full construction.

---

## 5. Current boundary

Established geometrically:

$$
\boxed{
\text{centered 3+1 split}
\rightarrow
\text{distinguished axis}
\rightarrow
\text{canonical two-dimensional transverse space}.
}
$$

Interpretive working hypothesis:

$$
\boxed{
\text{replaceable copies}
\rightarrow
\text{first non-replaceable original}
\rightarrow
\text{new coordinate axis}.
}
$$

The selection problem has now moved to the next layer.

A deterministic exactly symmetric current state cannot select one of the three
residual directions by itself. The current 0.3 reduced model therefore keeps a
small hidden historical residual and amplifies it when the residual branch
state becomes unstable.

See \`docs/NEXT_ONE_SELECTION.md\`.

The remaining empirical question is whether that hidden residual and its
instability can be read directly from the original learning dynamics.
