from __future__ import annotations

import argparse
import json
import os

from src.agents.governance_ledger import list_governance_versions, record_governance_version
from src.storage.audit_log import AuditLogger


def main() -> None:
    p = argparse.ArgumentParser(description="Governance recommendation versioning ledger")
    p.add_argument("--recommendation-id", required=True)
    p.add_argument("--version-tag", required=True)
    p.add_argument("--status", required=True)
    p.add_argument("--decided-by", default="human")
    p.add_argument("--payload-json", default="{}")
    p.add_argument("--list-only", action="store_true")
    args = p.parse_args()

    audit = AuditLogger(os.getenv("AUDIT_DB_PATH", "data/audit.db"))

    if not args.list_only:
        payload = json.loads(args.payload_json)
        record_governance_version(
            audit,
            recommendation_id=args.recommendation_id,
            version_tag=args.version_tag,
            status=args.status,
            decided_by=args.decided_by,
            payload=payload,
        )

    out = list_governance_versions(audit, recommendation_id=args.recommendation_id)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
