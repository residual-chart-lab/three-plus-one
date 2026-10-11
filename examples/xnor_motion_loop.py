"""Eight repeated contacts, using the existing SGD and phase/hidden split.

The network base state is advanced inside the loop. No future-readout table,
new learning rule, or externally fitted memory coefficient is supplied.
"""
import hashlib
import json
import math
from copy import deepcopy
from pathlib import Path

from xnor_retained_difference import dot, epoch, inject, mv, radial, read
from threeplusone import (
    ThreePlusOneMLP, centered_singleton_seed, add_transverse_vector_seed,
    transverse_residual, xnor,
)
from threeplusone.transverse import epoch_transverse_matrix


def run():
    base = ThreePlusOneMLP(epsilon=1, seed_pattern=centered_singleton_seed(4))
    add_transverse_vector_seed(base, direction=(1, 0, 0, 0), amplitude=.1, phase=0)
    for _ in range(728):
        epoch(base)
    r = radial(base)
    full = r[:]
    y, hidden, erased_y = 1.0, [0.0]*4, 1.0
    amounts = (1e-2, 1e-3)
    pairs = [(inject(base, r, a), inject(base, r, -a)) for a in amounts]
    records = []
    for step in range(1, 9):
        # J is computed from the present base state and the prescribed inputs.
        # Advance that same state; no future orbit is consulted.
        j = epoch_transverse_matrix(base, xnor(), representative_unit=1)
        jr, jh = mv(j, r), mv(j, hidden)
        epoch(base)
        next_r = radial(base)
        rho = read(next_r, jr)
        returned = read(next_r, jh)
        next_y = rho*y + returned
        generated = [(a-rho*b)*y for a, b in zip(jr, next_r)]
        carried = [a-returned*b for a, b in zip(jh, next_r)]
        next_hidden = [a+b for a, b in zip(generated, carried)]
        full = mv(j, full)
        erased_y *= rho
        reassembled = [next_y*a+b for a, b in zip(next_r, next_hidden)]
        reconstruction_error = max(abs(a-b) for a, b in zip(full, reassembled))
        finite = []
        for amount, (plus, minus) in zip(amounts, pairs):
            epoch(plus)
            epoch(minus)
            responses = [read(next_r, [z.imag for z in transverse_residual(n)])
                         for n in (plus, minus)]
            derivative = (responses[0]-responses[1])/(2*amount)
            finite.append({"amplitude": amount, "derivative": derivative,
                           "error_vs_full_tangent": derivative-read(next_r, full)})
        assert reconstruction_error < 1e-13
        assert abs(read(next_r, next_hidden)) < 1e-14
        assert abs(next_y-read(next_r, full)) < 1e-13
        assert abs(finite[-1]["error_vs_full_tangent"]) < 2e-8
        records.append({
            "step": step, "epoch": 728+step, "phase": next_y,
            "erase_each_step_phase": erased_y, "keep_minus_erase": next_y-erased_y,
            "return_from_previous_hidden": returned,
            "new_hidden_norm": math.sqrt(dot(generated, generated)),
            "carried_hidden_norm": math.sqrt(dot(carried, carried)),
            "total_hidden_norm": math.sqrt(dot(next_hidden, next_hidden)),
            "reconstruction_error": reconstruction_error,
            "nonlinear_checks": finite,
        })
        r, y, hidden = next_r, next_y, next_hidden
    assert abs(records[0]["keep_minus_erase"]) < 1e-14
    assert abs(records[1]["keep_minus_erase"]-2.869405956915665e-6) < 5e-12
    assert all(abs(row["return_from_previous_hidden"]) > 1e-7 for row in records[1:])
    root = Path(__file__).resolve().parents[1]
    files = ["src/threeplusone/core.py", "src/threeplusone/transverse.py",
             "src/threeplusone/datasets.py", "examples/xnor_retained_difference.py",
             "examples/xnor_motion_loop.py"]
    return {
        "scope": "finite 8-epoch tangent loop, equal-pair antisymmetric sector",
        "initial_epoch": 728,
        "base_included": "full 17-parameter network advanced online, not reduced away",
        "controls": "full tangent vs phase/hidden reassembly vs erase hidden each epoch",
        "inputs_including_targets": xnor(),
        "records": records,
        "checks": "PASS",
        "source_sha256": {p: hashlib.sha256((root/p).read_bytes()).hexdigest() for p in files},
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
