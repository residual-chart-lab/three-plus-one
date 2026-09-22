# Provenance, historical source, and research separation

This repository has two distinct kinds of provenance:

1. historical inspiration from a 1996 neural-network program,
2. mathematical context from the existing symmetry-breaking literature.

They should not be mixed.

---

## 1. Historical inspiration

The project was inspired by analysis of a small 1996 AMOS neural-network
program by Lee Atkins, distributed through Aminet.

During reconstruction work, an asymmetry in one hidden-to-output connection
was found to act as a symmetry-breaking seed in the XNOR example.

That observation motivated the controlled family

\[
a^{(0)}
=
a_0\mathbf1+\varepsilon s.
\]

---

## 2. Deliberate source-code separation

`three-plus-one` is not a source translation.

It does not contain:

- the original AMOS source,
- a line-by-line Python transcription,
- the historical variable names,
- the historical control flow,
- the historical update order,
- the original training-loop structure.

The current package uses a new implementation with conventional
backpropagation and explicit experimental controls.

---

## 3. Established theory imported later

As the project developed, several structures independently reached by the
derivation were recognized as established theory:

- hidden-unit permutation symmetry,
- the standard representation of \(S_n\),
- symmetry breaking / specialization,
- equivariant bifurcation,
- quadratic equivariants,
- the \(C_3\) conjugate-square harmonic,
- symmetry-adapted Hessian analysis.

These ideas are now treated as imported mathematical infrastructure rather
than as project novelty.

See
[`PRIOR_ART_AND_POSITIONING.md`](PRIOR_ART_AND_POSITIONING.md).

---

## 4. Project-specific empirical layer

The repository's narrower empirical contribution concerns the current
deterministic sigmoid-XNOR implementation:

- the controlled 3+1 and centered-3+1 interventions,
- the explicit complex residual \(Z\in\mathbb C^4\),
- the exact transverse Jacobian used here,
- measured finite-time transverse amplification,
- direct nonlinear phase-Fourier extraction,
- quantitative agreement between the extracted quadratic coefficient and the
  observed phase drift.

Those results should be distinguished from general statements about neural
networks.

---

## 5. Separate exploratory geometry

The dual-tetrahedral rotor construction was adapted from earlier Spark Engine
geometry.

It is retained as a separate mathematical model for oriented area, relative
motion, and recursive axis generation.

It is **not** currently claimed to be a mechanism derived from standard SGD.

---

## 6. Rights

The original 1996 source carries Lee Atkins' copyright notice and no
redistribution license has been verified.

For that reason, this repository intentionally excludes the original file.

The MIT license in this repository applies only to the new implementation and
documentation contained here.
