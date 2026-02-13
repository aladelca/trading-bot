from apps.backtester.weekly_postmortem import generate_weekly_postmortem
from src.storage.audit_log import AuditLogger


def test_generate_weekly_postmortem_file(tmp_path):
    audit_db = str(tmp_path / "audit.db")
    portfolio_db = str(tmp_path / "portfolio.db")
    out_dir = str(tmp_path / "reports")

    audit = AuditLogger(audit_db)
    audit.log("approval", {"approved": True})

    out_path = generate_weekly_postmortem(
        audit_db=audit_db,
        portfolio_db=portfolio_db,
        baseline={"approval_rate": 0.5, "equity_pnl_total": 0, "signals_rejected": 0},
        out_dir=out_dir,
    )
    assert out_path.endswith(".md")
