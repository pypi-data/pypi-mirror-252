from public import public

from .types import ModelType, TypeExt
from .format import Format
from .storage import Storage


"""
    Event listeners are run before the event occurs.
    If the listeners is a generator that yields
    the generator will be resumed after the event completes.
"""


@public
class Plugin:
    # Expected attrs
    # new types
    types: list[ModelType] = None

    # Extenstions to existing types
    type_exts: list[TypeExt] = None

    # New formats
    formats: list[Format] = None

    # New Storage Engines
    storages: list[Storage] = None

    # Base classes
    bases: list[type] = None

    def __init__(self, model):
        self.model = model

    def on_class_create(self, name, bases, attrs, struct_def):
        """
            Modifty the struct def before the class is generated.
        """

    def on_save(self, indiv, storage_engine):
        """
            Runs before an indiv is saved.
        """

    def on_delete(self, indiv, storage_engine):
        """
            Runs before an indiv is deleted.
        """

    def on_read(self, indiv, storage_engine):
        """
            Runs before an indiv is read.
        """

    def on_search(self, indiv, storage_engine, params: dict):
        """
            Runs before a search is performed.
        """

    def on_validate(self, indiv):
        """
            Runs before an indiv is validated.
        """
