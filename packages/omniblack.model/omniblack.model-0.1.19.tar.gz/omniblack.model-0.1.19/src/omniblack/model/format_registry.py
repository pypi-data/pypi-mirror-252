from typing import Union

from public import public

from .abc import Registry
from .format import Format
from .format_classes import JSONFormat, TomlFormat, YamlFormat

builtin_formats = tuple(
    format_cls
    for format_cls in (JSONFormat, TomlFormat, YamlFormat)
    if format_cls is not None
)


@public
class FormatRegistry(Registry):
    def __init__(self, model):
        super().__init__(model)
        self.by_suffix = {}
        self.by_mime_type = {}
        for plugin in model.plugins:
            for format in plugin.formats:
                self._add(format())

        for format in builtin_formats:
            self._add(format())

    def _add(self, format: Union[Format, str]):
        if isinstance(format, str):
            return self[format]
        else:
            self.by_mime_type |= {
                mime_type: format
                for mime_type in format.mime_types
            }

            self.by_suffix[format.file_suffix] = format

            return super()._add(format.name, format)
