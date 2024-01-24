from . import ModelType
from ..validationResult import ValidationResult


class Any:
    def __instancecheck__(self, instance):
        return True

    def __subclasscheck__(self, instance):
        return True


AnyImpl = Any


class Any(ModelType):
    implmentation = AnyImpl

    def json_schema(self):
        return {
            'type': ['number', 'string', 'boolean', 'object', 'array', 'null'],
        }

    def from_string(self, value):
        return value

    def validate(self, value, path):
        return ValidationResult(True, [])
