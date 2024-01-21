from collections.abc import MutableMapping, Mapping
from fractions import Fraction
from numbers import Number
from typing import overload, Self, TYPE_CHECKING

import attrs

from .base_classes import Dimensional


@attrs.define(slots=True, frozen=True, repr=False)
class Dimension:
    name: str
    symbol: str

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.symbol!r})"


class DimensionRegistry(MutableMapping[str, Dimension]):
    def __init__(self, _m=None):
        if _m is not None:
            self._dimensions = dict(_m)
        else:
            self._dimensions = {}

    @overload
    def register(self, dimension: Dimension):
        ...

    @overload
    def register(self, name: str, symbol: str):
        ...

    def register(self, _a, _b=None):
        if isinstance(_a, Dimension) and _b is None:
            self[_a.name] = _a
        elif isinstance(_a, str) and isinstance(_b, str):
            self[_a] = Dimension(name=_a, symbol=_b)
        else:
            raise TypeError("Invalid arguments")

    @overload
    def get_or_register(self, dimension: Dimension) -> Dimension:
        ...

    @overload
    def get_or_register(self, name: str, symbol: str) -> Dimension:
        ...

    def get_or_register(self, _a, _b=None):
        if isinstance(_a, Dimension) and _b is None:
            name = _a.name
            dimension = _a
        elif isinstance(_a, str) and isinstance(_b, str):
            name = _a
            dimension = Dimension(_a, _b)
        else:
            raise TypeError("Invalid arguments")

        if name in self:
            return self[name]
        else:
            self[name] = dimension
            return dimension

    def __setitem__(self, __key, __value):
        if __key in self._dimensions:
            raise ValueError(f"Dimension '{__key}' already exists")
        if __key != __value.name:
            raise ValueError(
                f"key '{__key}' and value name '{__value.name}' must be equal"
            )
        self._dimensions[__key] = __value

    def __delitem__(self, __key):
        raise TypeError(
            f"'{self.__class__.__name__}' object does not support item deletion"
        )

    def __getitem__(self, __key):
        return self._dimensions[__key]

    def __len__(self):
        return len(self._dimensions)

    def __iter__(self):
        return self._dimensions.__iter__()


dimensions: DimensionRegistry = DimensionRegistry()
dimensions.register("mass", "M")
dimensions.register("length", "L")
dimensions.register("luminous intensity", "J")
dimensions.register("time", "T")
dimensions.register("electric current", "I")
dimensions.register("thermodynamic temperature", "Θ")
dimensions.register("amount of substance", "N")


class Dimensions(Mapping[Dimension, Fraction | float], Dimensional):
    _map: dict[Dimension, Fraction | float]

    def __init__(self, mapping: Mapping[Dimension, Fraction | float] = None):
        if mapping is not None:
            self._map = dict(mapping)
        else:
            self._map = {}

    def __str__(self):
        if all(exponent == 0 for exponent in self._map.values()):
            return "1"

        return " ".join(
            [
                f"{dimension.symbol}^{exponent}"
                for dimension, exponent in self._map.items()
                if exponent != 0
            ]
        )

    def __repr__(self):
        return f"<{self.__class__.__name__} {self._map}>"

    def dimensions(self) -> Self:
        return self

    def multiplicative_inverse(self) -> Self:
        return Dimensions({d: -p for d, p in self._map.items()})

    def __getitem__(self, __key):
        return self._map.__getitem__(__key)

    def __len__(self):
        return self._map.__len__()

    def __iter__(self):
        return self._map.__iter__()

    # region Arithmetic operations
    def __mul__(self, other):
        if isinstance(other, Dimensions):
            return Dimensions(
                {
                    k: (self.get(k, 0) + other.get(k, 0))
                    for k in set(self.keys()) | set(other.keys())
                }
            )
        else:
            return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other):
        if other == 1:
            return self
        if isinstance(other, Dimensions):
            return self * other.multiplicative_inverse()
        elif isinstance(other, Number):
            return self
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, Dimensions):
            return other * self.multiplicative_inverse()
        elif isinstance(other, Number):
            return self.multiplicative_inverse()
        else:
            return NotImplemented

    def __pow__(self, power, modulo=None):
        if isinstance(power, (float, Fraction)):
            return Dimensions({d: p * power for d, p in self._map.items()})
        elif isinstance(power, int):
            power = Fraction(power)
            return Dimensions({d: p * power for d, p in self._map.items()})
        else:
            return NotImplemented

    def __neg__(self):
        return self

    def __pos__(self):
        return self

    def __abs__(self):
        return self

    # endregion


__all__ = ["Dimension", "Dimensions", "DimensionRegistry", "dimensions"]
