# Python imports
import pkgutil
import sys
from functools import partial, wraps

# Internal imports
from mox.exceptions import ObjectResolutionError


_NAME_PATTERN = None


def _resolve_name(name):  # pragma: no cover
    """
    Copied from pkg_util.resolve_name so it can be used with Python 3.8

    Resolve a name to an object.

    It is expected that `name` will be a string in one of the following
    formats, where W is shorthand for a valid Python identifier and dot stands
    for a literal period in these pseudo-regexes:

    W(.W)*
    W(.W)*:(W(.W)*)?

    The first form is intended for backward compatibility only. It assumes that
    some part of the dotted name is a package, and the rest is an object
    somewhere within that package, possibly nested inside other objects.
    Because the place where the package stops and the object hierarchy starts
    can't be inferred by inspection, repeated attempts to import must be done
    with this form.

    In the second form, the caller makes the division point clear through the
    provision of a single colon: the dotted name to the left of the colon is a
    package to be imported, and the dotted name to the right is the object
    hierarchy within that package. Only one import is needed in this form. If
    it ends with the colon, then a module object is returned.

    The function will return an object (which might be a module), or raise one
    of the following exceptions:

    ValueError - if `name` isn't in a recognised format
    ImportError - if an import failed when it shouldn't have
    AttributeError - if a failure occurred when traversing the object hierarchy
                     within the imported package to get to the desired object.
    """
    # Python imports
    import importlib

    global _NAME_PATTERN
    if _NAME_PATTERN is None:
        # Lazy import to speedup Python startup time
        # Python imports
        import re

        dotted_words = r"(?!\d)(\w+)(\.(?!\d)(\w+))*"
        _NAME_PATTERN = re.compile(f"^(?P<pkg>{dotted_words})" f"(?P<cln>:(?P<obj>{dotted_words})?)?$", re.UNICODE)

    m = _NAME_PATTERN.match(name)
    if not m:
        raise ValueError(f"invalid format: {name!r}")
    gd = m.groupdict()
    if gd.get("cln"):
        # there is a colon - a one-step import is all that's needed
        mod = importlib.import_module(gd["pkg"])
        parts = gd.get("obj")
        parts = parts.split(".") if parts else []
    else:
        # no colon - have to iterate to find the package boundary
        parts = name.split(".")
        modname = parts.pop(0)
        # first part *must* be a module/package.
        mod = importlib.import_module(modname)
        while parts:
            p = parts[0]
            s = f"{modname}.{p}"
            try:
                mod = importlib.import_module(s)
                parts.pop(0)
                modname = s
            except ImportError:
                break
    # if we reach this point, mod is the module, already imported, and
    # parts is the list of parts in the object hierarchy to be traversed, or
    # an empty list if just the module is wanted.
    result = mod
    for p in parts:
        result = getattr(result, p)
    return result


if sys.version_info < (3, 9):
    resolve_name = _resolve_name
else:
    resolve_name = pkgutil.resolve_name


def resolve_object(func):
    """Resolves an object and its attribute before calling the function in case a reference/path is pased."""

    def import_object(path):
        try:
            obj, attribute = path.rsplit(".", 1)
        except (TypeError, ValueError, AttributeError):
            raise ObjectResolutionError(path)

        return partial(resolve_name, obj), attribute

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        obj, attr_name = None, None

        if len(args) >= 1:
            obj = args[0]

        if len(args) >= 2:
            attr_name = args[1]

        if "obj" in kwargs:
            obj = kwargs.pop("obj")
        if "attr_name" in kwargs:
            attr_name = kwargs.pop("attr_name")

        if isinstance(obj, str):
            path = f"{obj.attr_name}" if attr_name else obj
            obj, attr_name = import_object(path)
            obj = obj()

        result = func(self, obj, attr_name, *args[2:], **kwargs)
        return result

    return wrapper
