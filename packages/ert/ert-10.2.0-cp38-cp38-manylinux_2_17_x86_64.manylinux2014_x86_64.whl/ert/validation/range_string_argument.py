from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .active_range import ActiveRange
from .argument_definition import ArgumentDefinition
from .validation_status import ValidationStatus

if TYPE_CHECKING:
    from ..storage import Storage


class RangeStringArgument(ArgumentDefinition):
    NOT_A_VALID_RANGE_STRING = (
        "The input should be of the type: "
        "<b><pre>\n\t1,3-5,9,17\n</pre></b>"
        "i.e. integer values separated by commas, and dashes to represent ranges."
    )
    VALUE_NOT_IN_RANGE = "A value must be in the range from 0 to %d."

    def __init__(self, max_value: Optional[int] = None, **kwargs: bool) -> None:
        super().__init__(**kwargs)
        self.__max_value = max_value

    def validate(self, token: str) -> ValidationStatus:
        validation_status = super().validate(token)

        if not validation_status:
            return validation_status

        try:
            ActiveRange.validate_rangestring(token)
        except ValueError:
            validation_status.setFailed()
            validation_status.addToMessage(RangeStringArgument.NOT_A_VALID_RANGE_STRING)

        if self.__max_value is not None:
            try:
                ActiveRange.validate_rangestring_vs_length(token, self.__max_value)
            except ValueError:
                validation_status.setFailed()
                validation_status.addToMessage(
                    RangeStringArgument.VALUE_NOT_IN_RANGE % (self.__max_value - 1)
                )

        validation_status.setValue(token)

        return validation_status


class NotInStorage(ArgumentDefinition):
    def __init__(self, storage: Storage, prop: str) -> None:
        self.storage = storage
        self.prop = prop

    def validate(self, token: str) -> ValidationStatus:
        validation_status = ValidationStatus()

        existing = [exp.name for exp in getattr(self.storage, self.prop)]
        if token in existing:
            validation_status.setFailed()
            validation_status.addToMessage(
                f"{self.prop.capitalize()} name must be unique, not one of: {existing}"
            )

        validation_status.setValue(token)

        return validation_status
