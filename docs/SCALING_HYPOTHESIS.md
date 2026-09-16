# Scaling hypothesis: synchronized groups in large models

This is a research hypothesis, not a claim established by the package.

## Question

A small deterministic network can contain units that remain exactly synchronized
when their states and gradient signals are identical. A deliberately introduced
asymmetry can split that synchronized group.

The large-model question is weaker and more interesting:

> During early training, do wide neural networks contain **approximate dynamical
> groups** whose units follow strongly correlated activation/gradient trajectories,
> so that the effective number of independently moving features is much smaller
> than the raw number of units?

If so, learning could be viewed partly as a sequence of group-splitting events:

\[
\mathcal C_1
\longrightarrow
\mathcal C_{1a}\oplus\mathcal C_{1b}
\longrightarrow \cdots
\]

rather than as every unit immediately behaving as an independent degree of freedom.

## Why this is not the same as exact symmetry

Modern large models are normally randomly initialized and trained with sources of
asymmetry such as minibatch order, dropout, normalization, optimizer state and
heterogeneous inputs.

Therefore exact equality of two neurons over training is not expected in general.

The hypothesis concerns **approximate synchronization**:

- highly correlated activations,
- highly aligned gradients,
- small trajectory distance,
- low effective feature rank,
- stable clusters of units over a finite training window.

## A measurable form

For layer \(\ell\) at training time \(t\), let

\[
H_\ell(t)\in\mathbb R^{B\times n}
\]

be the activation matrix over a probe batch, and let

\[
G_\ell(t)\in\mathbb R^{n\times p}
\]

collect per-unit gradient vectors.

Possible observables:

### 1. Activation effective rank

If \(\sigma_k\) are singular values of \(H_\ell\), define

\[
p_k=\frac{\sigma_k^2}{\sum_j \sigma_j^2},
\qquad
r_{\mathrm{eff}}
=
\exp\left(-\sum_k p_k\log p_k\right).
\]

If \(r_{\mathrm{eff}}\ll n\), the layer has many units but a much smaller
effective activation dimension on the probe distribution.

### 2. Gradient alignment

For units \(i,j\),

\[
C^{(g)}_{ij}
=
\frac{\langle g_i,g_j\rangle}
{\|g_i\|\|g_j\|}.
\]

Persistent blocks with \(C^{(g)}_{ij}\approx1\) are candidates for dynamical
groups.

### 3. Weight-trajectory distance

Track

\[
D_{ij}(t)
=
\|w_i(t)-w_j(t)\|.
\]

A useful group is not merely close at one instant; it remains close over a
training interval and responds similarly to perturbations.

### 4. Group count versus width

Let \(K_\ell(t)\) be the number of robust clusters under a fixed clustering
criterion. Compare

\[
K_\ell(t)
\quad\text{with}\quad
n_\ell.
\]

The strong version of the hypothesis predicts an early regime where

\[
K_\ell(t)\ll n_\ell
\]

for at least some layers, followed by increasing differentiation during learning.

## Falsifiable predictions

The hypothesis becomes interesting only if it can fail.

1. Increasing width while keeping task/data fixed may increase raw unit count
   faster than early effective rank.
2. Stronger explicit symmetry-breaking noise should shorten the lifetime of
   synchronized groups.
3. Removing stochastic asymmetry should make group structure more persistent.
4. Units inside one group should have similar ablation effects early in training.
5. A controlled perturbation to one member of a group may either decay
   (stable synchronization) or amplify (symmetry-breaking instability).

## Relation to Three Plus One

`three-plus-one` is only the smallest laboratory.

It establishes a clean control:

\[
\varepsilon=0
\quad\text{versus}\quad
\varepsilon\neq0.
\]

The scaling question is not "are large models secretly this four-neuron toy?"

It is:

> Does the same broad dynamical distinction — synchronized subspaces versus
> symmetry-breaking differentiation — remain useful when the system is wide,
> stochastic and highly overparameterized?

That question should be tested, not assumed.
