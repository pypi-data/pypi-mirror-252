from typing import Callable, Any

from public import public

from omniblack.string_case import Cases

from ..field import AttributeFields
from ..validationResult import ValidationResult, ErrorTypes, ValidationMessage
from ..dot_path import DotPath
from ..undefined import undefined
from ..localization import TXT


def native_adapter(self, value):
    return value


@public
class TypeExt:
    name: str | None = None
    impl: type | None = None
    attributes: AttributeFields | None = None
    validator: Callable[[Any], ValidationResult] | None = None
    prepare_metadata: Callable[[], None] | None = None
    get_implementation: Callable[[], type] | None = None
    json_schema: Callable[[], dict] | None = None


@public
class ModelType:
    """
    A type for the model, and details of how to manipulate it.

    Attributes
    ----------

    attributes: :type:`typing.Optional[omniblack.model.AttributeFields]`
        attributes that describe a field of this type.
        Will be add to the field struct with the name
        :code:`f'{self.name}_attrs'`

    implementation: :type:`type`
        The python type that this class describes.

    name: str
        The name of this type. Derived from the class name.


    Methods
    -------
    json_schema()
        Returns the json schema representing this field.

        Returns
        -------
        :type:`dict`

    prepare_metadata()
        Called when a field is created. Can be used to prepare
        metadata from the fields attributes.
    """

    attributes = None
    prepare_metadata = None

    def __init_subclass__(cls):
        cls.name = Cases.Snake.to(cls.__name__)

    def __init__(
        self,
        *,
        field,
        model,
    ):
        self.field = field
        self.model = model

    def __call__(self, *args, **kwargs):
        raise DeprecationWarning('Calling a model type is not supported')

    def __repr__(self):
        cls_name = self.__class__.__name__

        repr_str = f'<{cls_name} name={repr(self.name)}'

        if self.implementation is not None:
            repr_str += f' implementation={repr(self.implementation)}'

        return repr_str + '>'

    def __bool__(self):
        return True

    @property
    def implementation(self):
        if self.implementation is not None:
            return self.implementation
        else:
            return self.get_implementation()

    def get_implementation(self):
        """
        Return the implementation for the associated field.
        Is called by the default :code:`implementation` property.

        Returns
        -------
        :type:`typing.Optional[type]`
        """
        return None

    def validate(self, value: Any, path: DotPath):
        """
        The validator for this type.

        .. note::
            Does not need to handle required.
            The model function :code:`validate` handles required validation
            before calling the type specific validator.

        Parameters
        ----------

        value: :type:`typing.Any`
            The value of the field to validate.

        path: :type:`omniblack.model.DotPath`
            The path to the field in the overall struct.

        Returns
        -------
        :type:`omniblack.model.validationResult.ValidationResult`
        """
        impl = self.implementation()

        if self.field.required and value is undefined:
            msg = ValidationMessage(
                ErrorTypes.constraint_error,
                f'"{path}" is required.',
                path,
            )
            return ValidationResult(False, msg)
        elif not isinstance(value, impl):
            name = self.name
            txt = TXT(
                '${value} is not valid for the type ${name}.',
                locals(),
            )
            msg = ValidationMessage(ErrorTypes.invalid_value, txt, path)
            return ValidationResult(False, msg)

        else:
            return self.validator(value, path)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, ModelType):
            return self.name == other.name
        else:
            return NotImplemented
