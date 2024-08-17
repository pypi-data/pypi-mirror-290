"""User exposed models for order creation on GMXv2."""
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json

from dojo.actions.gmxV2.orders.base_models import (
    LongLimitOrder,
    LongMarketOrder,
    ShortLimitOrder,
    ShortMarketOrder,
)
from dojo.actions.gmxV2.orders.params import OrderType


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class IncreaseLongMarketOrder(LongMarketOrder):
    """Action representing an increase long market order on GMX v2."""

    ORDER_TYPE: OrderType = OrderType.MARKET_INCREASE


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DecreaseLongMarketOrder(LongMarketOrder):
    """Action representing an decrease long market order on GMX v2."""

    ORDER_TYPE: OrderType = OrderType.MARKET_DECREASE


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class IncreaseShortMarketOrder(ShortMarketOrder):
    """Action representing an increase short market order on GMX v2."""

    ORDER_TYPE: OrderType = OrderType.MARKET_INCREASE


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DecreaseShortMarketOrder(ShortMarketOrder):
    """Action representing an decrease short market order on GMX v2."""

    ORDER_TYPE: OrderType = OrderType.MARKET_DECREASE


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class IncreaseLongLimitOrder(LongLimitOrder):
    """Action representing an increase long limit order on GMX v2."""

    ORDER_TYPE: OrderType = OrderType.LIMIT_INCREASE


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DecreaseLongLimitOrder(LongLimitOrder):
    """Action representing an decrease long limit order on GMX v2."""

    ORDER_TYPE: OrderType = OrderType.LIMIT_DECREASE


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class IncreaseShortLimitOrder(ShortLimitOrder):
    """Action representing an increase short limit order on GMX v2."""

    ORDER_TYPE: OrderType = OrderType.LIMIT_INCREASE


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DecreaseShortLimitOrder(ShortLimitOrder):
    """Action representing a decrease short limit order on GMX v2."""

    ORDER_TYPE: OrderType = OrderType.LIMIT_DECREASE
