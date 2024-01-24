from __future__ import annotations

from collections.abc import Mapping
from importlib import import_module
from importlib.resources import files, Resource
from itertools import chain, groupby
from json import load, JSONDecodeError
from operator import attrgetter, getitem
from typing import TYPE_CHECKING
from os import path, PathLike

from public import public

from .abc import Registry
from .dot_path import DotPath
from .field import Field
from .format import Format, get_preferred_file
from .preprocess_struct import preprocess_struct_def
from .undefined import undefined

if TYPE_CHECKING:
    from .model import Model

bases_path = DotPath(('implementation', 'python', 'bases'))


meta_model = files('omniblack.model.meta_model')
struct_traversable = meta_model.joinpath('struct.json')

with struct_traversable.open('r', encoding='utf-8') as struct_def_file:
    # The struct def of struct
    struct_struct_def = load(struct_def_file)


def is_ui_string(field):
    return (
        field['type'] == 'child'
        and field['child_attrs']['struct'] == 'ui_string'
    )


@public
def indiv_fields(indiv):
    return indiv._StructBase__fields


@public
def get_path(indiv):
    return indiv._Struct__path


@public
def get_model(indiv):
    return indiv._Struct__model


@public
def get_struct_name(indiv):
    return type(indiv).name

from .coercion import coerce_from

root_ui_string = {
    field['name']
    for field in struct_struct_def['fields']
    if is_ui_string(field)
}

struct_fields = tuple(
    field['name']
    for field in struct_struct_def['fields']
)


def import_base(base_str):
    module_id, name = base_str.split(':')
    module = import_module(module_id)
    return getattr(module, name)


class Struct(type):
    def __new__(
            cls,
            name,
            bases,
            attrs: dict,
            struct_def: dict,
            model: Model,
    ):
        bases = list(bases)
        pass_struct, post_event = model.call_handlers(
            'create_class',
            name,
            bases,
            attrs,
            struct_def,
        )

        struct_def = model.meta_structs.struct(struct_def)

        model_bases = (
            import_base(base)
            for base in bases_path.get(struct_def, tuple())
        )
        final_bases = tuple(chain(model_bases, bases, (StructBase,)))

        fields = []
        attrs['_Struct__model'] = model
        attrs['model'] = model
        attrs['struct_def'] = struct_def

        for field in struct_def['fields']:
            field_name = field['name']
            field_descriptor = Field(**field, model=model)
            fields.append(field_descriptor)
            attrs[field_name] = field_descriptor

        attrs['_StructBase__fields'] = tuple(fields)

        new_cls = super().__new__(
            cls,
            name,
            final_bases,
            attrs,
        )

        if pass_struct:
            post_event(new_cls)
        else:
            post_event()

        return new_cls

    def __repr__(cls):
        name = cls.struct_def.name

        values = tuple(
            f'{name}={repr(cls.struct_def.get(name, None))}'
            for name in struct_fields
        )
        values_str = ', '.join(values)

        return f'{name}({values_str})'

@public
class StructBase:
    def __init__(self, values=None, *, is_base=False, **kwargs):
        if values is None or values is undefined:
            values = {}

        values |= kwargs

        if not is_base:
            cls = self.__class__
            for field in cls.__fields:
                value = values.get(field.field_def.name, undefined)
                setattr(self, field.field_def.name, value)

        super().__init__()

    def __repr__(self):
        cls = self.__class__
        name = cls.__name__

        field_names = (
            field.field_def.name
            for field in indiv_fields(self)
        )
        values = tuple(
            f'{field_name}={repr(getattr(self, field_name, undefined))}'
            for field_name in field_names
        )

        values_str = ', '.join(values)

        return f'{name}({values_str})'

    def __rich_repr__(self):
        for field in indiv_fields(self):
            field_value = getattr(self, field.field_def.name, undefined)
            yield field.field_def.name, field_value

    def __contains__(self, key):
        try:
            return self[key] is not undefined
        except KeyError:
            return False
        else:
            return True

    def __bool__(self):
        for field in indiv_fields(self):
            if field.field_def.type == 'child':
                if self[field.field_def.name]:
                    return True
            elif field.field_def.name in self:
                return True
        else:
            return False

    def __eq__(self, other):
        if not isinstance(other, Struct):
            return NotImplemented

        for field in indiv_fields(self):
            try:
                self_value = self[field.field_def.name]
            except KeyError:
                self_value = undefined

            try:
                other_value = other[field.field_def.name]
            except KeyError:
                other_value = undefined

            if self_value != other_value:
                return False
        else:
            return True

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError as err:
            raise KeyError(*err.args) from None

    def __setitem__(self, key, value):
        try:
            return setattr(self, key, value)
        except AttributeError as err:
            raise KeyError(*err.args) from None

    def __delitem__(self, key):
        try:
            return delattr(self, key)
        except AttributeError as err:
            raise KeyError(*err.args) from None

    def __iter__(self):
        for field in indiv_fields(self):
            if field.field_def.name in self:
                yield field.field_def.name

    def __reversed__(self):
        for field in reversed(indiv_fields(self)):
            if field.field_def.name in self:
                yield field.field_def.name

    def __copy__(self):
        values = {}
        cls = self.__class__
        for field in indiv_fields(self):
            try:
                values[field.field_def.name] = self[field.field_def.name]
            except KeyError:
                pass

        return cls(**values)

    def __set_path(self, path: DotPath):
        self.__path = path

    def __deepcopy__(self, memo):
        from copy import deepcopy
        cls = self.__class__
        values = {}

        for field in indiv_fields(self):
            try:
                values[field.field_def.name] = deepcopy(
                    self[field.field_def.name],
                    memo,
                )
            except KeyError:
                pass

        return cls(**values)

    @classmethod
    def load_file(cls, file: PathLike):
        model = cls.model
        _, suffix = path.splitext(file)

        format = model.formats.by_suffix[suffix]

        with open(file, mode='r') as file_obj:
            rec = format.load(file_obj)
            indiv = coerce_from(model, rec, format, cls.struct_def.name)
            return indiv


