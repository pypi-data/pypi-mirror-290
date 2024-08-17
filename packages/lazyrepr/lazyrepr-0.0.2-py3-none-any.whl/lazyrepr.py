""" Mixin class with __repr__ and _repr_pretty_ implementations """

from inspect import Signature, Parameter

INDENTATION = 4


def pretty_call(name, *args, **kwargs):
    """representation of a function call"""

    params = tuple(repr(p) for p in args) + tuple("%s=%r" % kv for kv in kwargs.items())
    params = ", ".join(params)

    return f"{name}({params})"


def split_arguments(func, arguments):
    """split arguments into args, kwargs according to function signature"""

    signature = Signature.from_callable(func)
    keyword_only = False
    args, kwargs = [], {}

    for p in signature.parameters.values():
        v = arguments.get(p.name, p.default)

        if p.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD):
            raise ValueError(f"Unsupported parameter type {p.kind}")

        if p.kind == Parameter.KEYWORD_ONLY:
            keyword_only = True

        if v == p.default:
            # skip argument if not equal to default
            if keyword_only or not isinstance(v, (int, float)):
                keyword_only = True
                continue

        if keyword_only:
            kwargs[p.name] = v
        else:
            args.append(v)

    return args, kwargs


def lazy_repr(obj):
    """minimal __repr__ method based on __init__ signature"""

    ctor = obj.__init__
    data = obj.__dict__
    cname = obj.__class__.__name__
    args, kwargs = split_arguments(ctor, data)

    params = tuple(repr(p) for p in args) + tuple(
        "%s=%r" % kv for kv in kwargs.items()
    )
    params = ", ".join(params)

    return "%s(%s)" % (cname, params)


class ReprMixin:
    """Mixin class with __repr__ and _repr_pretty_ implementations"""

    __repr__ = lazy_repr

    def _repr_pretty_(self, p, cycle):
        """IPython pretty printer handler"""

        if cycle:
            p.text("...")
            return

        ctor = self.__init__
        data = self.__dict__
        cname = self.__class__.__name__
        args, kwargs = split_arguments(ctor, data)

        started = False

        def new_item():
            nonlocal started
            if started:
                p.text(",")
                p.breakable()
            started = True

        prefix = cname + "("
        with p.group(INDENTATION, prefix, ")"):
            for arg in args:
                new_item()
                p.pretty(arg)
            for arg_name, arg in kwargs.items():
                new_item()
                arg_prefix = arg_name + "="
                with p.group(len(arg_prefix), arg_prefix):
                    p.pretty(arg)
