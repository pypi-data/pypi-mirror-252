from tomllib import load, loads

from public import public

from ..format import Format

write_lib = None

try:
    import tomli_w
except ImportError:
    pass
else:
    write_lib = tomli_w

if write_lib is None:
    try:
        import toml
    except ImportError:
        pass
    else:
        write_lib = toml

if write_lib is None:
    try:
        import tomlkit
    except ImportError:
        pass
    else:
        write_lib = tomlkit


if hasattr(write_lib, 'dump'):
    dump = staticmethod(write_lib.dump)
else:
    dump = None

if hasattr(write_lib, 'dumps'):
    dumps = staticmethod(write_lib.dumps)
else:
    dumps = None


@public
class TomlFormat(Format):
    load = staticmethod(load)
    loads = staticmethod(loads)

    dump = dump
    dumps = dumps
