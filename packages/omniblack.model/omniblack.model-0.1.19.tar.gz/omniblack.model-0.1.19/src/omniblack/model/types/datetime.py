from datetime import datetime

from ..validationResult import ValidationResult
from . import ModelType


class Datetime(ModelType):
    implementation = datetime

    def from_string(self, string: str):
        try:
            return datetime.fromisoformat(string)
        except TypeError as err:
            raise ValueError('Invalid date time', string) from err

    def to_string(self, value: datetime):
        return value.isoformat()

    def validator(self, value, path):
        messages = []
        return ValidationResult(not messages, messages)
