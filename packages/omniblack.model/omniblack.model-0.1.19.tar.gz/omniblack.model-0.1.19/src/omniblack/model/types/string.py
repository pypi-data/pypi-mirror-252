from functools import cache
from re import Pattern, compile
from sys import maxsize

from ..field import AttributeFields
from ..localization import TXT
from ..validationResult import ErrorTypes, ValidationMessage, ValidationResult
from . import ModelType


@cache
def create_allowed_chars_re(allowed_chars: str) -> Pattern:
    return compile(rf'[^{allowed_chars}]')


class String(ModelType):
    implementation = str

    def json_schema(self):
        field = self.field
        model = field.model
        attrs = getattr(
            field,
            'string_attrs',
            model.meta_structs.string_attrs(),
        )

        schema = {
            'type': 'string',
            'minLength': attrs.min_len,
            'maxLength': attrs.max_len,
        }

        if 'allowed_chars' in attrs:
            schema['pattern'] = f'^[{attrs.allowed_chars}]*$'

        return schema

    def validator(self, value, path):
        field = self.field
        field_def = field.field_def
        attrs = field_def.string_attrs
        max_len = attrs.max_len
        min_len = attrs.min_len
        allowed_chars = attrs.get('allowed_chars', None)

        messages = []
        if len(value) > max_len:
            messages.append(ValidationMessage(
                ErrorTypes.constraint_error,
                TXT('${path} may not be longer than ${max_len}.', locals()),
                path,
            ))

        elif len(value) < min_len:
            messages.append(ValidationMessage(
                ErrorTypes.constraint_error,
                TXT('${path} may not be shorter than ${min_len}.', locals()),
                path,
            ))

        if allowed_chars:
            sorted_chars = ''.join(sorted(allowed_chars))

            allowed_chars_re = create_allowed_chars_re(sorted_chars)

            if allowed_chars_re.search(value) is not None:
                msg = TXT(
                    '${path} may only contain the characters ${allowed_chars}.',  # noqa: E501
                    locals(),
                )
                messages.append(ValidationMessage(
                    ErrorTypes.constraint_error,
                    msg,
                    path,
                ))

            return ValidationResult(not messages, messages)

    attributes = AttributeFields(
        dict(
            name='allowed_chars',
            display=dict(en='Allowed Characters'),
            desc=dict(
                en='A string of characters that'
                   + "are allowed in the field's values.",
            ),
            type='string',
        ),
        dict(
            name='min_len',
            display=dict(en='Minimum Length'),
            desc=dict(en="The minimum length of the field's value."),
            type='integer',
            assumed=0,
            attrs=dict(
                min=0,
                max=maxsize,
            ),
        ),
        dict(
            name='max_len',
            display=dict(en='Maximum'),
            desc=dict(en="The maximum length of the field's value."),
            type='integer',
            assumed=maxsize,
            attrs=dict(
                min=0,
                max=maxsize,
            ),
        ),
    )
