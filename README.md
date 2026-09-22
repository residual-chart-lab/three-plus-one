# three-plus-one
## The Three Plus One Network

A small experimental framework that began with one question:

> What happens when a perfectly symmetric hidden population receives one
> deliberately asymmetric seed?

The project started from a tiny neural-network observation and now keeps four
connected layers in one repository:

1. a reproducible 3+1 symmetry-breaking experiment,
2. a geometric/dynamical model of what the 3+1 split creates,
3. a history-seeded model for how one residual branch can become the next 1,
4. an exact transverse linearization of the original XNOR learning dynamics.

This project is **not** a port of the 1996 AMOS program that inspired it.
It is a new implementation of the underlying phenomenon.

---

## Core construction

All hidden units begin with the same incoming weights:

$$
B_i^{(0)} = b_0.
$$

The outgoing hidden-to-output weights begin as

$$
a_i^{(0)} = a_0 + \varepsilon s_i.
$$

For the default four-hidden-unit case,

$$
s=(0,0,0,1),
$$

so

$$
a^{(0)}
=
\begin{bmatrix}
a_0\\
a_0\\
a_0\\
a_0+\varepsilon
\end{bmatrix}.
$$

That is the **3+1 seed**.

More generally, with \(n\) hidden units this is an \((n-1)+1\) construction.

The important control is

$$
\varepsilon=0,
$$

where all hidden units are exactly symmetric.

---

## Why this can matter

With deterministic data order and identical hidden units, standard
backpropagation preserves symmetry when the outgoing weights are identical.

For one output unit, a hidden delta contains the factor

$$
\delta_i^{(h)}
=
h_i(1-h_i)\,\delta^{(o)}\,a_i.
$$

If \(h_i=h_j\) and \(a_i=a_j\), the two hidden units receive the same update.

But if

$$
a_i-a_j
=
\varepsilon(s_i-s_j),
$$

then, whenever the remaining factors are nonzero,

$$
\delta_i^{(h)}-\delta_j^{(h)}
=
h(1-h)\,\delta^{(o)}\,
\varepsilon(s_i-s_j).
$$

A tiny outgoing-weight asymmetry therefore creates an immediate difference in
the hidden updates. Whether that difference is useful is task-dependent; the
framework is designed to measure it rather than assume it.

---

## XNOR demo

Install locally:

~~~bash
python -m pip install -e .
~~~

Run:

~~~bash
three-plus-one demo
~~~

Default configuration:

- 2 inputs
- 4 hidden units
- 1 output
- identical incoming hidden weights
- sigmoid activation
- standard backpropagation
- explicit seed <code>s=(0,0,0,1)</code>
- <code>epsilon=1</code>

On the deterministic XNOR demo, the default 3+1 run converges while the
perfectly symmetric control does not reach the same error target within the
same budget.

Compare:

~~~bash
three-plus-one demo --epsilon 0
three-plus-one demo --epsilon 1
~~~

Sweep the seed magnitude:

~~~bash
three-plus-one sweep
~~~

---

## Centered 3+1 control

The default singleton seed changes both symmetry and the sum of the outgoing
weights.

To isolate symmetry breaking more cleanly, use the centered seed

$$
s_c
=
\left(
-\frac1n,
\dots,
-\frac1n,
1-\frac1n
\right),
$$

for which

$$
\sum_i s_{c,i}=0.
$$

At the initial symmetric hidden state, all hidden activations are equal, so a
zero-sum seed preserves the initial output preactivation while still making
one hidden unit dynamically distinct from the others.

For four hidden units,

$$
s_c=(-0.25,-0.25,-0.25,0.75).
$$

Run:

~~~bash
three-plus-one demo --epsilon 1 --centered
three-plus-one sweep --centered 0 0.01 0.05 0.1 0.2 0.5 1 2
~~~

In the deterministic XNOR setup, the centered 3+1 seed also reaches the target
MSE while the exactly symmetric control does not. This removes the simple
explanation that the effect comes only from shifting the network's initial
output.

---

## Generalized seeds

The code accepts arbitrary seed patterns.

~~~python
from threeplusone import ThreePlusOneMLP

# 3+1
a = ThreePlusOneMLP(
    hidden=4,
    epsilon=1.0,
    seed_pattern=[0, 0, 0, 1],
)

# 2+2
b = ThreePlusOneMLP(
    hidden=4,
    epsilon=1.0,
    seed_pattern=[0, 0, 1, 1],
)

# graded asymmetry
c = ThreePlusOneMLP(
    hidden=4,
    epsilon=0.25,
    seed_pattern=[0, 1, 2, 3],
)
~~~

The broader family is

