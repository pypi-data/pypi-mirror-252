from functools import reduce


class UFCS:
    """
    A simple [Uniform Function Call Syntax (UFCS)](https://tour.dlang.org/tour/en/gems/uniform-function-call-syntax-ufcs) implementation in python.

    Example:
    ```py
    UFCS([3, 2, 1]).sorted(key=lambda x: x <= 1).map(lambda x: x * 2).filter(lambda x: x > 3).list().print()
    ```
    """

    def __init__(self, val) -> None:
        self._val = val if not isinstance(val, UFCS) else val._val

    def filter(self, func) -> "UFCS":
        return UFCS(filter(func, self._val))

    def map(self, func) -> "UFCS":
        return UFCS(map(func, self._val))

    def reduce(self, func, start=None):
        return reduce(func, self._val, start)

    def __getattr__(self, __name: str):
        __call = globals().get("__builtins__").get(__name)
        if __call:
            return lambda *args, **kwds: UFCS(__call(self._val, *args, **kwds))
        else:
            return lambda *args, **kwds: getattr(self._val, __name)(*args, **kwds)

    def __repr__(self) -> str:
        return repr(self._val)

    def __str__(self) -> str:
        return str(self._val)

    def __getitem__(self, index) -> any:
        return self._val[index]

    def __iter__(self):
        return iter(self._val)

    def __len__(self) -> int:
        return len(self._val)

    def __eq__(self, __value: object) -> bool:
        return self._val == __value

    def __ne__(self, __value: object) -> bool:
        return self._val != __value

    def __hash__(self) -> int:
        return hash(self._val)
