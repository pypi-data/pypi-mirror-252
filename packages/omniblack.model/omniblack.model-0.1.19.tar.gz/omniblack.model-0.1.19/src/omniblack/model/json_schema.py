from public import public

from .metadata import MetaBase
from .struct import Struct, indiv_fields


@public
def to_json_schema(struct_cls: Struct) -> dict:
    struct_def = struct_cls.struct_def

    schema = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        'title': struct_def.name,
        'description': struct_def.desc.en,
        'type': 'object',
    }

    properties = {
        field.field_def.name: field_schema(field)
        for field in indiv_fields(struct_cls)
    }

    schema['properties'] = properties

    required_fields = [
        field.name
        for field in struct_def.fields
        if field.required
    ]

    schema['required'] = required_fields

    return schema


def field_schema(field: MetaBase):
    type_def = field.type

    if type_def.json_schema is None:
        raise TypeError(
            f'"{field.field_def.type}" does not support json schemas.',
        )

    field_schema = type_def.json_schema()

    if field.field_def.list:
        field_schema = list_schema(field.field_def, field_schema)

    field_schema['title'] = field.field_def.display.en
    field_schema['description'] = field.field_def.desc.en

    return field_schema


def list_schema(field, item_schema):
    model = field.model
    attrs = getattr(field, 'list_attrs', model.meta_structs.list_attrs())

    schema = {
        'type': 'array',
        'items': item_schema,
    }

    if attrs.get('minLen'):
        schema['minItems'] = attrs.minLen

    if attrs.get('maxLen'):
        schema['maxItems'] = attrs.maxLen

    return schema
