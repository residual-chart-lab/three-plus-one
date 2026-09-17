# three-plus-one
## The Three Plus One Network

A tiny experimental framework for one question:

> What happens when a perfectly symmetric hidden population receives one
> deliberately asymmetric seed?

This project is **not** a port of the 1996 AMOS program that inspired it.
It is a new implementation of the underlying phenomenon.

The historical observation was simple: a bug-looking asymmetry in a small
neural network appeared to break a deadlock that a "repaired" symmetric
initialization could not escape.

`three-plus-one` turns that accident into an explicit experimental operator.

---

## Core construction

All hidden units begin with the same incoming weights:

$$
B_i^{(0)} = b_0
$$

The outgoing hidden-to-output weights begin as:

$$
a_i^{(0)} = a_0 + \varepsilon s_i
$$

For the default four-hidden-unit case,

$$
s=(0,0,0,1)
$$

so

$$ a^{(0)} = \begin{bmatrix} a_0 \\ a_0 \\ a_0 \\ a_0+\varepsilon \end{bmatrix} $$

That is the **3+1 seed**.

More generally, with $n$ hidden units this is an $(n-1)+1$ construction.

The important control is $\varepsilon=0$: then all hidden units are exactly
symmetric.

---

## Why this can matter

With deterministic data order and identical hidden units, standard
backpropagation preserves symmetry when the outgoing weights are identical.

For one output unit, a hidden delta contains the factor

$$ \delta_i^{(h)}=h_i(1-h_i)\,\delta^{(o)}\,a_i $$

If $h_i=h_j$ and $a_i=a_j$, then the two units receive the same update.

But if

$$
a_i-a_j=\varepsilon(s_i-s_j),
$$

then, whenever the remaining factors are nonzero,

$$
\delta_i^{(h)}-\delta_j^{(h)}
=
h(1-h)\,\delta^{(o)}\,
\varepsilon(s_i-s_j)
$$

A tiny outgoing-weight asymmetry therefore creates an immediate difference in
the hidden updates. Whether that difference is useful is task-dependent; the
framework is designed to measure it rather than assume it.

---

## XNOR demo

Install locally:

```bash
python -m pip install -e .
```

Run:

```bash
three-plus-one demo
```

Default configuration:

- 2 inputs
- 4 hidden units
- 1 output
- identical incoming hidden weights
- sigmoid activation
- standard backpropagation
- explicit seed `s=(0,0,0,1)`
- `epsilon=1`

On the deterministic XNOR demo, the default run converges while the perfectly
symmetric control does not reach the same error target within the same budget.

Compare:

```bash
three-plus-one demo --epsilon 0
three-plus-one demo --epsilon 1
```

Sweep the seed magnitude:

```bash
three-plus-one sweep
```

---

## Generalized seeds

The code accepts arbitrary seed patterns.

Examples:

```python
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
```

The framework therefore studies a broader family:

$$
a^{(0)} = a_0\mathbf{1}+\varepsilon s
$$

---

## What is new here

The project does not claim that symmetry breaking in neural-network
initialization is new. It is not.

The contribution of this small package is narrower:

- isolate a historically observed accidental asymmetry as an explicit operator,
- make the symmetric control first-class,
- make the perturbation magnitude $\varepsilon$ sweepable,
- expose post-training hidden-unit grouping and hidden-weight spread,
- keep the system small enough that the entire mechanism is inspectable.

It is a laboratory object, not a production ML library.

---

## Historical inspiration

The project was inspired by studying a 1996 AMOS neural-network program by
Lee Atkins recovered from Aminet.

The original program is **not included** in this repository and this package
does not adopt or relicense its source code.

See `docs/PROVENANCE.md`.

---

## Scaling question

The tiny 3+1 system suggests a larger experimental question: do wide networks
begin training with groups of units whose activations and gradients are highly
correlated, so that their effective dynamical dimension is much smaller than
their raw width?

That is deliberately framed as a hypothesis, not a conclusion.

See `docs/SCALING_HYPOTHESIS.md`.

## A note for Lee

A short historical note is kept in `docs/LEE_NOTE.md`, including an answer to
one question Lee left in an old AMOS-list signature.

## License

The new `three-plus-one` implementation is released under the MIT License.

That license applies only to this repository's new implementation and
documentation. It does not grant rights to Lee Atkins' original 1996 source.