$$
a^{(0)}
=
a_0\mathbf 1
+
\varepsilon s.
$$

---

## Axis generation from centered 3+1

For the four possible centered singleton directions, define

$$
v_i
=
\frac{4e_i-\mathbf 1}{\sqrt{12}}.
$$

They satisfy

$$
\|v_i\|=1,
$$

and

$$
\langle v_i,v_j\rangle=-\frac13
\qquad(i\neq j).
$$

So the four possible centered 3+1 directions form a regular tetrahedron in the
three-dimensional zero-sum contrast space.

Choosing one 1 creates a distinguished axis. After that axis is removed, the
remaining three-copy sector is a canonical two-dimensional transverse plane.

In compressed form:

$$
\boxed{
\text{centered 3+1}
\rightarrow
\text{regular tetrahedron}
\rightarrow
\text{axis}
\rightarrow
\text{2D transverse plane}.
}
$$

See <code>docs/AXIS_GENERATION.md</code>.

---

## Dual tetrahedral dynamics

Version 0.2 adds an explicit two-frame model.

Two oppositely oriented regular tetrahedra share the generated axis and rotate
independently around it.

The universal transverse object is the oriented area form

$$
\omega_a(u,v)
=
a\cdot(u\times v).
$$

For a rotating transverse vector,

$$
u(t)
=
r
\left(
\cos\theta(t)e_1
+
\sin\theta(t)e_2
\right),
$$

one obtains

$$
\omega_a(u,\dot u)
=
r^2\dot\theta.
$$

So the sign of the oriented area sweep is the local rotation orientation.

The unlabeled relative phase of the two tetrahedral frames is encoded by

$$
q
=
e^{3i(\theta_+-\theta_-)}.
$$

Its real and imaginary parts give a threefold alignment/parity pair that is
invariant under relabeling of either triangular base.

The conservative relative-rotation model uses

$$
V(\phi)
=
\kappa(1-\cos3\phi),
$$

with

$$
\phi=\theta_+-\theta_-.
$$

The reduced relative energy is

$$
E_r
=
\frac{\ell^2}{2I_r}
+
\kappa(1-\cos3\phi).
$$

Because the potential barrier is \(2\kappa\),

$$
\boxed{
E_r>2\kappa
}
$$

gives persistent relative rotation, while

$$
E_r<2\kappa
$$

gives libration.

This produces sustained rotation without inserting a one-way angular drift
term by hand.

Run the executable example:

~~~bash
python examples/dual_tetrahedral_rotor.py
~~~

See <code>docs/DUAL_TETRAHEDRAL_DYNAMICS.md</code>.

---

## The next 1

The next-branch problem has one structural obstruction.

Let the unresolved branch variable be

$$
z\in\mathbb C,
$$

with the residual threefold symmetry

$$
z\mapsto\omega z,
\qquad
\omega=e^{2\pi i/3}.
$$

For any deterministic \(C_3\)-equivariant vector field,

$$
F(\omega z)=\omega F(z),
$$

the exactly symmetric state obeys

$$
\boxed{
F(0)=0.
}
$$

So an exactly symmetric **current configuration alone** cannot choose one of
three equivalent branches.

The minimal branch field used in version 0.3 is

$$
\dot z
=
\mu z
+
\nu\bar z^2
-
\beta|z|^2z.
$$

For positive \(\nu\), its three stable rays are

$$
\theta_k=\frac{2\pi k}{3},
\qquad
k=0,1,2.
$$

A small hidden residual can therefore remain dynamically insignificant while
the symmetric state is stable, then be amplified when that state loses
stability.

The reduced coupled model uses the already existing rotor barrier

$$
E_c=2\kappa
$$

as one explicit candidate trigger:

$$
\mu(E_r)
=
\sigma(2\kappa-E_r).
$$

Weak rotor dissipation gives

$$
\dot E_r
=
-\gamma\dot\phi^2
\le0.
$$

A transported hidden residual then evolves by

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

The model therefore implements

