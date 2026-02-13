from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ReplayScenario:
    confidence: float
    pnl_outcome: float
    approved: bool


def evaluate_threshold(scenarios: list[ReplayScenario], threshold: float) -> dict:
    selected = [s for s in scenarios if s.confidence >= threshold]
    if not selected:
        return {
            "threshold": threshold,
            "selected": 0,
            "approval_rate": 0.0,
            "avg_pnl": 0.0,
            "score": -999.0,
        }

    approvals = sum(1 for s in selected if s.approved)
    approval_rate = approvals / len(selected)
    avg_pnl = sum(float(s.pnl_outcome) for s in selected) / len(selected)

    # conservative scoring: reward pnl + approval quality, penalize over-trading.
    trade_penalty = len(selected) * 0.001
    score = (avg_pnl * 0.7) + (approval_rate * 0.3) - trade_penalty

    return {
        "threshold": round(float(threshold), 4),
        "selected": len(selected),
        "approval_rate": round(approval_rate, 6),
        "avg_pnl": round(avg_pnl, 6),
        "score": round(score, 6),
    }


def calibrate_thresholds(
    scenarios: list[ReplayScenario],
    candidate_thresholds: list[float],
) -> dict:
    evaluations = [evaluate_threshold(scenarios, t) for t in candidate_thresholds]
    ranked = sorted(evaluations, key=lambda x: (x["score"], x["avg_pnl"]), reverse=True)
    best = ranked[0] if ranked else None
    return {
        "best": best,
        "ranked": ranked,
    }
