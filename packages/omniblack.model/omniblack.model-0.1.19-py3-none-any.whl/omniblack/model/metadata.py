from omniblack.utils import public
from importlib.resources import files
from json import load
from copy import deepcopy
from collections.abc import KeysView, ItemsView, ValuesView
from omniblack.string_case import Cases

from .undefined import undefined
from .abc import Registry

meta_json_cache = {}


def load_meta_json(struct_name):
    if struct_name not in meta_json_cache:
        meta_pkg = files('omniblack.model.meta_model')
        with open(meta_pkg.joinpath(struct_name + '.json')) as file:
            meta_json_cache[struct_name] = load(file)

    return deepcopy(meta_json_cache[struct_name])


def items_to_merge(target, source):
    for key, value in target.items():
        if key in source:
            yield key, value, source[key]

    for key, value in source.items():
        if key not in target:
            yield key, target.get(key, undefined), value


class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


@public
class MetaBase:
    def __init_subclass__(
        cls,
        model=None,
        struct_def=None,
        struct_name=None,
        plain=False,
        **kwargs,
    ):
        if not plain:
            if model is None:
                raise TypeError(
                    'Model may not be none for smart MetaBase classes',
                )
            cls.model = model

            if struct_name is None:
                if struct_def is not None:
                    struct_name = struct_def['name']
                else:
                    struct_name = Cases.Snake.to(cls.__name__)

            cls.struct_name = struct_name

            if struct_def is None:
                cls.struct_def = load_meta_json(struct_name)
            else:
                cls.struct_def = struct_def

        else:
            cls.struct_name = None
            cls.field_names = None
            cls.struct_def = None
            cls.model = None

        super().__init_subclass__(**kwargs)

    @classproperty
    def field_names(cls):
        if cls.struct_def:
            for field in cls.struct_def['fields']:
                yield field['name']
        else:
            return None

    def __init__(self, values=None, model=None, **kwargs):
        cls = self.__class__
        self._model = model or cls.model

        if values is not None:
            self.update(values)

        self.update(kwargs)

    def __getattr__(self, name):
        field = self.get_field(name)

        if field is None:
            raise AttributeError(name)

        assumed = field.get('assumed', undefined)

        if assumed is undefined:
            raise AttributeError(name)

        return assumed

    def _to_child_type(self, value, child_type):
        if isinstance(value, child_type):
            return value
        else:
            return child_type(**value, model=self._model)

    def __setattr__(self, name, value):
        try:
            if value is undefined:
                if name in self.__dict__:
                    del self.__dict__[name]
            else:
                child_type, is_list = self._get_child_type(name)
                if child_type is not None:
                    if is_list:
                        value = [
                            self._to_child_type(item, child_type)
                            for item in value
                        ]
                    else:
                        value = self._to_child_type(value, child_type)

                self.__dict__[name] = value
        except KeyError as err:
            raise AttributeError(*err.args)

    def _get_child_type(self, name):
        field = self.get_field(name)

        if field and field['type'] == 'child':
            child_type_name = field['child_attrs']['struct']
            if self._model and child_type_name in self._model.meta_structs:
                child_type = self._model.meta_structs[child_type_name]
                return child_type, field.get('list')
            else:
                return None, field.get('list')

        return None, False

    def __delattr__(self, name):
        try:
            del self.__dict__[name]
        except KeyError as err:
            raise AttributeError(*err.args) from None

    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            field = self.get_field(key)
            assumed = field.get('assumed',  undefined)

            if assumed is undefined:
                raise

            return assumed

    def __setitem__(self, key, value):
        if value is undefined:
            if key in self.__dict__:
                del self.__dict__[key]
        else:
            self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        if self.struct_def:
            for field_name in self.field_names:
                if field_name in self:
                    yield field_name
        else:
            for key, value in self.__dict__.items():
                if value is not undefined:
                    yield key

    def __len__(self):
        return len(self.__dict__)

    def __reversed__(self):
        return reversed(self.__dict__)

    def __contains__(self, key):
        return hasattr(self, key)

    def __rich_repr__(self):
        for key, value in self.items():
            if not key.startswith('_'):
                yield key, value

    def __repr__(self):
        item_strs = (
            f'{key}={repr(value)}'
            for key, value in self.items()
            if not key.startswith('_')
        )

        item_str = ', '.join(item_strs)

        cls = self.__class__
        cls_name = cls.__name__

        return f'{cls_name}({item_str})'

    def keys(self):
        return KeysView(self)

    def values(self):
        return ValuesView(self)

    def items(self):
        return ItemsView(self)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __copy__(self):
        cls = self.__class__
        return cls(self.__dict__)

    def __deepcopy__(self, memo):
        cls = self.__class__

        values = {
            key: deepcopy(value, memo)
            for key, value in self.items()
        }

        return cls(values)

    def update(self, other, **kwargs):
        for key, value in other.items():
            setattr(self, key, value)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __or__(self, other):
        return self.__dict__ | other

    def __ior__(self, other):
        self.__dict__ |= other
        return self.__dict__

    def copy(self):
        return self.__copy__()

    @classmethod
    def get_field(cls, field_name):
        if cls.struct_def is None:
            return

        for field in cls.struct_def.get('fields', tuple()):
            if field['name'] == field_name:
                return field

    def merge(self, other):
        for attr, selfValue, otherValue in items_to_merge(self, other):
            if selfValue is undefined:
                self[attr] = otherValue
            elif isinstance(selfValue, MetaBase):
                selfValue.merge(otherValue)
            else:
                self[attr] = otherValue


@public
class Metadata(MetaBase, plain=True):
    pass


@public
class MetaStructRegistry(Registry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for struct_path in files('omniblack.model.meta_model').iterdir():
            if struct_path.name.endswith('.json'):
                with struct_path.open('r') as struct_file:
                    struct_def = load(struct_file)
                self._add(struct_def)

    def _add(self, struct_def: dict):
        struct_name = struct_def['name']

        meta_cls = type(
            Cases.Pascal.to(struct_name),
            (MetaBase,),
            {},
            struct_def=struct_def,
            model=self.model,
        )
        return super()._add(meta_cls.struct_name, meta_cls)

    def add_type_attrs(self, type_name, attributes):
        field_name = Cases.Snake.to(f'{type_name}_attrs')
        display = dict(en=Cases.Title.to(f'{type_name} Attributes'))
        desc = dict(
            en=f'Attributes that configure a {type_name} field.',
        )

        attr_struct = dict(
            name=field_name,
            desc=desc,
            display=display,
            fields=attributes.fields.values(),
        )

        self._add(attr_struct)

        field_def = dict(
            name=field_name,
            desc=desc,
            display=display,
            type='child',
            required=attributes.get('required', False),
            child_attrs=dict(struct=field_name),
        )

        self.field.struct_def['fields'].append(field_def)
