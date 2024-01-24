from collections.abc import Mapping
from copy import deepcopy
from functools import partial

from .walker import walk
from .undefined import undefined


def items(source):
    if isinstance(source, Mapping):
        yield from source.items()
    else:
        for name in source:
            yield name, source[name]


def get(source: Mapping, key: str, default=None):
    try:
        source[key]
    except (KeyError, TypeError):
        return default


def setdefault(source, key, value):
    if key in source:
        return source[key]
    else:
        source[key] = value
        return value


def defaults_deep(dest, *sources: Mapping):
    sources = [
        source
        for source in sources
        if source
    ]

    for source in deepcopy(sources):
        for key, value in items(source):
            dest_value = setdefault(dest, key, {})
            if isinstance(value, Mapping) and isinstance(dest_value, Mapping):
                defaults_deep(dest_value, value)
            else:
                setdefault(dest, key, value)


def bool_dict(dct: dict):
    for value in dct.values():
        if value is undefined:
            continue
        elif isinstance(value, dict):
            if bool_dict(value):
                return True
    else:
        return False


def skip(path, value, visited, descended, new_rec, **kwargs):
    if not visited and descended:
        new_values = path.get(new_rec)
        need_attach = False
        if new_values is None:
            new_values = {}
            need_attach = True

        defaults_deep(new_values, value)

        if need_attach and bool_dict(new_values):
            path.set(new_rec, new_values)

    elif value is not undefined:
        path.set(new_rec, value)


def map(cb, indiv, filter=None, descend=None, reversed=False):
    new_rec = dict()
    skipped = partial(skip, new_rec=new_rec)
    walker = walk(indiv, filter, descend, skipped=skipped)
    if reversed:
        walker = reversed(walker)

    for field in walker:
        new_value = cb(field)
        if new_value is not undefined:
            path = field.path
            path.set(new_rec, new_value)

    return new_rec
