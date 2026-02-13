from dataclasses import asdict

from src.signals.models import TradeSignal


class ApprovalGate:
    """Approval placeholder.

    required=True: currently auto-approves while printing payload.
    required=False: bypasses approval gate.
    Replace with real Telegram callback flow.
    """

    def __init__(self, required: bool = True):
        self.required = required

    def request(self, signal: TradeSignal) -> bool:
        if not self.required:
            return True
        payload = asdict(signal)
        print("APPROVAL_REQUEST", payload)
        return True
