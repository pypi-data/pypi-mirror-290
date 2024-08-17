"""Actions for keepers to execute on GMX v2."""
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json

from dojo.actions.gmxV2.base_gmx_action import BaseGmxAction


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class KeeperAction(BaseGmxAction):
    """Action representing a keeper action on GMX v2."""

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class HistoricDepositExecuted(KeeperAction):
    """Action representing an order execution event on GMX v2."""

    pass
