"""Parameters required to communicate with GMX v2 deposit withdrawal."""
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CreateWithdrawalParamsAddresses:
    """Addresses required to create a withdrawal on GMX v2."""

    receiver: str
    callback_contract: str
    ui_fee_receiver: str
    market: str
    long_token_swap_path: list[str]
    short_token_swap_path: list[str]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CreateWithdrawalParamsNumbers:
    """Numbers required to create a withdrawal on GMX v2."""

    min_long_token_amount: int
    min_short_token_amount: int
    execution_fee: int
    callback_gas_limit: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CreateWithdrawalParams:
    """Parameters required to create a withdrawal on GMX v2."""

    addresses: CreateWithdrawalParamsAddresses
    numbers: CreateWithdrawalParamsNumbers
    should_unwrap_native_token: bool
