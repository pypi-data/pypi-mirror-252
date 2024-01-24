from typing import NamedTuple


class PreprocessInformation(NamedTuple):
    meta_structs: tuple[str]


def preprocess_struct_def(struct_def) -> PreprocessInformation:
    try:
        meta_structs = set()
        child_fields = (
            field
            for field in struct_def['fields']
            if field['type'] == 'child'
        )

        meta_ref_fields = (
            field
            for field in child_fields
            if field['child_attrs']['struct'].startswith('meta:')
        )

        for field in meta_ref_fields:
            struct_name = field['child_attrs']['struct'].removeprefix('meta:')
            field['child_attrs']['struct'] = struct_name
            meta_structs.add(struct_name)

        return PreprocessInformation(tuple(meta_structs))
    except KeyError as err:
        display = struct_def.get('name', struct_def)
        raise ValueError('Invalid struct def', display) from err
