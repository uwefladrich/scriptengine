import sys
from copy import deepcopy

from deepdiff import DeepDiff, Delta
from deepmerge import always_merger

_python_version = (sys.version_info.major, sys.version_info.minor)


def save_copy(context):
    """For versions other than 3.6, this is just copy.deepcopy.
    For 3.6, we have to remove ["se"]["instance"] before deepcopying and restore
    afterwards, because this constitutes some recursive reference that 3.6 has a
    problem with.
    """
    if _python_version != (3, 6):
        return deepcopy(context)
    singleton = object()
    try:
        se_instance = context["se"]["instance"]
        context["se"]["instance"] = None
    except KeyError:
        se_instance = singleton
    copied_context = deepcopy(context)
    if se_instance is not singleton:
        copied_context["se"]["instance"] = context["se"]["instance"] = se_instance
    return copied_context


def context_delta(first, second):
    """The deepdiff.Delta's __init__ and __add__ functions use copy.deepcopy
    internally, which does not work with the SE context (see above).
    Therefore, we ignore context["se"]["instance"] before creating Delta. This
    means, that for Python 3.6 this item in the context is not part of the Delta,
    even if it was changed between first and second!
    Also, we have to create the Delta with mutate=True to avoid another deepcopy.
    """
    if _python_version != (3, 6):
        return Delta(DeepDiff(first, second))

    singleton = object()
    try:
        first_se_instance = first["se"]["instance"]
        first["se"]["instance"] = None
    except KeyError:
        first_se_instance = singleton
    try:
        second_se_instance = second["se"]["instance"]
        second["se"]["instance"] = None
    except KeyError:
        second_se_instance = singleton
    delta = Delta(DeepDiff(first, second), mutate=True)
    if first_se_instance is not singleton:
        first["se"]["instance"] = first_se_instance
    if second_se_instance is not singleton:
        second["se"]["instance"] = second_se_instance
    return delta


class Context(dict):
    pass


class ContextUpdate:
    def __init__(self, base=None, second=None):
        if base is None:
            self.merge = self.delta = None
        elif second is None:
            if not isinstance(base, dict):
                raise TypeError(
                    "First argument of ContextUpdate() must be None or a dict"
                )
            self.merge = base
            self.delta = None
        else:
            self.merge = None
            self.delta = context_delta(base, second)

    def __radd__(self, other):
        if isinstance(other, dict):
            if self.merge:
                return always_merger.merge(other, self.merge)
            elif self.delta:
                return other + self.delta
            return other
        raise TypeError(
            f"Unsupported operand types for +: '{type(other)}' and 'ContextUpdate'"
        )

    def __repr__(self):
        if self.merge:
            return f"<ContextUpdate: merge {self.merge}>"
        elif self.delta:
            return f"<ContextUpdate: {self.delta}>"
        else:
            return "<ContextUpdate: None>"
