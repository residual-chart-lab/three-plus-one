import math

from threeplusone import (
    NextOneParams,
    NextOneState,
    branch_lock_error,
    rotor_energy,
    selected_branch,
    simulate_next_one,
)


def run_case(label: str, history_angle: float) -> None:
    params = NextOneParams()

    initial = NextOneState(
        phi=0.0,
        ell=1.8,
        z_re=1e-4 * math.cos(history_angle),
        z_im=1e-4 * math.sin(history_angle),
    )

    states = simulate_next_one(
        initial,
        params,
        dt=0.01,
        steps=5000,
        record_every=500,
    )

    final = states[-1]

    print(
        f"{label}: "
        f"E0={rotor_energy(states[0], params):.3f} "
        f"E1={rotor_energy(final, params):.3f} "
        f"branch={selected_branch(final)} "
        f"|z|={abs(final.z):.3f} "
        f"lock_error={branch_lock_error(final):.3e}"
    )


if __name__ == "__main__":
    run_case("history 0", -2.0 * math.pi / 3.0)
    run_case("history 1", 0.0)
    run_case("history 2", 2.0 * math.pi / 3.0)
