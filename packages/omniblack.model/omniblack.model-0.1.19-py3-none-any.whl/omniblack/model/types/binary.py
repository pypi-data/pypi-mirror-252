from base64 import b64decode, b64encode
from binascii import Error as B64Error
from sys import maxsize

from humanize import naturalsize as natural_size

from ..field import AttributeFields
from ..localization import TXT
from ..types import native_adapter
from ..validationResult import ErrorTypes, ValidationMessage, ValidationResult
from . import ModelType


class Binary(ModelType):
    implementation = bytes

    to_yaml = native_adapter
    from_yaml = native_adapter
    to_mongo = native_adapter
    from_mongo = native_adapter

    def from_string(string: str, field):
        try:
            return b64decode(string, validate=True)
        except B64Error as err:
            raise ValueError('Invalid base64 data.') from err

    def to_string(value: bytes, field):
        return b64encode(value).decode('ascii')

        def json_schema(self):
            return {
                'type': 'string',
                'pattern': '^[a-zA-Z0-9+/]*=?$'
            }

    def validator(self, value, path):
        field_def = self.field.field_def
        attrs = field_def.binary_attrs

        messages = []
        if len(value) < attrs.min:
            min_human = natural_size(attrs.min, binary=True)
            messages.append(ValidationMessage(
                ErrorTypes.constraint_error,
                TXT('${path} must not be less than ${min_human}.', locals()),
                path,
            ))
        elif len(value) > attrs.max:
            max_human = natural_size(attrs.max, binary=True)
            messages.append(ValidationMessage(
                ErrorTypes.constraint_error,
                TXT(
                    '${path} must not be greater than ${max_human}.',
                    locals(),
                ),
                path,
            ))

        return ValidationResult(not messages, messages)

    attributes = AttributeFields(
        dict(
            name='min',
            display=dict(en='Minimum'),
            desc=dict(en="The minimum size of the field's data, in bytes."),
            type='integer',
            assumed=0,
            attrs=dict(
                min=0,
                max=maxsize,
            ),
        ),
        dict(
            name='max',
            display=dict(en='Maximum'),
            desc=dict(en="The maximum size of the field's data, in bytes."),
            type='integer',
            assumed=maxsize,
            attrs=dict(
                min=0,
                max=maxsize,
            ),
        ),
    )
