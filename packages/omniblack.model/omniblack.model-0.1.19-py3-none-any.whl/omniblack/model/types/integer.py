from ..field import AttributeFields
from ..localization import TXT
from ..validationResult import ErrorTypes, ValidationMessage, ValidationResult
from . import ModelType

max_64bit = (2**63)-1
min_64bit = -2**63

max_32bit = (2**31)-1
min_32bit = (-2**31)


def native_64_bit_to(self, value):
    if value in range(min_64bit, max_64bit+1):
        return value
    else:
        str(value)


def native_32_bit_to(self, value):
    if value in range(min_32bit, max_32bit+1):
        return value
    else:
        str(value)


def native_or_str(self, value):
    if isinstance(value, str):
        return int(value, 10)
    else:
        return value


class Integer(ModelType):
    implementation = int

    def to_string(self, integer):
        return str(integer)

    def from_string(self, string):
        return int(string, 10)

    to_mongo = native_64_bit_to
    from_mongo = native_or_str

    to_toml = native_64_bit_to
    from_toml = native_or_str

    to_json = native_32_bit_to
    from_json = native_or_str

    to_yaml = native_32_bit_to
    from_yaml = native_or_str

    def validator(self, value, path):
        field_def = self.field.field_def
        attrs = field_def.integer_attrs
        max = attrs.max
        min = attrs.min

        messages = []
        if max is not None and value > max:
            messages.append(ValidationMessage(
                ErrorTypes.constraint_error,
                TXT('${value} must not be greater than ${max}.', locals()),
                path,
            ))

        elif min is not None and value < min:
            messages.append(ValidationMessage(
                ErrorTypes.constraint_error,
                TXT('${value} must not be less than ${min}.', locals()),
                path,
            ))

        return ValidationResult(not messages, messages)

    def json_schema(self):
        attrs = self.field.integer_attrs

        schema = {
            'type': 'integer',
        }

        if attrs.get('min') is not None:
            schema['minimum'] = attrs.min

        if attrs.get('max') is not None:
            schema['maximum'] = attrs.max

        return schema

    attributes = AttributeFields(
        dict(
            name='min',
            display=dict(en='Minimum'),
            desc=dict(en='The minimum value allowed for this field.'),
            type='integer',
        ),
        dict(
            name='max',
            display=dict(en='Maximum'),
            desc=dict(en='The maximum value allowed for this field.'),
            type='integer',
        ),
    )
