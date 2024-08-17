"""Set of functions to get parameters for interaction with GMX contracts."""
from typing import Any

from hexbytes import HexBytes

from dojo.actions.gmxV2.deposit.models import Deposit
from dojo.actions.gmxV2.orders.base_models import Order
from dojo.actions.gmxV2.orders.params import (
    CreateOrderParamsAddresses,
    CreateOrderParamsNumbers,
)


def _get_create_deposit_args(deposit_action: Deposit) -> list[Any]:
    """Return arguments to encode in `createDeposit` function."""
    return [
        deposit_action.create_deposit_params.addresses.receiver,
        deposit_action.create_deposit_params.addresses.callback_contract,
        deposit_action.create_deposit_params.addresses.ui_fee_receiver,
        deposit_action.create_deposit_params.addresses.market,
        deposit_action.create_deposit_params.addresses.initial_long_token,
        deposit_action.create_deposit_params.addresses.initial_short_token,
        deposit_action.create_deposit_params.addresses.long_token_swap_path,
        deposit_action.create_deposit_params.addresses.short_token_swap_path,
        deposit_action.create_deposit_params.numbers.min_market_tokens,
        deposit_action.create_deposit_params.should_unwrap_native_token,
        deposit_action.create_deposit_params.numbers.execution_fee,
        deposit_action.create_deposit_params.numbers.callback_gas_limit,
    ]


def _get_create_order_args_addresses(
    order_action_addresses: CreateOrderParamsAddresses,
) -> tuple[str, str, str, str, str | None, str | None, list[str]]:
    return (
        order_action_addresses.receiver,
        order_action_addresses.cancellation_receiver,
        order_action_addresses.callback_contract,
        order_action_addresses.ui_fee_receiver,
        order_action_addresses.market,
        order_action_addresses.initial_collateral_token,
        order_action_addresses.swap_path or [],
    )


def _get_create_order_args_numbers(
    order_action_numbers: CreateOrderParamsNumbers,
) -> tuple[int, int, int, int, int, int, int]:
    return (
        order_action_numbers.size_delta_usd,
        order_action_numbers.initial_collateral_delta_amount,
        order_action_numbers.trigger_price,
        order_action_numbers.acceptable_price,
        order_action_numbers.execution_fee,
        order_action_numbers.callback_gas_limit,
        order_action_numbers.min_output_amount,
    )


def _get_create_order_args(
    order_action: Order,
) -> tuple[
    tuple[str, str, str, str, str | None, str | None, list[str]],
    tuple[int, int, int, int, int, int, int],
    int,
    int,
    bool,
    bool,
    bool,
    HexBytes,
]:
    """Return arguments to encode in `createOrder` function."""
    addresses = _get_create_order_args_addresses(
        order_action.create_order_params.addresses
    )
    numbers = _get_create_order_args_numbers(order_action.create_order_params.numbers)
    return (
        addresses,
        numbers,
        order_action.create_order_params.order_type.value,
        order_action.create_order_params.decrease_position_swap_type.value,
        order_action.create_order_params.is_long,
        order_action.create_order_params.should_unwrap_native_token,
        order_action.create_order_params.autoCancel,
        HexBytes(order_action.create_order_params.referral_code),
    )
