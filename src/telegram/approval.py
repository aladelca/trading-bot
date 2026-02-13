from dataclasses import asdict

from src.signals.models import TradeSignal


class ApprovalGate:
    """Telegram approval placeholder.

    In v1 scaffold we simulate a required approval and return True by default.
    Replace with real Telegram API callback flow.
    """

    def request(self, signal: TradeSignal) -> bool:
        payload = asdict(signal)
        print("APPROVAL_REQUEST", payload)
        return True
