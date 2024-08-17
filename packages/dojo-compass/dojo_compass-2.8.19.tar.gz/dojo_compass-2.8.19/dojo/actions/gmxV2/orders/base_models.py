"""Order actions for GMX v2."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from dataclasses_json import LetterCase, dataclass_json

from dojo.actions.gmxV2.action_validation import validate_kwargs
from dojo.actions.gmxV2.base_gmx_action import BaseGmxAction
from dojo.actions.gmxV2.orders.params import CreateOrderParams, DecreasePositionSwapType
from dojo.agents import BaseAgent
from dojo.models.gmxV2.market import _get_gmx_markets


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Order(BaseGmxAction):
    """Base action representing an order."""

    create_order_params: CreateOrderParams
    gas: Optional[int] = None
    gas_price: Optional[int] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class HistoricOrder(Order):
    """Action representing a historical order event on GMX v2."""

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class BaseTraderOrder(Order, ABC):
    """Base trader order action on GMX v2."""

    @classmethod
    @abstractmethod
    def from_parameters(cls, **kwargs: dict[str, Any]) -> Any:
        """Create a trader order from parameters."""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LimitOrder(BaseTraderOrder):
    """Action representing a limit order on GMX v2."""

    @classmethod  # type: ignore
    @validate_kwargs(
        {
            "agent",
            "initial_collateral_delta_amount",
            "trigger_price",
            "acceptable_price",
            "market_key",
            "token_in_symbol",
            "collateral_token_symbol",
            "is_long",
            "slippage",
        }
    )
    def from_parameters(cls, **kwargs: dict[str, Any]) -> "LimitOrder":
        """Class method to generate a limit order from parameters."""
        agent: BaseAgent = kwargs["agent"]  # type: ignore
        initial_collateral_delta_amount: int = kwargs["initial_collateral_delta_amount"]  # type: ignore
        trigger_price: int = kwargs["trigger_price"]  # type: ignore
        acceptable_price: int = kwargs["acceptable_price"]  # type: ignore
        market_key: str = kwargs["market_key"]  # type: ignore
        token_in_symbol: str = kwargs["token_in_symbol"]  # type: ignore
        collateral_token_symbol: str = kwargs["collateral_token_symbol"]  # type: ignore
        is_long: bool = kwargs["is_long"]  # type: ignore
        _ = kwargs["slippage"]

        market_key_to_market = _get_gmx_markets(
            chain=agent.backend.chain, backend=agent.backend
        )
        market = market_key_to_market[market_key]
        swap_path: list[str] = []
        if token_in_symbol not in {
            market.long_token.symbol,
            market.short_token.symbol,
        }:
            # TODO implement swap path, currently only supports collateral token as long or short
            # swap_path = _get_swap_path(market_key_to_market)
            pass

        # TODO implement leverage logic here when the oracle prices are available
        initial_collateral_token = (
            market.long_token.address
            if collateral_token_symbol == market.long_token.symbol
            else market.short_token.address
        )
        addresses = {
            "receiver": agent.original_address,
            "account": agent.original_address,
            "initial_collateral_token": initial_collateral_token,
            "market": market.market_token.address,
            "swap_path": swap_path,
        }
        numbers = {
            "size_delta_usd": 10**16,  # TODO add this after leverage is added
            "initial_collateral_delta_amount": initial_collateral_delta_amount,
            "trigger_price": trigger_price,
            "acceptable_price": acceptable_price,  # TODO add this after leverage is added
            "execution_fee": 10
            ** 16,  # TODO calculate this - there is a ticket for this
            "callback_gas_limit": 0,
            "min_output_amount": 0,
        }
        create_order_params = {
            "addresses": addresses,
            "numbers": numbers,
            "order_type": cls.ORDER_TYPE,  # type: ignore
            "decrease_position_swap_type": DecreasePositionSwapType.NO_SWAP,
            "is_long": is_long,
            "should_unwrap_native_token": False,
            "auto_cancel": False,
        }
        return cls.from_dict(
            {"create_order_params": create_order_params, "agent": agent}
        )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MarketOrder(LimitOrder):
    """Action representing a market order on GMX v2."""

    @classmethod  # type: ignore
    @validate_kwargs(
        {
            "agent",
            "initial_collateral_delta_amount",
            "market_key",
            "token_in_symbol",
            "collateral_token_symbol",
            "is_long",
            "slippage",
        }
    )
    def from_parameters(cls, **kwargs: dict[str, Any]) -> "MarketOrder":
        """Create a market order from parameters.

        Expected parameters:
        - agent: BaseAgent
        - initial_collateral_delta_amount: int, the amount of collateral to be used in the order
        - market_key: str, the format of this key is "index_token:long_token:short_token"
        - token_in_symbol: str, the symbol of the token to be used in the order
        - collateral_token_symbol: str, the symbol of the collateral token either long or short
        - is_long: bool, True if the order is long, False otherwise
        - slippage: int, the slippage tolerance for the order in basis points
        """
        # TODO once the oracle prices are available, add trigger price and acceptable price
        kwargs["trigger_price"] = 0  # type: ignore
        kwargs["acceptable_price"] = 0  # type: ignore
        return super().from_parameters(**kwargs)  # type: ignore


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LongMarketOrder(MarketOrder):
    """Action representing a long market order on GMX v2."""

    @classmethod  # type: ignore
    @validate_kwargs(
        {
            "agent",
            "initial_collateral_delta_amount",
            "market_key",
            "token_in_symbol",
            "collateral_token_symbol",
            "slippage",
        }
    )
    def from_parameters(cls, **kwargs: dict[str, Any]) -> "LongMarketOrder":
        """Create a long market order from parameters."""
        kwargs["is_long"] = True  # type: ignore
        return super().from_parameters(**kwargs)  # type: ignore


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ShortMarketOrder(MarketOrder):
    """Action representing a long market order on GMX v2."""

    @classmethod  # type: ignore
    @validate_kwargs(
        {
            "agent",
            "initial_collateral_delta_amount",
            "market_key",
            "token_in_symbol",
            "collateral_token_symbol",
            "slippage",
        }
    )
    def from_parameters(cls, **kwargs: dict[str, Any]) -> "ShortMarketOrder":
        """Create a long market order from parameters."""
        kwargs["is_long"] = False  # type: ignore
        return super().from_parameters(**kwargs)  # type: ignore


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LongLimitOrder(LimitOrder):
    """Action representing a limit order on GMX v2."""

    @classmethod  # type: ignore
    @validate_kwargs(
        {
            "agent",
            "initial_collateral_delta_amount",
            "trigger_price",
            "acceptable_price",
            "market_key",
            "token_in_symbol",
            "collateral_token_symbol",
            "slippage",
        }
    )
    def from_parameters(cls, **kwargs: dict[str, Any]) -> "LongLimitOrder":
        """Create a long limit order from parameters."""
        kwargs["is_long"] = True  # type: ignore
        return super().from_parameters(**kwargs)  # type: ignore


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ShortLimitOrder(LimitOrder):
    """Action representing a limit order on GMX v2."""

    @classmethod  # type: ignore
    @validate_kwargs(
        {
            "agent",
            "initial_collateral_delta_amount",
            "trigger_price",
            "acceptable_price",
            "market_key",
            "token_in_symbol",
            "collateral_token_symbol",
            "slippage",
        }
    )
    def from_parameters(cls, **kwargs: dict[str, Any]) -> "LongLimitOrder":
        """Create a short limit order from parameters."""
        kwargs["is_long"] = False  # type: ignore
        return super().from_parameters(**kwargs)  # type: ignore


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class StopLossOrder(LimitOrder):
    """Action representing a stop loss order on GMX v2."""

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TakeProfitOrder(LimitOrder):
    """Action representing a take profit order on GMX v2."""

    pass
