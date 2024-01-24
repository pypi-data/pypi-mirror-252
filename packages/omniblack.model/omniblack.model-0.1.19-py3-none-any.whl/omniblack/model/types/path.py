from pathlib import Path as PathImpl
from os import fspath

from ..validationResult import ValidationResult
from . import ModelType


class Path(ModelType):
    implementation = PathImpl

    def from_string(self, string: str):
        try:
            return self.implementation(string)
        except TypeError as err:
            raise ValueError('Invalid path', string) from err

    def to_string(self, value: PathImpl):
        return fspath(value)

    def validator(self, path):
        messages = []
        return ValidationResult(not messages, messages)
