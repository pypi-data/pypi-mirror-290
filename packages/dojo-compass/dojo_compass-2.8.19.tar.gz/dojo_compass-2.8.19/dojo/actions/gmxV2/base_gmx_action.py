"""Base GMX action."""
from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin, LetterCase, dataclass_json

from dojo.actions.base_action import BaseAction
from dojo.observations import GmxV2Obs


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class BaseGmxAction(DataClassJsonMixin, BaseAction[GmxV2Obs]):
    """Base Action for GMX."""

    pass
