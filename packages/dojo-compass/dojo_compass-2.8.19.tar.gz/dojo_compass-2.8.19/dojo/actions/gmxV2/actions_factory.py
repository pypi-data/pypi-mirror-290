"""Set of functions to create actions from event data."""
from collections import defaultdict
from typing import Any

from dojo.actions.gmxV2.base_gmx_action import BaseGmxAction
from dojo.actions.gmxV2.deposit.models import HistoricDeposit
from dojo.actions.gmxV2.orders.base_models import HistoricOrder
from dojo.actions.gmxV2.orders.params import DecreasePositionSwapType, OrderType
from dojo.agents.base_agent import BaseAgent


def _get_addresses(raw_addresses: list[dict[str, Any]]) -> dict[str, str]:
    addresses = {}
    for item in raw_addresses:
        key, value = item.values()
        addresses[key] = value
    return addresses


def _get_bools(raw_bools: list[dict[str, Any]]) -> dict[str, bool]:
    return {item["key"]: item["value"] for item in raw_bools}


def _get_numbers(
    raw_numbers: list[dict[str, Any]],
) -> tuple[
    dict[Any, Any], OrderType | None, DecreasePositionSwapType | None, Any | None
]:
    numbers = {}
    order_type = None
    decrease_position_swap_type = None
    block_number = None

    for item in raw_numbers:
        if item["key"] == "orderType":
            order_type = OrderType(item["value"])
        elif item["key"] == "decreasePositionSwapType":
            decrease_position_swap_type = DecreasePositionSwapType(item["value"])
        elif item["key"] == "updatedAtBlock":
            block_number = item["value"]
        else:
            numbers[item["key"]] = item["value"]
    return numbers, order_type, decrease_position_swap_type, block_number


def _create_market_order(
    event_data: dict[str, Any], agent: BaseAgent
) -> tuple[HistoricOrder, Any | None, Any]:
    """Class method to instantiate an CreateOrder object from event data."""
    addresses = _get_addresses(event_data["addressItems"]["items"])
    (
        numbers,
        order_type,
        decrease_position_swap_type,
        block_number,
    ) = _get_numbers(event_data["uintItems"]["items"])
    bools = _get_bools(event_data["boolItems"]["items"])
    original_key = event_data["bytes32Items"]["items"][0]["value"]
    return (
        HistoricOrder.from_dict(
            {
                "create_order_params": {
                    "addresses": addresses,
                    "numbers": numbers,
                    "order_type": order_type,
                    "decrease_position_swap_type": decrease_position_swap_type,
                    **bools,
                },
                "agent": agent,
            }
        ),
        block_number,
        original_key,
    )


def _create_market_deposit(
    event_data: dict[str, Any], agent: BaseAgent
) -> tuple[HistoricDeposit, Any | None, None]:
    """Class method to instantiate an HistoricDeposit object from event data."""
    addresses = _get_addresses(event_data["addressItems"]["items"])
    (numbers, _, _, block_number) = _get_numbers(event_data["uintItems"]["items"])
    bools = _get_bools(event_data["boolItems"]["items"])
    original_key = event_data["bytes32Items"]["items"][0]["value"]
    return (
        HistoricDeposit.from_dict(
            {
                "create_deposit_params": {
                    "addresses": addresses,
                    "numbers": numbers,
                    **bools,
                },
                "agent": agent,
            }
        ),
        block_number,
        original_key,
    )


def _events_to_actions(
    events: list[dict[str, Any]], agent: BaseAgent
) -> tuple[defaultdict[Any | None, list[BaseGmxAction]], dict[Any, BaseGmxAction],]:

    block_to_actions = defaultdict(list)
    original_key_to_action: dict[str, BaseGmxAction] = {}
    event_name_to_action = {
        "OrderCreated": _create_market_order,
        "DepositCreated": _create_market_deposit,
    }
    for event in events:
        factory_method = event_name_to_action.get(event["event_data"]["eventName"])
        if factory_method is not None:
            action, block_number, original_key = factory_method(
                event["event_data"]["eventData"], agent
            )
            block_to_actions[block_number].append(action)
            if original_key:
                original_key_to_action[original_key] = action

    return block_to_actions, original_key_to_action
