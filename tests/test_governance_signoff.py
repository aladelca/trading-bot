from src.agents.governance_signoff import evaluate_signoff_matrix


def test_signoff_matrix_ready_for_deploy():
    out = evaluate_signoff_matrix(
        {
            "risk_owner_approved": True,
            "ops_owner_approved": True,
            "rollback_plan_attached": True,
            "kpi_snapshot_attached": True,
            "dry_run_validation_passed": True,
        }
    )
    assert out["ok"] is True
    assert out["status"] == "ready-for-deploy"


def test_signoff_matrix_blocked_when_missing_gates():
    out = evaluate_signoff_matrix(
        {
            "risk_owner_approved": True,
            "ops_owner_approved": False,
            "rollback_plan_attached": True,
        }
    )
    assert out["ok"] is False
    assert "ops_owner_approved" in out["missing_gates"]
