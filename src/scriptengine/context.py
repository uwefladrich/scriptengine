from collections import UserDict
from collections.abc import Mapping
from typing import Any

import yaml
from deepmerge import always_merger

KEY_SEP = "."


class Context(UserDict):
    """
    The ScriptEngine Context provides context information for Tasks

    https://scriptengine.readthedocs.io/en/latest/concepts.html#task-context
    The Context is a special dict that allows
    * dotted keys, i.e. c["foo.bar"] is equivalent to c["foo"]["bar"]
    * deep merges of other Mappings (via deepmerge.always_merger)
    * save and load the data to/from a file-like object

    Methods
    -------
    merge(other)
        Deep merges other into the context

    reset(keep=None)
        Deletes all data from the context, except for the keys listed in 'keep'

    save(stream)
        ...

    load(stream)
        ...
    """

    def __getitem__(self, key: Any) -> Any:
        """Return x[key] where key is possibly a dotted key"""
        def iter_getitem(data, subkey):
            try:
                return data[subkey]
            except TypeError:  # dotted key with too many components
                raise KeyError(subkey)
            except KeyError:
                pass
            try:
                first, _, remain = subkey.partition(KEY_SEP)
            except AttributeError:
                raise KeyError(subkey)
            return iter_getitem(data[first], remain)

        try:
            return iter_getitem(self.data, key)
        except KeyError as e:
            raise KeyError(
                f"{key} (subkey {e} not found)" if str(key) != str(e) else key
            ) from None

    def __setitem__(self, key: Any, item: Any) -> None:
        """Set x[key]=item where key is possibly a dotted key"""
        try:
            keys = key.split(KEY_SEP)
        except AttributeError:
            self.data[key] = item
        else:
            d = self.data
            for k in keys[:-1]:
                #             allow overwriting of non-mapping keys
                if k not in d or not isinstance(d[k], Mapping):
                    d[k] = {}
                d = d[k]
            # Make sure that nested dotted keys are resolved!
            d[keys[-1]] = Context(item).data if isinstance(item, Mapping) else item

    def __contains__(self, key: object) -> bool:
        def iter_contains(data, subkey):
            if subkey in data:
                return True
            try:
                first, _, remain = subkey.partition(KEY_SEP)
            except AttributeError:
                return False
            if first in data:
                return iter_contains(data[first], remain)
            return False

        return iter_contains(self.data, key)

    def __str__(self) -> str:
        return f"Context({self.data})"

    def __add__(self, other):
        if isinstance(other, Mapping):
            self.merge(other)
            return self
        return NotImplemented

    def merge(self, other):
        if isinstance(other, Context):
            always_merger.merge(self.data, other.data)
        elif isinstance(other, Mapping):
            always_merger.merge(self.data, other)
        else:
            raise TypeError(f"can not merge Context and {type(other).__name__}")

    def reset(self, keep=None):
        save_copy = Context()
        for k in keep or []:
            if k in self:
                save_copy[k] = self[k]
        self.data.clear()
        for k in save_copy:
            self[k] = save_copy[k]

    def load(self, stream):
        self.data = yaml.safe_load(stream)

    def save(self, stream):
        yaml.dump(self.data, stream, sort_keys=False)


# from dotty_dict import Dotty
# class Context(Dotty):
#     def __init__(self, dictionary=None):
#         super().__init__(dictionary or {}, no_list=True)
