from importlib.resources import files
from typing import Literal
from json import load

from .abc import Registry
from .errors import CoercionError
from .field import AttributeFields

from .types.binary import Binary
from .types.boolean import Boolean
from .types.child import Child
from .types.choice import Choice
from .types.date import Date
from .types.datetime import Datetime
from .types.email import Email
from .types.estimate import Estimate
from .types.integer import Integer
from .types.path import Path
from .types.string import String
from .types.any import Any

direction_displays = {
    'from_': 'from',
    'to': 'to',
}


def create_adapter(direction: Literal['from_', 'to']):
    def adapt(
        self,
        format_name,
        value,
        field,
        original_format=None,
    ):
        if field.type.name == 'string':
            return value

        converted_name = f'{direction_displays[direction]}_{format_name}'

        if hasattr(field.type, converted_name):
            converter = getattr(field.type, converted_name)
            return converter(value)

        if format_name != 'string':
            return adapt(
                self=self,
                format_name='string',
                value=value,
                original_format=format_name,
                field=field,
            )
        else:
            dir = direction_displays[direction]
            if original_format is None:
                original_format = format_name

            raise CoercionError(
                f'Cannot convert {field.type.name} {dir} {original_format}.'
            )

    return adapt


builtin_types = (
    Any,
    Binary,
    Boolean,
    Child,
    Choice,
    Date,
    Datetime,
    Email,
    Estimate,
    Integer,
    Path,
    String,
)


builtin_types = {
    type.name: type
    for type in builtin_types
}


def create_final_class(model, base_type, type_exts):
    final_attributes = AttributeFields()
    if base_type.attributes:
        final_attributes._merge(base_type.attributes, model)

    for ext in type_exts:
        if ext.attributes:
            final_attributes._merge(ext.attributes, model)

    body = {}
    if final_attributes:
        body['attributes'] = final_attributes

    return type(base_type.__name__, (*reversed(type_exts), base_type), body)


class TypeRegistry(Registry):
    to_format = create_adapter('to')
    from_format = create_adapter('from_')

    def __init__(self, model, types):
        super().__init__(model)

        types = {
            type.name: type
            for type in types
        }

        plugin_types = {
            type.name: type
            for plugin in self.model.plugins
            for type in plugin.types
        }

        types = builtin_types | plugin_types | types

        type_exts = {}
        for plugin in self.model.plugins:
            for ext in plugin.type_exts:
                type_exts.setdefault(ext.name, [])
                type_exts[ext.name].append(ext)

        self.types_by_impl = {}

        for name, type in types.items():
            exts = type_exts.get(name, [])
            final_type = create_final_class(model, type, exts)

            if not isinstance(final_type.implementation, property):
                self.types_by_impl[final_type.implementation] = final_type

            self.register_meta_info(final_type)
            self._add(name, final_type)

        self.__load_special_attrs()

    def __load_special_attrs(self):
        for file in files('omniblack.model.types').iterdir():
            if file.name.endswith('.json'):
                with file.open('r') as file_obj:
                    attrs_def = load(file_obj)

                name = file.name.removesuffix('_attrs.json')

                attributes = AttributeFields(*attrs_def['fields'])
                self.model.meta_structs.add_type_attrs(
                    name,
                    attributes,
                )

    def register_meta_info(self, new_type):
        if new_type.attributes:
            self.model.meta_structs.add_type_attrs(
                new_type.name,
                new_type.attributes,
            )


def validate(*args, **kwargs):
    return True
