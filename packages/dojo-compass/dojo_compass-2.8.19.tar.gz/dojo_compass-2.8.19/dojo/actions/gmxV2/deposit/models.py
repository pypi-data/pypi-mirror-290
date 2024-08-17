"""Deposit actions for GMX."""
from dataclasses import dataclass
from typing import Any, Optional

from dataclasses_json import LetterCase, dataclass_json

from dojo.actions.gmxV2.base_gmx_action import BaseGmxAction
from dojo.actions.gmxV2.deposit.params import CreateDepositParams


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Deposit(BaseGmxAction):
    """Base LP order action on GMX v2."""

    create_deposit_params: CreateDepositParams
    gas: Optional[int] = None
    gas_price: Optional[int] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class HistoricDeposit(Deposit):
    """Action representing a historical LP order event on GMX v2."""

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LPDeposit(Deposit):
    """Action representing a LP deposit on GMX v2."""

    @classmethod
    def from_parameters(cls, **kwargs: dict[str, Any]) -> None:
        """Create a LP deposit from parameters."""
        pass
