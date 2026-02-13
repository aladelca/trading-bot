from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class OrderRequest:
    symbol: str
    side: str
    quantity: int
    order_type: str = "market"
    extended_hours: bool = True


class BrokerClient(ABC):
    @abstractmethod
    def place_order(self, order: OrderRequest) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_buying_power(self) -> float:
        raise NotImplementedError
