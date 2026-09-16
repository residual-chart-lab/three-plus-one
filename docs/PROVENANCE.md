# Provenance and separation from the historical source

## Historical inspiration

The project was inspired by analysis of a small 1996 AMOS neural-network
program by Lee Atkins, distributed through Aminet.

During reconstruction work, an asymmetry in one hidden-to-output connection
was found to act as a symmetry-breaking seed in the XNOR example.

That observation motivated the present project.

## Deliberate separation

`three-plus-one` is not a source translation.

It does not contain:

- the original AMOS source,
- a line-by-line Python transcription,
- the historical variable names,
- the historical control flow,
- the historical update order,
- the original training loop structure.

Instead, it implements a new mathematical object:

\[
a^{(0)}=a_0\mathbf{1}+\varepsilon s
\]

under conventional backpropagation.

The historical artifact is cited for inspiration only.

## Rights

The original 1996 source carries Lee Atkins' copyright notice and no
redistribution license has been verified.

For that reason, this repository intentionally excludes the original file.

The MIT license in this repository applies only to the new implementation and
documentation contained here.
