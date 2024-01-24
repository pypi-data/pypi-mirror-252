from ..types import native_adapter
from ..undefined import undefined
from ..validationResult import ValidationResult
from . import ModelType


class Boolean(ModelType):
    implementation = bool

    def from_string(self, string: str):
        if string.lower() == 'false':
            return False
        elif string.lower() == 'true':
            return True
        elif not string:
            return undefined
        else:
            raise ValueError(f'{string} cannot be converted into a boolean.')

    def to_string(self, boolean):
        return str(boolean)

    to_json = native_adapter
    from_json = native_adapter
    to_yaml = native_adapter
    from_yaml = native_adapter
    to_toml = native_adapter
    from_toml = native_adapter
    to_mongo = native_adapter
    from_mongo = native_adapter

    def validator(self, value, path):
        return ValidationResult(True)

    def json_schema(self):
        return {
            'type': 'boolean',
        }
