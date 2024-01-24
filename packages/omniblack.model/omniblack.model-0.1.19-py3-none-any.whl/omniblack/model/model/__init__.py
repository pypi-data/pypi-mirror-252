from __future__ import annotations

import sys
from types import GeneratorType

from public import public

from ..format_registry import FormatRegistry
from ..metadata import MetaStructRegistry
from ..struct import StructRegistry
from ..type_registry import TypeRegistry


@public
class Model:
    """The main interface to access the rest of omniblack.model."""

    #: The name of the model. Used in debugging.
    name: str

    #: The types the model is aware of.
    types: TypeRegistry

    #: The struct classes of the model.
    structs: StructRegistry

    #: The structs used to define the shape of this model's defintions.
    meta_structs: MetaStructRegistry

    #: The formats the model can load or dump to.
    formats: FormatRegistry

    def __hash__(self):
        return hash(id(self))

    def __init__(
        self,
        name,
        struct_packages=[],
        struct_defs=[],
        plugins=[],
        types=[],
        *,
        module_name=None,
        no_expose=False,
    ):
        """
        Parameters
        ----------

        name: :type:`str`
            The name of the model.
            Used to make debugging mutliple models easier.

        struct_packages: :type:`list[str]`
            Import paths where struct defintions are stored.
            See [packaging structs](#header-packaging-structs).

        struct_defs: :type:`list[collections.abc.Mapping]`
            Struct defintions to be registered with the created model.

        plugins: :type:`Plugin`
            Plugins to be added to the model.

        types: :type:`omniblack.model.ModelType`
            Types to be registered with the model.
        """
        self.name = name

        if not no_expose:
            if module_name is None:
                frame = sys._getframe(1)
                module_name = frame.f_globals['__name__']

            self.exposed_module = sys.modules[module_name].__dict__
            self.exposed_module['__all__'] = []

        else:
            self.exposed_module = None

        self.module_name = module_name

        self.plugins = plugins
        self.meta_structs = MetaStructRegistry(self)
        self.types = TypeRegistry(self, types)
        self.formats = FormatRegistry(self)
        self.structs = StructRegistry(
            self,
            struct_packages=struct_packages,
            struct_defs=struct_defs,
        )

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f'{cls_name}(name={self.name})'

    def __rich_repr__(self):
        yield 'name', self.name

    def expose(self, name, value):
        if self.exposed_module is not None:
            self.exposed_module[name] = value
            self.exposed_module['__all__'].append(name)

    def load_meta_model(self, name=None, no_expose=False):
        """
        Return the meta model for this model.

        Parameters
        ----------
        name: :type:`str`
            The name of the meta model.
            Defaults to :code:`f'Meta Model for {self.name}'`
        """

        struct_defs = [
            struct.struct_def
            for struct in self.meta_structs.values()
        ]

        if name is None:
            name = f'Meta Model for {self.name}'

        return self.__class__(
            name,
            struct_defs=struct_defs,
            no_expose=no_expose,
        )

    def call_handlers(self, event, *args, **kwargs):
        """
        Call associated event handlers.

        Parameters
        ----------

        event: :type:`str`
            The event to fire.

        *args: :type:`typing.Any`
            Args to be passed to the event handlers.

        **kwargs: :type:`typing.Any`
            Keyword args to be passed to the event handlers.
        """
        suspended = []
        request_value = False

        for plugin in self.plugins:
            handler = getattr(plugin, f'on_{event}', None)
            if handler is not None:
                value = handler(*args, **kwargs)

                if isinstance(value, GeneratorType):
                    request_value = request_value or next(value)
                    suspended.append(value)

        def post_event(new_value=None):
            for listener in suspended:
                try:
                    listener.send(new_value)
                except StopIteration:
                    pass

        return request_value, post_event
