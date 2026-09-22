# Future admissibility, retained difference, and the persistence gap

Status: handoff note connecting the current `three-plus-one` results to the
minimal-refinement / continuation machinery already present in Free Numbers.

This note is deliberately conservative. It does **not** claim backward
physical causation. It isolates the mathematical components that would be
needed before such a claim could even be formulated.


> **Persistence-test update.** A direct centered-XNOR test now shows that the
> retained residual survives and threefold selector action continues to
> accumulate well after the ordinary task target is reached (verified through
> 100,000 epochs). The remaining issue is therefore not simply "does the drive
> die?" but whether cumulative selector action is summable:
>
> \[
> \mathcal A_\infty<\infty
> \quad\text{or}\quad
> \mathcal A_\infty=\infty.
> \]
>
> See [`SELECTOR_PERSISTENCE.md`](SELECTOR_PERSISTENCE.md).

---

## 1. Current empirical starting point

The centered deterministic XNOR system currently supplies the following chain:

$$
\boxed{
\text{nonzero transverse residual}
\rightarrow
\text{transport}
\rightarrow
\text{amplification}
\rightarrow
\text{threefold directional sorting}.
}
$$

The residual is

$$
Z\in\mathbb C^4,
$$

and its first-order epoch dynamics are

$$
Z_{e+1}
=
M_e Z_e
+
O(\|Z_e\|^2).
$$

The nonlinear copy-space symmetry is described locally by

$$
F(Z)
=
LZ
+
Q(\bar Z,\bar Z)
+
O(\|Z\|^3).
$$

In one projected residual channel this becomes

$$
z'
=
\lambda z
+
\nu\bar z^2
+
O(|z|^3).
$$

The actual XNOR map contains a nonzero quadratic coefficient and the resulting
phase drift is quantitatively observed.

Thus a difference that begins as an externally supplied perturbation can later
participate in selecting the direction of its own continuation.

This is the first role reversal:

$$
\boxed{
\text{difference as payload}
\longrightarrow
\text{difference as selector}.
}
$$

That role reversal is more important than the weaker statement

$$
\|Z_t\|>\|Z_0\|.
$$

Amplitude growth alone is not yet autonomous selection.

---

## 2. A useful threshold distinction

Define schematically

$$
\chi(Z)
=
\frac{\|Q(\bar Z,\bar Z)\|}
{\|LZ\|}.
$$

Then:

- \(\chi=0\): purely linear transport;
- \(0<\chi\ll1\): selector emergence;
- \(\chi\sim1\): nonlinear selector competes with inherited linear transport;
- \(\chi>1\): selector-dominated local motion.

The present XNOR calculations establish selector emergence and measurable
threefold phase sorting.

They do **not** yet establish that the system reaches a regime where
\(\chi\ge1\) while the local quadratic truncation remains valid.

Therefore the phrase "the copy exceeds the original" should currently be used
in the causal-role sense:

> a retained difference begins to participate in choosing the next difference.

It should not be identified only with an amplitude crossover.

---

## 3. Symmetry constrains admissible future operations

The residual three-copy sector carries the standard two-dimensional
representation of

$$
S_3\simeq D_3.
$$

The cyclic part acts as

$$
z\mapsto\omega z,
\qquad
\omega=e^{2\pi i/3}.
$$

The three oriented singleton rays are associated with the three reflection
isotropy subgroups

$$
H_k\simeq\mathbb Z_2,
\qquad
k=0,1,2,
$$

through their fixed-point lines

$$
\operatorname{Fix}(H_k).
$$

Therefore future operations are not arbitrary maps.

At a given truncation order they must lie in the corresponding space of
equivariant operations.

At second order, write this admissible operation space schematically as

$$
\boxed{
\mathfrak A_G^{(2)}
=
\{\text{\(G\)-equivariant 2-jets on the residual representation}\}.
}
$$

For the scalar complex residual coordinate, the lowest allowed terms have the
form

$$
z'
=
\lambda z
+
\nu\bar z^2
+
\cdots.
$$

The symmetry determines the **form of admissible operations**.

It does not determine:

- the numerical values of \(\lambda,\nu\),
- which admissible operation the actual system realizes,
- which of the three symmetry-related branches is selected,
- whether the selected difference persists indefinitely.

---

## 4. Three levels of future operation

To avoid collapsing several distinct notions into one symbol, separate:

