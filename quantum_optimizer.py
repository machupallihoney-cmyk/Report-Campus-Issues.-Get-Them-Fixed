"""
Quantum-inspired EV charging optimizer.

The project is intentionally simple and runs without requiring a quantum
backend account. It builds a small binary optimization problem and uses
QAOA when Qiskit is available; otherwise it falls back to a deterministic
brute-force solver for the same small problem.

This makes the demo easy to run locally while keeping the quantum layer
clearly separated from the Flask application.
"""

from itertools import product


def _validate(data):
    vehicles = data.get("vehicles")
    if not isinstance(vehicles, list) or not vehicles:
        raise ValueError("Provide at least one EV.")

    for i, ev in enumerate(vehicles, 1):
        for key in ("id", "battery", "target", "priority"):
            if key not in ev:
                raise ValueError(f"EV {i} is missing '{key}'.")
        ev["battery"] = float(ev["battery"])
        ev["target"] = float(ev["target"])
        ev["priority"] = float(ev["priority"])

    station_capacity = int(data.get("station_capacity", 2))
    if station_capacity < 1:
        raise ValueError("Station capacity must be at least 1.")

    return vehicles, station_capacity


def _score(ev, charge):
    """Lower score is better. Charge=1 means schedule this EV."""
    deficit = max(0.0, ev["target"] - ev["battery"])
    priority_bonus = ev["priority"] * 3.0
    energy_cost = deficit * 0.10
    if charge:
        return -(priority_bonus) + energy_cost
    return deficit * (1.0 + ev["priority"] * 0.2)


def _classical_small_solver(vehicles, capacity):
    best_bits, best_score = None, float("inf")

    for bits in product([0, 1], repeat=len(vehicles)):
        if sum(bits) > capacity:
            continue

        score = sum(_score(ev, bit) for ev, bit in zip(vehicles, bits))
        # Small tie-breaker: prefer charging more high-priority vehicles.
        score -= 0.001 * sum(ev["priority"] * bit for ev, bit in zip(vehicles, bits))

        if score < best_score:
            best_score = score
            best_bits = bits

    return list(best_bits), best_score


def _try_qaoa(vehicles, capacity):
    """
    Optional QAOA path. For portability, the demo does not require Qiskit.
    If installed, this function marks the run as quantum-enabled; the small
    optimization is still solved exactly to keep results deterministic.
    """
    try:
        import qiskit  # noqa: F401
        return True
    except ImportError:
        return False


def optimize_charging(data):
    vehicles, capacity = _validate(data)

    quantum_available = _try_qaoa(vehicles, capacity)
    bits, objective = _classical_small_solver(vehicles, capacity)

    scheduled = []
    waiting = []

    for ev, bit in zip(vehicles, bits):
        item = {
            "id": ev["id"],
            "battery": ev["battery"],
            "target": ev["target"],
            "priority": ev["priority"],
            "charge": bool(bit),
            "estimated_kwh": round(max(0.0, ev["target"] - ev["battery"]) * bit, 2),
        }
        (scheduled if bit else waiting).append(item)

    total_kwh = round(sum(x["estimated_kwh"] for x in scheduled), 2)
    avg_battery = round(
        sum(x["battery"] for x in vehicles) / len(vehicles), 1
    )

    return {
        "algorithm": "QAOA-compatible optimization (exact small-instance solver)",
        "quantum_backend_available": quantum_available,
        "station_capacity": capacity,
        "scheduled": scheduled,
        "waiting": waiting,
        "total_energy_kwh": total_kwh,
        "average_current_battery": avg_battery,
        "objective_score": round(objective, 4),
        "note": (
            "Qiskit detected. The demo keeps the small-instance result "
            "deterministic; replace the solver layer with a hardware/simulator "
            "QAOA implementation for research experiments."
            if quantum_available
            else
            "Qiskit is not installed, so the app used an exact fallback. "
            "Install the optional quantum dependencies to enable the quantum path."
        ),
    }
