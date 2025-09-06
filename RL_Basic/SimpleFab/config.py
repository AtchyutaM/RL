# === ALIGNMENT: shared_config.py (or paste in both files) ===
from typing import Dict, Any, List

def make_common_config(mode: str = "ALL_AT_T0", H: int = 50) -> Dict[str, Any]:
    # Base parameters (match both models)
    common = {
        'time_horizon': H,
        'machines': [0, 1, 2, 3],
        'products': [0, 1],

        # Processing/batch/setup identical to your code
        'processing_times': {
            0: {0: 16, 1: 20},
            1: {0: 2,  1: 2},
            2: {0: 16, 1: 20},
            3: {0: 2,  1: 2},
        },
        'batch_sizes': {0: 4, 1: 1, 2: 4, 3: 1},
        'setup_times': {     # informational for sim; MILP uses constraints
            0: {0: {0: 0, 1: 0}, 1: {0: 0, 1: 0}},
            1: {0: {0: 0, 1: 1}, 1: {0: 1, 1: 0}},
            2: {0: {0: 0, 1: 0}, 1: {0: 0, 1: 0}},
            3: {0: {0: 0, 1: 1}, 1: {0: 1, 1: 0}},
        },

        # Economics — match both
        'revenue_per_unit': {0: 50, 1: 60},
        'production_cost': {
            0: {0: 8,  1: 10},
            1: {0: 4,  1: 4},
            2: {0: 8,  1: 10},
            3: {0: 4,  1: 4},
        },
        'setup_cost': {0: 0, 1: 20, 2: 0, 3: 20},
        'inventory_cost_per_unit': {0: 0.5, 1: 0.6},
        'backorder_cost_per_unit': {0: 15, 1: 18},

        # Initial WIP (queues 1..3) and FG must be zero for fair comparison
        'initial_inventory': {
            0: {0: 0, 1: 0},   # queue0 starts empty; arrivals_schedule will feed it
            1: {0: 0, 1: 0},
            2: {0: 0, 1: 0},
            3: {0: 0, 1: 0},
            'finished': {0: 0, 1: 0},
        },

        # Schedules (length = H). Fill below by mode.
        'arrivals_schedule': {},   # raw material released to queue0 each period
        'demand_schedule': {},     # external demand each period
    }

    # Totals to match your previous cases (64 each)
    TOTAL_0, TOTAL_1 = 64, 64

    def zero(H): return [0]*H

    if mode.upper() == "ALL_AT_T0":
        arr0 = zero(H); arr1 = zero(H); dem0 = zero(H); dem1 = zero(H)
        arr0[0] = TOTAL_0; arr1[0] = TOTAL_1
        dem0[0] = TOTAL_0; dem1[0] = TOTAL_1
    elif mode.upper() == "UNIFORM":
        # spread evenly by integer division; remainder in earliest slots
        base0, r0 = divmod(TOTAL_0, H)
        base1, r1 = divmod(TOTAL_1, H)
        arr0 = [base0 + (1 if t < r0 else 0) for t in range(H)]
        arr1 = [base1 + (1 if t < r1 else 0) for t in range(H)]
        dem0 = arr0[:]  # choose whether you want demand to mirror arrivals or not
        dem1 = arr1[:]
    else:
        raise ValueError("mode must be ALL_AT_T0 or UNIFORM")

    common['arrivals_schedule'] = {0: arr0, 1: arr1}
    common['demand_schedule']   = {0: dem0, 1: dem1}
    common['demand'] = {0: TOTAL_0, 1: TOTAL_1}  # keep totals for reporting

    return common
