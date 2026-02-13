from src.broker.base import OrderRequest


class PaperExecutionEngine:
    def execute(self, symbol: str, side: str, quantity: int, extended_hours: bool = True) -> dict:
        return {
            "status": "filled",
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "extended_hours": extended_hours,
            "mode": "paper",
        }