$$
\boxed{
\mathfrak A_G
\supseteq
\mathcal O_{\mathrm{dyn}}
\supseteq
\mathcal P_k.
}
$$

### 4.1 Symmetry-admissible operations

\(\mathfrak A_G\) is the family of operations allowed by the current symmetry type.

### 4.2 Dynamically realized operations

\(\mathcal O_{\mathrm{dyn}}\) contains the operations actually realized by the
concrete system. For the current XNOR model, measured \(M_e,\lambda,\nu\) are
examples of dynamical data at this layer.

### 4.3 Branch-conditioned continuations

For a future branch \(B_k\), let \(\mathcal P_k\) be the family of allowed
finite continuation paths compatible with reaching that branch.

This is the correct layer for asking:

> which present differences remain relevant if branch \(B_k\) is the future
> outcome?

---

## 5. Free Numbers already contains the key continuation theorem

Free Numbers Note 27 defines, for a state \(s\), all allowed finite
continuations

$$
w:s\to t,
$$

including the identity path, and sets

$$
\boxed{
K_s
=
\bigcap_{w:s\to t}
\ker(q_tJ_w).
}
$$

Interpretation:

$$
\boxed{
K_s
=
\text{differences invisible now and invisible under every allowed future continuation}.
}
$$

The quotient

$$
\boxed{
\widetilde E_s
=
E_s/K_s
}
$$

therefore retains exactly those present differences that some allowed future
continuation can later detect.

Note 27 also proves

$$
\boxed{
J_aK_s\subseteq K_t.
}
$$

Hence each allowed update induces

$$
\bar J_a:
E_s/K_s
\longrightarrow
E_t/K_t.
$$

This is already a rigorous answer to the operational question:

> which currently replaceable differences must be retained if future
> continuation may later distinguish them?

It is an operation-based equivalence criterion. It is not yet a persistence
force or backward physical causation.

---

## 6. Branch-conditioned retained difference

For a selected future branch define

$$
\boxed{
K_s^{(k)}
=
\bigcap_{w\in\mathcal P_k}
\ker(q_tJ_w).
}
$$

Then

$$
x\sim_k y
$$

iff

$$
q_tJ_wx=q_tJ_wy
\qquad
\text{for every }w\in\mathcal P_k.
$$

Thus

$$
\boxed{
B_k
\text{ indexes an equivalence relation on earlier states.}
}
$$

Two present states can be indistinguishable now but inequivalent relative to
one future branch:

$$
q_s(x)=q_s(y),
\qquad
x-y\notin K_s^{(k)}.
$$

The associated retained quotient is

$$
\boxed{
R_s^{(k)}
=
E_s/K_s^{(k)}.
}
$$

This is the cleanest current mathematical form of:

> a future result determines which earlier differences were replaceable and
> which were not.

---

## 7. Symmetry before branch selection

Before branch selection,

$$
K_s^{(0)},
\qquad
K_s^{(1)},
\qquad
K_s^{(2)}
$$

are symmetry-related and form one \(S_3\) orbit.

No branch is privileged.

The nonlinear selector carried by the residual then produces the transition

$$
\boxed{
\{K_s^{(0)},K_s^{(1)},K_s^{(2)}\}
\longrightarrow
K_s^{(k)}.
}
$$

The residual is no longer merely something retained because a future operation
might detect it. Its phase also participates in selecting which
future-conditioned equivalence relation becomes relevant.

---

## 8. Division of labor

Symmetry gives

$$
\boxed{\text{admissible operation form}}
$$

and

$$
\boxed{\text{admissible branch type}}.
$$

History / residual gives

$$
\boxed{\text{which symmetry-related branch becomes selected}}.
$$

Free Numbers gives

$$
\boxed{
\text{which currently invisible differences that branch-compatible future
operations can later detect}.
}
$$

The tested XNOR residual does remain dynamically present over the measured
finite horizon. What is still unresolved is whether the continuing
directional contraction has infinite cumulative action:

$
\boxed{
\mathcal A_\infty
=
\infty
\quad\text{or}\quad
<\infty.
}
$

That is the selector-action summability gap.

---

## 9. Possible future relevance is not realized relevance

If

$$
\delta\notin K_s,
$$

then at least one allowed future continuation detects \(\delta\).

But a different actually realized continuation can still erase it.

Therefore

