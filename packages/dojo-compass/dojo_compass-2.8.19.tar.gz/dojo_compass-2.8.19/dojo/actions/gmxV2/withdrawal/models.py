"""Withdrawal action models for GMX v2."""
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json

from dojo.actions.gmxV2.base_gmx_action import BaseGmxAction


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Withdrawal(BaseGmxAction):
    """Action representing a withdrawal on GMX v2."""

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class HistoricWithdrawal(Withdrawal):
    """Action representing a historical withdrawal event on GMX v2."""

    pass
