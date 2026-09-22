# Changelog

## 0.5.0 — 2026-09-22

- derive that C3/S3 equivariance forces the quadratic transverse term to have conjugate-square form
- add nonlinear phase-Fourier extraction for the actual XNOR training map
- extract a nonzero -2 harmonic from the dominant 728-epoch transverse channel
- measure the dominant-course coefficients lambda ~= 34.70306 and nu ~= -87.21614 in the fixed channel orientation
- extract the original hidden-to-output residual channel coefficients lambda ~= 15.15569 and nu ~= +6.65860
- verify that the extracted quadratic coefficient predicts the measured nonlinear phase shift
- verify C3 covariance of the full nonlinear 728-epoch course
- verify finite-amplitude angular attraction toward the three oriented singleton rays
- keep the exact-zero no-selection theorem intact
- make explicit that centered XNOR exhibits directional sorting but not complete asymptotic locking from a generic off-ray residual
- move the remaining gap to persistence: what keeps the update alive long enough to complete the next-1 lock?

## 0.4.0 — 2026-09-22

- extract the actual hidden three-copy residual as a complex four-channel variable
- derive the exact one-sample transverse Jacobian of the existing XNOR SGD update
- factor the transverse tangent space into copy-space orientation and parameter-channel dynamics
- define the actual finite-time instability rate from transverse singular growth
- verify that centered XNOR is transversely amplifying at every epoch through convergence
- measure the expanding-channel dimension sequence 2 -> 3 -> 2 -> 1
- measure cumulative transverse gains on the unmodified centered XNOR trajectory
- verify that a 1e-6 hidden residual is amplified by the actual training rule
- correct the version-0.3 barrier-coupled instability law: it remains a reduced-model closure, not the XNOR instability mechanism
- add dependency-free transverse diagnostics and regression tests
- move the sharp edge to extraction of the nonlinear C3 anisotropy / branch-locking term

## 0.3.0 — 2026-09-22

- prove the no-selection result for an exactly symmetric deterministic current state
- add the minimal real-reflection-symmetric `C3` branch normal form
- model the next 1 as amplification of a retained hidden historical residual
- add weakly damped relative-rotor dynamics with monotone energy loss
- add a barrier-coupled instability closure using the existing `2*kappa` rotor threshold
- transport the hidden residual with signed relative angular velocity
- add regression tests showing exact zero history never self-selects
- add regression tests showing three `C3`-related hidden histories select three related branches
- add an executable next-one selection example
- keep the barrier/instability coupling explicitly provisional pending extraction from the original XNOR dynamics

## 0.2.0 — 2026-09-22

- expose the regular-tetrahedron geometry of the four centered 3+1 directions
- derive the distinguished axis and canonical two-dimensional transverse plane
- add dual oppositely oriented tetrahedral frames with independent rotations
- add the oriented transverse area form and unlabeled threefold parity observable
- add a conservative two-rotor Hamiltonian with exact libration/rotation threshold
- add a symplectic velocity-Verlet simulator and regression tests
- derive the exact tetrahedral child-axis geometry and branch angle
- keep the endogenous next-1 selection law explicitly open
- repair math rendering in the axis-generation documentation

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
