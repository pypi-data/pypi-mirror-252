import json
from collections.abc import Mapping, MutableMapping
from io import TextIOBase

from public import public

from omniblack.context_proxy import ContextProxy

from .format import Format, StringLoadFormat
from .formats import TomlFormat  # noqa: F401

__all__ = ['YamlFormat']


@public
class JSONFormat(Format):
    load = staticmethod(json.load)
    dump = staticmethod(json.dump)

    loads = staticmethod(json.loads)
    dumps = staticmethod(json.dumps)


YamlFormat = None
yaml_mime_types = (
    'text/vnd.yaml',
    'text/yaml',
    'text/x-yaml',
    'application/vnd.yaml',
    'application/yaml',
    'application/x-yaml',
)

try:
    from ruamel.yaml import YAML
except ImportError:
    pass
else:
    class YamlFormat(Format, StringLoadFormat, mime_types=yaml_mime_types):
        loader = staticmethod(
            ContextProxy(lambda: YAML(typ='safe'), name='YAML'),
        )

        def load(self, file: TextIOBase) -> MutableMapping:
            return self.loader.load(file)

        def dump(self, file: TextIOBase, data: Mapping) -> None:
            self.loader.dump(data, file)


if YamlFormat is None:
    try:
        from yaml import safe_load, safe_dump
    except ImportError:
        pass
    else:
        class YamlFormat(Format, StringLoadFormat, mime_types=yaml_mime_types):
            load = staticmethod(safe_load)
            dump = staticmethod(safe_dump)
