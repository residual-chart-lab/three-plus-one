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
