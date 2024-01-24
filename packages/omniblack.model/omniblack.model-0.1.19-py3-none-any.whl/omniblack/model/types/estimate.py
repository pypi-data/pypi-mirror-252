from sys import float_info

from ..field import AttributeFields
from ..localization import TXT
from ..types import native_adapter
from ..validationResult import ErrorTypes, ValidationMessage, ValidationResult
from . import ModelType


class Estimate(ModelType):
    implementation = float

    def from_string(self, string):
        return float(string)

    def to_string(self, num):
        return str(num)

    to_json = native_adapter
    from_json = native_adapter
    to_yaml = native_adapter
    from_yaml = native_adapter
    to_toml = native_adapter
    from_toml = native_adapter

    def validator(self, value, path):
        messages = []

        field_def = self.field.field_def
        attrs = field_def.estimate_attrs
        max = attrs.max
        min = attrs.min

        if value > max:
            messages.append(ValidationMessage(
                ErrorTypes.constraint_error,
                TXT('${path} must not be greater than ${max}.', locals()),
                path,
            ))
        elif value < min:
            messages.append(ValidationMessage(
                ErrorTypes.constraint_error,
                TXT('${path} must not be less than ${min}.', locals()),
                path,
            ))

        return ValidationResult(not messages, messages)

    attributes = AttributeFields(
        dict(
            name='min',
            display=dict(en='Minimum'),
            desc=dict(en='The minimum value allowed for this field.'),
            type='integer',
            assumed=float_info.min,
        ),
        dict(
            name='max',
            display=dict(en='Maximum'),
            desc=dict(en='The maximum value allowed for this field.'),
            type='integer',
            assumed=float_info.max,
        ),
    )
