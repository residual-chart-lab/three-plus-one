# Mathematics

## 1. Symmetric hidden population

Let a one-hidden-layer network contain \(n\) hidden units.

Write the incoming parameter vector of hidden unit \(i\) as

\[
B_i \in \mathbb{R}^{d+1},
\]

including bias.

The symmetric initialization is

\[
B_1^{(0)} = B_2^{(0)} = \cdots = B_n^{(0)} = b_0.
\]

For one output unit, let hidden-to-output weights be

\[
a=(a_1,\dots,a_n).
\]

If initially

\[
a_1^{(0)}=\cdots=a_n^{(0)}=a_0,
\]

then hidden units are permutation-symmetric.

With deterministic training, identical activations and identical outgoing
weights give identical hidden gradients, so this equality is preserved.

## 2. Explicit symmetry seed

Define a seed vector

\[
s\in\mathbb{R}^{n}
\]

and perturbation magnitude \(\varepsilon\).

Set

\[
a^{(0)}
=
a_0\mathbf{1}
+
\varepsilon s.
\]

The default Three Plus One seed is

\[
s=(0,\dots,0,1).
\]

For \(n=4\),

\[
a^{(0)}
=
\begin{bmatrix}
a_0\\
a_0\\
a_0\\
a_0+\varepsilon
\end{bmatrix}.
\]

## 3. First-step divergence

For sigmoid hidden activation \(h_i\) and output delta \(\delta^{(o)}\),

\[
\delta_i^{(h)}
=
h_i(1-h_i)\delta^{(o)}a_i.
\]

At the symmetric hidden state \(h_i=h_j=h\),

\[
\delta_i^{(h)}-\delta_j^{(h)}
=
h(1-h)\delta^{(o)}(a_i-a_j).
\]

Substituting the seed gives

\[
\delta_i^{(h)}-\delta_j^{(h)}
=
h(1-h)\delta^{(o)}
\varepsilon(s_i-s_j).
\]

Thus a nonzero seed difference produces different hidden updates whenever

\[
h(1-h)\delta^{(o)}\neq 0.
\]

This is the precise mechanism implemented by the package.

## 4. What this does not prove

A nonzero \(\varepsilon\) does not guarantee successful learning.

The seed only removes one symmetry obstruction. Optimization can still fail
for many other reasons: saturation, poor step size, insufficient width,
incompatible architecture, task geometry, or finite training budget.

The right experimental question is therefore:

> after removing exact symmetry by a controlled amount, what changes?

That is why the package reports both task error and hidden-population spread.