def get_contents(package, model: Model):
    pkg_files = files(package)

    resources = (
        resource
        for resource in pkg_files.iterdir()
        if resource.is_file() and resource.suffix in model.formats.by_suffix
    )

    return tuple(
        get_preferred_file(files, model)
        for name, files in groupby(resources, attrgetter('stem'))
    )


def is_loadable(path, model):
    return path.suffix in model.formats.by_suffix


@public
class StructRegistry(Registry):
    def __init__(self, model, struct_packages, struct_defs):
        super().__init__(model)
        for pkg in struct_packages:
            self.load_model_package(pkg)

        for struct_def in struct_defs:
            self._add(struct_def)

    def _add(self, struct_def: dict, *bases):
        meta_structs, = preprocess_struct_def(struct_def)
        for struct_name in meta_structs:
            self.load_meta_struct(struct_name)

        name = struct_def['name']
        new_struct = Struct(
            name,
            bases,
            {},
            struct_def=struct_def,
            model=self.model,
        )

        self.model.expose(name, new_struct)
        return super()._add(name, new_struct)

    __call__ = _add

    def load_meta_struct(self, struct_name):
        if struct_name in self:
            return self[struct_name]

        meta_model_files = files('omniblack.model.meta_model')
        struct_def_resource = meta_model_files.joinpath(f'{struct_name}.json')

        struct_cls = self.load_struct_def_resource(struct_def_resource)

        child_fields = (
            field
            for field in struct_cls.struct_def.fields
            if field['type'] == 'child'
        )

        for child_field in child_fields:
            self.load_meta_struct(child_field['child_attrs']['struct'])

        return self[struct_name]

    def load_model_package(self, package):
        for resource in get_contents(package, self.__model):
            self.load_struct_def_resource(resource)

    def load_struct_def_resource(self, resource_path):
        format = self.__model.formats.by_suffix[resource_path.suffix]

        try:
            struct_def = self.load_resource(
                resource_path,
                format,
            )

            return self._add(struct_def)
        except AttributeError as err:
            raise ValueError('Missing field in', resource_path) from err
        except KeyError as err:
            raise ValueError('Missing needed value in', resource_path) from err
        except JSONDecodeError:
            print(f'File {resource_path}')
            raise

    def load_resource(self, resource: Resource, format: Format):
        with resource.open('r') as file_obj:
            return format.load(file_obj)


class ChildField(Field, type='child'):
    def __set__(self, parent_indiv, new_value):
        indiv = self.__get__(parent_indiv, type(parent_indiv))

        if isinstance(indiv, self.__objclass__):
            super().__set__(parent_indiv, indiv)
        elif new_value is not undefined:
            getter = (
                getitem
                if isinstance(new_value, Mapping)
                else getattr
            )

            for field in indiv_fields(indiv):
                try:
                    indiv[field.field_def.name] = getter(
                        new_value,
                        field.field_def.name,
                    )
                except (KeyError, AttributeError):
                    del indiv[field.field_def.name]
        else:
            for field in indiv_fields(indiv):
                del indiv[field.field_def.name]

    def __get__(self, obj, obj_type):
        if obj is None:
            return self

        try:
            return super().__get__(obj, obj_type=obj_type)
        except AttributeError:
            child_cls = self.model.structs[self.field_def.child_attrs.struct]
            new_child = child_cls()
            super().__set__(obj, new_child)
            return new_child
