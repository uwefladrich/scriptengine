from collections import UserDict
from collections.abc import Mapping
from typing import Any

import yaml
from deepmerge import always_merger

KEY_SEP = "."


class Context(UserDict):
    def __getitem__(self, key: Any) -> Any:
        def _iter_search(data, subkey):
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
            return _iter_search(data[first], remain)

        try:
            return _iter_search(self.data, key)
        except KeyError as e:
            raise KeyError(
                f"{key} (subkey {e} not found)" if str(key) != str(e) else key
            ) from None

    def __setitem__(self, key: Any, item: Any) -> None:
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
            d[keys[-1]] = item

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

    def load(self, stream):
        self.data = yaml.safe_load(stream)

    def save(self, stream):
        yaml.dump(self.data, stream, sort_keys=False)


# from dotty_dict import Dotty
# class Context(Dotty):
#     def __init__(self, dictionary=None):
#         super().__init__(dictionary or {}, no_list=True)
