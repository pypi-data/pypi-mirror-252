from enum import Enum

from ..validationResult import ValidationResult
from ..field import AttributeFields
from . import ModelType


class EnumBase(Enum):
    @classmethod
    def _missing_(cls, value):
        return cls.name_to_member.get(value)

    def __repr__(self):
        cls = self.__class__
        display = cls.displays[self.value]

        return f'{cls.__name__}({display["en"]})'

    def __rich_repr__(self):
        yield from self.choice.items()


class Choice(ModelType):
    def from_string(self, string: str):
        enum_cls = self.get_implementation()

        try:
            return enum_cls[string]
        except KeyError as err:
            raise ValueError('Value is not valid') from err

    def to_string(self, value):
        return str(value)

    def validator(self, value, path):
        return ValidationResult(True, tuple())

    def prepare_metadata(self):
        names = []
        displays = []
        descriptions = []

        field = self.field
        field_def = field.field_def

        for choice in field_def.choice_attrs.choices:
            descriptions.append(getattr(choice, 'desc', None))
            displays.append(choice.display)

            if choice.get('internal'):
                names.append(choice['internal'])
            else:
                names.append(choice['name'])

        enum_name = field_def.choice_attrs.enum_name

        enum_cls = EnumBase(
            enum_name,
            names,
            start=0,
            module=field.model.module_name,
        )

        enum_cls.displays = displays
        enum_cls.descriptions = descriptions

        enum_cls.name_to_member = {}

        for choice in field_def.choice_attrs.choices:
            if choice.get('internal'):
                member = enum_cls[choice.internal]
                enum_cls.name_to_member[choice.name] = member
            else:
                member = enum_cls[choice.name]

            member.choice = choice

        field.metadata.enum_cls = enum_cls

        field.model.expose(enum_name, enum_cls)

    def get_implementation(self):
        return self.field.metadata.enum_cls

    def json_schema(self):
        all_choices = self.field.choice_attrs.choices

        valid_values = [
            choice.name
            for choice in all_choices
        ]

        return {
            'type': 'string',
            'enum': valid_values,
        }

    attributes = AttributeFields(
        dict(
            name='enum_name',
            type='string',
            display=dict(en='Enum Name'),
            desc=dict(en='The name of the enum class in code.'),
            required=True,
        ),
        dict(
            name='choices',
            type='child',
            display=dict(en='Choices'),
            desc=dict(en='The choices this field is limited to.'),
            list=True,
            required=True,
            child_attrs=dict(struct='choice_member'),
        ),
        required=True,
    )
