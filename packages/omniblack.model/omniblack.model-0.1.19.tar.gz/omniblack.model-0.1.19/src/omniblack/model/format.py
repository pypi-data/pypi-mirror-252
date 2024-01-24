from abc import ABC, abstractmethod
from typing import Callable
from collections.abc import Iterable, MutableMapping, Mapping
from functools import partial
from io import TextIOBase, StringIO
from pathlib import Path

from public import public

format_preference = ('yaml', 'toml', 'json')


def pref_key(key):
    try:
        return format_preference.index(key)
    except IndexError:
        return len(format_preference)


def path_pref_key(path: Path, model):
    format = model.formats.by_suffix[path.suffix]
    return pref_key(format.name)


@public
def get_preferred_file(paths: Iterable[Path], model) -> Path:
    paths_by_pref = sorted(paths, key=partial(path_pref_key, model=model))
    return paths_by_pref[0]


load_type_def = Callable[[TextIOBase], MutableMapping] | None
dump_type_def = Callable[[Mapping, TextIOBase], None] | None

loads_type_def = Callable[[str], MutableMapping] | None
dumps_type_def = Callable[[Mapping], str] | None


@public
class FileLoadFormat(ABC):
    def load(self, file: TextIOBase) -> MutableMapping:
        string = file.read()
        return self.loads(string)

    def dump(self, data: Mapping, file: TextIOBase) -> None:
        return file.write(self.dumps(data))

    @abstractmethod
    def loads(self, string: str) -> MutableMapping:
        pass

    @abstractmethod
    def dumps(self, data: Mapping) -> str:
        pass


@public
class StringLoadFormat(ABC):
    @abstractmethod
    def load(self, file: TextIOBase) -> MutableMapping:
        pass

    @abstractmethod
    def dump(self, data: Mapping, file: TextIOBase) -> None:
        pass

    def loads(self, string: str) -> MutableMapping:
        file = StringIO(string)
        return self.load(file)

    def dumps(self, data: Mapping) -> str:
        file = StringIO()
        self.dump(file, data)
        return file.getvalue()


@public
class Format:
    load: load_type_def = None
    dump: dump_type_def = None

    loads: loads_type_def = None
    dumps: dumps_type_def = None

    def __init_subclass__(cls, extension=None, mime_types=None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls_name = cls.__name__
        name = cls_name.removesuffix('Format').lower()
        cls.name = name

        if extension is None:
            cls.file_extension = name
        else:
            cls.file_extension = extension

        cls.file_suffix = f'.{cls.file_extension}'

        if mime_types is not None:
            mime_is_iter = (isinstance(mime_types, Iterable)
                            and not isinstance(mime_types, str))
            if mime_is_iter:
                mime_types = tuple(mime_types)
                cls.mime_types = frozenset(mime_types)
                cls.mime_type = mime_types[0]
            else:
                cls.mime_type = mime_types
                cls.mime_types = frozenset((mime_types, ))
        else:
            cls.mime_type = f'application/{name}'
            cls.mime_types = frozenset((cls.mime_type, ))
