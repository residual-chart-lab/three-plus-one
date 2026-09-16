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
