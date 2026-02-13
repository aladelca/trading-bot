from src.broker.base import BrokerClient, OrderRequest


class QuestradeClient(BrokerClient):
    """Stub adapter. Replace internals once credentials are provided."""

    def __init__(self, client_id: str = "", refresh_token: str = "", practice: bool = True):
        self.client_id = client_id
        self.refresh_token = refresh_token
        self.practice = practice

    def place_order(self, order: OrderRequest) -> dict:
        # TODO: wire to real Questrade endpoint flow (auth token refresh + order route)
        return {
            "status": "paper-simulated",
            "broker": "questrade",
            "symbol": order.symbol,
            "side": order.side,
            "quantity": order.quantity,
            "extended_hours": order.extended_hours,
        }

    def get_buying_power(self) -> float:
        # TODO: replace with real account balance call
        return 10000.0
