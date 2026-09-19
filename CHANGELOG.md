# Changelog

## 0.1.2 — 2026-09-19

- add zero-sum centered `(n-1)+1` seed helper
- add `--centered` controls to the demo and epsilon sweep
- verify that centered 3+1 preserves the initial network function
- verify that the centered 3+1 seed still learns deterministic XNOR
- document the centered control as a cleaner symmetry-breaking experiment

## 0.1.1 — 2026-09-17

- add scaling hypothesis for approximate group synchronization in wide models
- define effective-rank, gradient-alignment and trajectory diagnostics
- add a small note for Lee Atkins
- keep all large-model claims explicitly falsifiable and provisional

## 0.1.0 — 2026-09-17

- first independent implementation
- explicit symmetry seed `a^(0) = a0 1 + epsilon s`
- deterministic XNOR demo
- symmetric control (`epsilon=0`)
- epsilon sweep
- hidden-group and hidden-spread diagnostics
- generalized seed patterns
- MIT license for the new implementation
- historical provenance kept separate from executable code
