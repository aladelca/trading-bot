from __future__ import annotations


REQUIRED_GATES = [
    "risk_owner_approved",
    "ops_owner_approved",
    "rollback_plan_attached",
    "kpi_snapshot_attached",
    "dry_run_validation_passed",
]


def evaluate_signoff_matrix(signoff: dict) -> dict:
    missing = [g for g in REQUIRED_GATES if not bool(signoff.get(g))]
    ok = len(missing) == 0
    return {
        "ok": ok,
        "missing_gates": missing,
        "required_gates": REQUIRED_GATES,
        "status": "ready-for-deploy" if ok else "blocked",
    }
