# Reproducible experiments

## Experiment A — exact symmetry

```bash
three-plus-one demo --epsilon 0
```

Expected qualitative result:

- all hidden incoming weights remain identical
- hidden spread remains exactly zero
- XNOR does not reach the default target MSE within the default budget

## Experiment B — three plus one

```bash
three-plus-one demo --epsilon 1
```

Expected qualitative result:

- the fourth hidden unit separates from the first three
- hidden spread becomes nonzero
- XNOR reaches the default target MSE

## Experiment C — epsilon sweep

```bash
three-plus-one sweep 0 0.01 0.05 0.1 0.2 0.5 1 2
```

The point is not to assert a universal critical epsilon.

The threshold depends on:

- learning rate
- initial base weights
- task
- training budget
- activation function
- data order

The sweep is a diagnostic for this particular dynamical system.

## Experiment D — change the partition

Use custom `seed_pattern` values to compare:

- `(n-1)+1`
- `(n-2)+2`
- graded seeds
- alternating signs
- zero-sum seeds

This is the path from the historical 3+1 observation to a general controlled
symmetry-breaking laboratory.


## Experiment E — centered three plus one

The default singleton seed changes the sum of the hidden-to-output weights.
The centered control removes that change while preserving the 3+1 asymmetry.

```bash
three-plus-one demo --epsilon 1 --centered
```

For four hidden units the seed is

```text
(-0.25, -0.25, -0.25, 0.75)
```

and its entries sum to zero.

Expected qualitative result:

- the centered seed has the same initial network predictions as the
  `epsilon=0` symmetric control
- hidden symmetry still breaks after the first nonzero gradient signal
- the deterministic XNOR run reaches the default target MSE
- the first three hidden units remain grouped and the fourth separates

A centered sweep is also available:

```bash
three-plus-one sweep --centered 0 0.01 0.05 0.1 0.2 0.5 1 2
```

This is the cleaner control when the question is whether symmetry breaking
itself matters, rather than a simultaneous shift in the initial output.


## Experiment F — actual transverse growth

Run the exact centered-XNOR transverse diagnostics:

~~~bash
python examples/xnor_transverse_scan.py
~~~

This experiment does not introduce a new optimizer state. It extracts the
mean-zero three-copy residual already present in the network parameters and
measures the tangent growth of that residual under the existing training rule.

Expected deterministic results for the current default setup:

- ordinary centered XNOR reaches the target at epoch 728,
- the largest one-epoch transverse singular value is greater than 1 at every
  measured epoch through 728,
- the expanding channel dimension follows
  \(2\to3\to2\to1\),
- the accumulated top transverse gain at epoch 728 is about \(34.703\),
- a direct \(10^{-6}\) hidden-to-output residual is amplified by about
  \(15.156\times\) by epoch 728.

See
[`XNOR_TRANSVERSE_EXTRACTION.md`](XNOR_TRANSVERSE_EXTRACTION.md).

## Experiment G — nonlinear threefold anisotropy

Run:

~~~bash
python examples/xnor_quadratic_anisotropy.py
~~~

The experiment phase-sweeps a small transverse residual and Fourier-decomposes
the actual nonlinear training map.

For the original hidden-to-output residual channel, the current deterministic
run gives approximately

\[
\lambda_{\rm out}\approx15.15569,
\]

\[
\nu_{\rm out}\approx6.65860.
\]

The extracted quadratic coefficient predicts the small-amplitude phase drift

\[
\Delta\theta
=
-\frac{\nu}{\lambda}r\sin3\theta
+
O(r^2),
\]

which is then checked against the full nonlinear XNOR course.

See
[`XNOR_QUADRATIC_ANISOTROPY.md`](XNOR_QUADRATIC_ANISOTROPY.md).

## Interpretation rule

The experiments deliberately separate three claim levels:

1. **established theory** — permutation symmetry, standard representations,
   equivariant bifurcation, quadratic equivariants;
2. **system-specific measurements** — the exact numbers reported by this
   deterministic sigmoid-XNOR implementation;
3. **exploratory models** — the dual-tetrahedral rotor and recursive geometry.

Do not promote a result from one level into another without a derivation or
experiment.

See
[`PRIOR_ART_AND_POSITIONING.md`](PRIOR_ART_AND_POSITIONING.md).
