from threeplusone import (
    DualRotorParams,
    DualRotorState,
    relative_energy,
    relative_regime,
    relative_winding,
    simulate_dual_rotor,
)


def run_case(label: str, p: float) -> None:
    params = DualRotorParams(kappa=1.0)
    initial = DualRotorState(
        theta_plus=0.0,
        theta_minus=0.0,
        p_plus=p,
        p_minus=-p,
    )
    states = simulate_dual_rotor(
        initial,
        params,
        dt=0.002,
        steps=10000,
        record_every=50,
    )

    energy0 = relative_energy(states[0], params)
    max_energy_error = max(
        abs(relative_energy(state, params) - energy0)
        for state in states
    )

    print(
        f"{label}: "
        f"regime={relative_regime(initial, params)} "
        f"winding={relative_winding(states):.3f} "
        f"max_relative_energy_error={max_energy_error:.3e}"
    )


if __name__ == "__main__":
    # E_rel = p^2 for I_+=I_-=1 and phi(0)=0.
    # The exact barrier is 2*kappa.
    run_case("below barrier", p=1.0)
    run_case("above barrier", p=1.5)