$$
\boxed{
\text{hidden historical difference}
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

Crucially, if the hidden residual is exactly zero, deterministic selection does
not occur. The selector is not a post-hoc argmax over the current state; it is
a retained difference that becomes dynamically relevant later.

Run:

~~~bash
python examples/next_one_selection.py
~~~

See <code>docs/NEXT_ONE_SELECTION.md</code>.

The barrier-coupled growth law is a reduced-model closure, not yet a result of
the original XNOR network. The next empirical task is to identify the hidden
residual and instability parameter directly in the learning dynamics.

---

## Actual XNOR transverse extraction

Version 0.4 returns from the reduced model to the original centered XNOR
network.

For hidden units 1, 2 and 3, collect the local parameter vectors

$
q_i=(a_i,b_i,w_{i1},w_{i2})\in\mathbb R^4.
$

Using the branch-aligned copy-space basis

$
c_R=\frac1{\sqrt6}(2,-1,-1),
\qquad
c_I=\frac1{\sqrt2}(0,1,-1),
$

define the actual hidden residual

$
\boxed{
Z=
\sum_{i=1}^3
(c_{R,i}+i c_{I,i})q_i
\in\mathbb C^4.
}
$

On the exact three-copy symmetric trajectory, the existing SGD rule gives

$
\boxed{
Z_{e+1}=M_eZ_e+O(\|Z_e\|^2),
}
$

where \(M_e\) is the exact epoch transverse Jacobian.

A finite-time instability rate is therefore available directly from the
network:

$
\boxed{
\mu_e=\log\sigma_1(M_e).
}
$

For centered XNOR, the largest transverse singular value is greater than 1 at
every epoch through the ordinary convergence point at epoch 728.

The instantaneous expanding-channel dimension follows

$
2\rightarrow3\rightarrow2\rightarrow1
$

over the intervals 1–8, 9–131, 132–558 and 559–728.

At epoch 728 the accumulated transverse singular values are approximately

$
(34.7030,\;24.1998,\;0.3200,\;7.18\times10^{-8}).
$

An actual \(10^{-6}\) mean-zero output-weight residual is amplified by about
\(15.156\times\) by epoch 728 under the unmodified learning rule.

This changes the status of the version-0.3 barrier closure: the expression

$
\mu(E_r)=\sigma(2\kappa-E_r)
$

remains a reduced-model example, but it is not the XNOR instability mechanism.
The actual XNOR instability is already present from the start.

Run the diagnostics from Python with
<code>scan_transverse_growth</code> and
<code>transverse_residual</code>.

See <code>docs/XNOR_TRANSVERSE_EXTRACTION.md</code>.

The remaining sharp edge is nonlinear: extract the actual \(C_3\) anisotropy
that can turn an amplified historical phase into a discrete three-way branch.

---

## Recursive spring extension

If a selected child axis becomes the axis of another copy of the same
dimensionless dynamics, then a local helix can seed a smaller child helix.

With a fixed scale factor

$$
0<\lambda<1,
$$

and repeated tetrahedral branching, the construction gives an explicit route
to a self-similar multiscale spring/tree geometry.

This is a mathematical extension of the model, not yet an empirical result of
the XNOR network.

---

## What is new here

The project does not claim that symmetry breaking in neural-network
initialization is new. It is not.

The contribution is narrower:

- isolate a historically observed accidental asymmetry as an explicit operator,
- make the symmetric control first-class,
- make the perturbation magnitude \(\varepsilon\) sweepable,
- isolate a centered control that preserves the initial network function,
- expose the regular-tetrahedron geometry of the four centered 3+1 directions,
- identify the axis plus two-dimensional transverse plane generated by a 3+1 split,
- provide an explicit dual-tetrahedral relative-rotation model,
- expose oriented area/parity as the invariant structure that a
  configuration-only snapshot can discard,
- derive an exact conservative rotation threshold,
- prove that an exactly symmetric deterministic present cannot choose a
  residual branch by itself,
- add the minimal (C_3)-equivariant next-branch normal form,
- show how a retained hidden residual can be transported and amplified into a
  persistent next-1 branch,
- keep the barrier-coupled instability law explicitly provisional,
- extract the actual complex three-copy residual from the original XNOR network,
- derive its exact transverse Jacobian and finite-time growth rates,
- verify that the exact symmetric manifold is invariant but transversely
  amplifying throughout centered XNOR training,
- move the remaining open problem to the nonlinear (C_3) branch-locking term.

It remains a laboratory object, not a production ML library.

---

## Scaling question

The tiny 3+1 system also suggests a larger experimental question: do wide
networks begin training with groups of units whose activations and gradients
are highly correlated, so that their effective dynamical dimension is much
smaller than their raw width?

That remains a hypothesis, not a conclusion.

See <code>docs/SCALING_HYPOTHESIS.md</code>.

---

## Historical inspiration

The project was inspired by studying a 1996 AMOS neural-network program by
Lee Atkins recovered from Aminet.

The original program is **not included** in this repository and this package
does not adopt or relicense its source code.

See <code>docs/PROVENANCE.md</code>.

A short historical note is kept in <code>docs/LEE_NOTE.md</code>.

---

## License

The new three-plus-one implementation is released under the MIT License.

That license applies only to this repository's new implementation and
documentation. It does not grant rights to Lee Atkins' original 1996 source.
