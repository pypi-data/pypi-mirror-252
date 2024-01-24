from typing import Union

from public import public

from .format import Format
from .mapper import map
from .struct import get_model
from .walker import WalkerYield, visit_leaves
from .undefined import undefined


@public
def coerce_to(indiv, format: Union[str, Format]):
    """
    Coerce an indiv to format.

    Parameters
    ----------

    indiv: :type:`omniblack.model.StructBase`
        The indiv to be converted to `format`

    format: :type:`omniblack.model.Format` | :type:`str`
        The format the output should be comptabile with.
    """

    if isinstance(format, Format):
        format_name = format.name
    else:
        format_name = format

    model = get_model(indiv)

    def to_map_cb(walker_leaf: WalkerYield):
        value = walker_leaf.value

        if value is undefined or value is None:
            return value

        return model.types.to_format(
            format_name=format_name,
            value=walker_leaf.value,
            field=walker_leaf.field,
        )

    return map(to_map_cb, indiv, visit_leaves)


@public
def coerce_from(model, rec, format: Union[str, Format], struct_name: str):
    """
    Coerce from a format.

    Parameters
    ----------

    model: :type:`omniblack.model.Model`
        The model :code:`struct_name` is defined in.

    rec: :type:`collections.abc.Mapping`
        The rec to convert to :code:`struct_name`.

    format: :type:`str` | :type:`omniblack.model.Format`
        The format :code:`rec` should converted from.

    struct_name: :type:`str`
        The struct :code:`rec` should be converted to.
    """

    Struct = model.structs[struct_name]
    indiv = Struct(rec)

    if isinstance(format, Format):
        format_name = format.name
    else:
        format_name = format

    def from_map_cb(walker_leaf: WalkerYield):
        value = walker_leaf.value

        if value is undefined or value is None:
            return value

        return model.types.from_format(
            format_name=format_name,
            value=value,
            field=walker_leaf.field,
        )

    coerced_rec = map(from_map_cb, indiv, visit_leaves)

    return Struct(coerced_rec)
