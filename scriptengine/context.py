import sys
from copy import deepcopy

from deepdiff import DeepDiff, Delta

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
    """deepdiff.Delta.__add__ uses copy.deepcopy internally if Delta was created
    with mutate=False (the default). We set mutate=True for Python 3.6 in order to
    avoid the use of deepcopy (see above).
    """
    if _python_version != (3, 6):
        return Delta(DeepDiff(first, second))
    return Delta(DeepDiff(first, second), mutate=True)