$$
\boxed{
\text{possible future relevance}
\neq
\text{relevance along the realized future}.
}
$$

The branch-conditioned kernel \(K_s^{(k)}\) narrows the operation family to
continuations compatible with \(B_k\), but the quotient still tells us only
what must remain distinguishable. It does not itself provide the dynamical
mechanism that keeps representative information alive.

---

## 10. Minimal Time Engine bridge

At the present stage the strongest justified statement is not

$$
\text{future state causes the present}.
$$

It is

$$
\boxed{
\text{future result}
\longrightarrow
\text{equivalence relation on earlier differences}.
}
$$

Equivalently,

$$
\boxed{
\text{the future indexes which past differences count as replaceable}.
}
$$

This is a backward dependence of classification, not yet a backward force.

It is therefore a plausible **minimal component** for a later future-causal
theory.

---

## 11. Nonlinear bridge: use equivariant jets

Free Numbers Note 27 is linear, whereas the actual three-plus-one selector
contains

$$
\nu\bar z^2.
$$

A direct identification is therefore incomplete.

A natural next formalization is a finite \(G\)-equivariant jet space. At
second order, use a state containing the relevant linear and quadratic
coordinates, schematically

$$
\boxed{
\mathcal J_G^{(2)}
\ni
(z,\bar z^2,\ldots).
}
$$

Then:

1. admissible operations are \(G\)-equivariant 2-jets;
2. truncated composition is well-defined;
3. finite continuation paths can be formed;
4. branch-conditioned kernels can be computed at jet level;
5. measured \(\lambda,\nu\) can be inserted without pretending the selector
   is linear.

This is the cleanest current bridge between the nonlinear XNOR result and the
linear continuation-refinement theorem.

---

## 12. Current map

$$
\boxed{
S_3
\rightarrow
\mathfrak A_{S_3}^{(2)}
\rightarrow
\mathcal O_{\mathrm{dyn}}
\rightarrow
\mathcal P_k
\rightarrow
K_s^{(k)}
\rightarrow
E_s/K_s^{(k)}
\rightarrow
\text{selector-action summability gap}.
}
$$

Read from left to right:

- symmetry restricts future operation form;
- the actual system realizes a subset of those operations;
- a future branch restricts the relevant continuation family;
- that family defines which earlier differences are safely discardable;
- the quotient retains all branch-relevant differences;
- a separate persistence mechanism is still required to keep them alive.

---

## 13. Claim boundary

### Established / already available

- \(S_3/D_3\) residual symmetry;
- standard representation and isotropy lines;
- equivariant quadratic conjugate-square form;
- the Free Numbers all-continuation kernel
  \[
  K_s=\bigcap_w\ker(q_tJ_w);
  \]
- quotient descent
  \[
  J_aK_s\subseteq K_t.
  \]

### Measured in the current XNOR model

- actual transverse residual \(Z\);
- exact linear transport \(M_e\);
- transverse amplification;
- nonzero quadratic anisotropy;
- threefold phase sorting.

### New synthesis / current proposal

- distinguish
  \[
  \mathfrak A_G,\ \mathcal O_{\mathrm{dyn}},\ \mathcal P_k;
  \]
- define branch-conditioned kernels
  \[
  K_s^{(k)};
  \]
- interpret the future branch as indexing an earlier-state equivalence relation;
- bridge the nonlinear selector to continuation quotients through
  \(G\)-equivariant finite jets.

### Not yet established

- the asymptotic summability class of the actual selector action;
- future-to-present physical force;
- a proof that Time Engine future causality follows from the present mathematics.

---

## 14. Next exact task

Do **not** search again for generic symmetry breaking.

Do **not** rederive the existence of the \(\bar z^2\) harmonic.

The next exact task is:

> Build the smallest \(S_3\)-equivariant 2-jet continuation model containing
> the measured XNOR linear and quadratic terms, define branch-conditioned
> continuation families \(\mathcal P_k\), and compute the resulting
> \(K_s^{(k)}\) / retained quotient.

In parallel, the direct persistence diagnostic should be pushed from a finite
horizon to an asymptotic statement:

> Does \(\mathcal A_N\) remain bounded, or does it diverge?

The finite-horizon test already shows that the residual is not simply erased
when ordinary task convergence is reached. The unresolved issue is whether
the selector action is summable.

That is the current handoff point.
