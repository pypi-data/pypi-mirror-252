from ..field import AttributeFields
from . import ModelType


class Child(ModelType):
    def get_implementation(self):
        field = self.field
        return field.model.structs[field.field_def.child_attrs.struct]

    def json_schema(self):
        child_struct = self.field.field_def.child_attrs.struct

        return {
            'type': 'object',
            '$ref': f'./{child_struct}.schema.json',
        }

    attributes = AttributeFields(
        dict(
            name='struct',
            type='string',
            display=dict(en='Struct Name'),
            desc=dict(
                en='The name of the struct to embed in the field.',
            ),
            required=True,
        ),
        required=True,
    )
