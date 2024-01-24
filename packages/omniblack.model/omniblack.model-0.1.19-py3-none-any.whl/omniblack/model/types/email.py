from email_validator import validate_email, EmailNotValidError

from ..types import native_adapter
from ..validationResult import ErrorTypes, ValidationMessage, ValidationResult
from . import ModelType


class Email(ModelType):
    to_string = native_adapter
    from_string = native_adapter

    implementation = str

    def validator(self, value, path):
        messages = []

        try:
            validate_email(value)
        except EmailNotValidError as err:
            messages.append(
                ValidationMessage(ErrorTypes.invalid_value, str(err), [path]),
            )

        return ValidationResult(not messages, messages)

    def json_schema(self):
        return {
            'type': 'string',
            'format': 'idn-email',
        }
