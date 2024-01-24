from datetime import date

from ..validationResult import ValidationResult
from . import ModelType


class Date(ModelType):
    implementation = date

    def from_string(self, string: str):
        try:
            return date.fromisoformat(string)
        except TypeError as err:
            raise ValueError('Invalid date time', string) from err

    def to_string(self, value: date):
        return value.isoformat()

    def validator(self, value, path):
        messages = []
        return ValidationResult(not messages, messages)
