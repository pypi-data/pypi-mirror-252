from __future__ import annotations

from typing import TypeVar
from copy import deepcopy

from public import public
from .undefined import undefined
from .metadata import Metadata, MetaBase


def sort_overrides(item):
    key, cls = item
    return len(key)


ListAttrs = TypeVar('ListAttrs')


field_attrs = (
    'attrs',
    'desc',
    'display',
    'list',
    'name',
    'required',
    'type',
    'valid_values',
)


@public
class Field:
    """
    :cvar field_def: The definition for this field.
    :vartype field_def: :type:`MetaBase`

    :cvar metadata: A container for arbitray metadata.
        Often used by the ModelType or Plugins.
    :vartype metadata: :type:`Metadata`

    :cvar model: The model this field is associated with.
    :vartype model: :type:`omniblack.model.Model`

    :cvar type: The :type:`omniblack.model.ModelType` instance of this field.
    :vartype type: :type:`omniblack.model.ModelType`
    """
    __type_overrides = {}

    def __init_subclass__(
        cls,
        /,
        *,
        type=undefined,
        list=undefined,
        **kwargs,
    ):
        super().__init_subclass__(**kwargs)

        keys = {}
        if type is not undefined:
            keys['type'] = type

        if list is not undefined:
            keys['list'] = list

        key = tuple(keys.items())

        all_overrides = tuple(Field.__type_overrides.items()) + ((key, cls),)
        Field.__type_overrides = dict(
            sorted(all_overrides, key=sort_overrides, reverse=True)
        )

    def __new__(cls, *args, **kwargs):
        for requirements, override in Field.__type_overrides.items():
            matches = all(
                kwargs.get(name, None) == value
                for name, value in requirements
            )

            if matches:
                cls = override
                break

        return super().__new__(cls)

    def __init__(
        self,
        *,
        model,
        **kwargs,
    ):
        """
        :param model: The model the field is associated with.
        :type model: :type:`omniblack.model.Model`

        For other arguments the meta model's field.json

        .. todo::
            Correctly link to the meta model's automatic documentation.
        """

        if isinstance(kwargs['type'], str):
            type_def = model.types[kwargs['type']]
        else:
            type_def = kwargs['type']
            kwargs['type'] = type_def.name

        self.field_def = model.meta_structs.field(kwargs)
        self.model = model
        self.metadata = Metadata()
        self.type = type_def(field=self, model=model)

        if self.type.prepare_metadata:
            self.type.prepare_metadata()

    def __deepcopy__(self, memo):
        new_def = deepcopy(self.field_def, memo)

        return self.__class__(self.model, **new_def)

    def __set_name__(self, owner, name):
        # objclass helps with inspecting the object
        self.__objclass__ = owner
        self.__cls_name = owner.__name__

    def __get__(self, obj, obj_type):
        if obj is None:
            return self

        value = self.__get_value(obj)
        if value is undefined:
            try:
                return self.field_def.assumed
            except AttributeError:
                raise AttributeError(f'{self.field_def.name} is not set.')
        else:
            return value

    def __get_value(self, indiv):
        return getattr(indiv, self.__attr_name, undefined)

    def __set__(self, obj, new_value):
        setattr(obj, self.__attr_name, new_value)

    def __delete__(self, obj):
        self.__set__(obj, undefined)

    def __repr__(self):
        cls = self.__class__
        cls_name = cls.__name__
        values = (
            f'{name}={repr(getattr(self.field_def, name))}'
            for name in field_attrs
            if getattr(self, name, None) is not None
            if getattr(self, name, None) is not undefined
        )

        value_str = ', '.join(values)
        return f'{cls_name}({value_str})'

    def __rich_repr__(self):
        for key, value in self.items():
            if value is not None and value is not undefined:
                yield key, value

    @property
    def __attr_name(self):
        return f'_{self.__cls_name}__{self.field_def.name}'

    def __getitem__(self, key):
        return self.field_def[key]

    def keys(self):
        return self.field_def.keys()

    def items(self):
        return self.field_def.items()


@public
class ListField(Field, list=True):
    def __set__(self, indiv, value):
        coerced = value
        if not isinstance(value, list) and value is not undefined:
            coerced = list(value)

        super().__set__(indiv, coerced)


def ensure_field(maybe_field):
    if isinstance(maybe_field, Field):
        return maybe_field
    else:
        return Field(**maybe_field)


@public
class AttributeFields(MetaBase, plain=True):
    """
    A set of fields that defines the attrs for a type.

    :cvar required: Are the attrs required.
    :vartype required: :type:`bool`

    :cvar fields: The fields that will make up the attrs struct.
    :vartype fields: :type:`dict[str, omniblack.model.Field]`
    """

    def __init__(self, *fields, required=False):
        self.required = required
        self.fields = {
            field['name']: field
            for field in fields
        }

    def __bool__(self):
        return bool(self.fields)

    def __repr__(self):
        cls_name = self.__class__.__name__
        return (
            f'{cls_name}(required={self.required}, fields={repr(self.fields)})'
        )

    def __rich_repr__(self):
        yield 'required', self.required
        yield 'fields', self.fields

    def __deepcopy__(self, memo):
        fields = [
            deepcopy(field, memo)
            for field in self.fields.values()
        ]

        return self.__class__(*fields, self.required)

    def _merge(self, other, model):
        self.required = self.required or other.required
        for name, attr in other.fields.items():
            attr = model.meta_structs.field(attr)

            if name in self.fields:
                self.fields[name]._merge(attr)
            else:
                self.fields[name] = attr
