from __future__ import annotations

import dataclasses
from collections.abc import Mapping, Sequence
from decimal import Decimal
from fractions import Fraction
from functools import total_ordering
from numbers import Real, Number
from typing import Any, Self

from .base_classes import Unit, Dimensional
from .dimension import Dimensions, Dimension


__all__ = [
    "Quantity",
    "DerivedUnit",
    "BaseUnit",
]

__version__ = "0.0.8"


@total_ordering
@dataclasses.dataclass(slots=True, frozen=True, eq=False)
class Quantity(Dimensional):
    value: Real | Decimal
    unit: DerivedUnit

    def __str__(self):
        if isinstance(self.unit, BaseUnit):
            return f"{self.value} {self.unit}"
        if isinstance(self.unit, DerivedUnit) and self.unit.factor == 0:
            return f"{self.value} {self.unit}"
        return f"{self.value} × {self.unit}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self}>"

    # region Arithmetic operation handlers
    def __pow__(self, power: int | Fraction | float, modulo=None):
        if not isinstance(power, (float, Decimal)):
            power = Fraction(power)
        if isinstance(self.value, int):
            value = Fraction(self.value)
        else:
            value = self.value
        return Quantity(value ** power, self.unit ** power)

    def __mul__(self, other: Any, /):
        if isinstance(other, Quantity):
            new_unit = self.unit * other.unit
            if not new_unit.dimensions():
                return self.value * other.value * new_unit.factor
            return Quantity(self.value * other.value, new_unit)
        if isinstance(other, Unit):
            return self * other.as_quantity()
        if isinstance(other, (Real, Decimal)):
            return Quantity(self.value * other, self.unit)
        return NotImplemented

    __rmul__ = __mul__

    def __add__(self, other: Any, /):
        if isinstance(other, Quantity):
            if self.unit != other.unit:
                return self + other.convert_to(self.unit)
            return Quantity(self.value + other.value, self.unit)
        if other == 0:  # This allows using sum() on a list of quantities.
            return self
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other: Any, /):
        if isinstance(other, Quantity):
            return self + other.additive_inverse()
        return NotImplemented

    def __rsub__(self, other: Any, /):
        return other + self.additive_inverse()

    def __abs__(self):
        return Quantity(abs(self.value), self.unit)

    def __ceil__(self):
        return Quantity(self.value.__ceil__(), self.unit)

    def __floor__(self):
        return Quantity(self.value.__floor__(), self.unit)

    def __truediv__(self, other: Any, /):
        if isinstance(other, Quantity):
            return self * other.multiplicative_inverse()
        if isinstance(other, Unit):
            return self / other.as_quantity()
        if isinstance(other, (Real, Decimal)):
            return Quantity(self.value / other, self.unit)
        return NotImplemented

    def __rtruediv__(self, other: Any, /):
        if isinstance(other, Quantity):
            return self.multiplicative_inverse() * other
        if isinstance(other, Unit):
            return self.multiplicative_inverse() * other.as_quantity()
        if isinstance(other, (Real, Decimal)):
            return Quantity(
                other / self.value,
                self.unit.multiplicative_inverse()
            )
        return NotImplemented

    def __divmod__(self, other: Any, /):
        if isinstance(other, Quantity):
            if self.unit != other.unit:
                return divmod(self.convert_to(other.unit), other)
            div_, mod_ = divmod(self.value, other.value)
            return div_, Quantity(mod_, self.unit)
        if isinstance(other, Unit):
            return divmod(self, other.as_quantity())
        return NotImplemented

    def __floordiv__(self, other: Any, /):
        if isinstance(other, Quantity):
            new_unit = self.unit / other.unit
            if not new_unit.dimensions():
                return self.value // other.value * new_unit.factor
            return Quantity(self.value // other.value, new_unit)
        if isinstance(other, Unit):
            return self // other.as_quantity()
        if isinstance(other, (Real, Decimal)):
            return Quantity(self.value // other, self.unit)
        return NotImplemented

    def __rfloordiv__(self, other: Any, /):
        if isinstance(other, Quantity):
            new_unit = other.unit / self.unit
            if not new_unit.dimensions():
                return other.value // self.value * new_unit.factor
            return Quantity(other.value // self.value, new_unit)
        if isinstance(other, Unit):
            return other.as_quantity() // self
        if isinstance(other, (Real, Decimal)):
            return Quantity(
                other // self.value,
                self.unit.multiplicative_inverse()
            )
        return NotImplemented

    def __mod__(self, other: Any, /):
        if isinstance(other, Quantity):
            if self.unit != other.unit:
                return self.convert_to(other.unit) % other
            return Quantity(self.value % other.value, self.unit)
        if isinstance(other, Unit):
            return self % other.as_quantity()
        return NotImplemented

    def __neg__(self):
        return Quantity(-self.value, self.unit)

    def __round__(self, n=None):
        return Quantity(self.value.__round__(n), self.unit)
    # endregion

    # region Comparison handlers
    def __eq__(self, other: Any, /):
        if isinstance(other, Quantity):
            if self.dimensions() != other.dimensions():
                return False
            if (self.value * self.unit.si_factor()
                    != other.value * other.unit.si_factor()):
                return False
            return True
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Quantity):
            if self.dimensions() != other.dimensions():
                raise ValueError(f"units must have the same dimensions")
            return (self.value * self.unit.si_factor()
                    > other.value * other.unit.si_factor())
        return NotImplemented
    # endregion

    def dimensions(self):
        return self.unit.dimensions()

    def multiplicative_inverse(self):
        return Quantity(1 / self.value, self.unit.multiplicative_inverse())

    def additive_inverse(self):
        return Quantity(-self.value, self.unit)

    def convert_to(self, other: Unit | Quantity, /):
        """Convert this quantity to another unit.

        This method returns a new Quantity
        which is equivalent to this quantity
        but in the other unit.
        """
        if isinstance(other, Quantity):
            other = other.as_derived_unit()
        if self.unit.dimensions() != other.dimensions():
            raise ValueError(f"target unit must have the same dimensions")
        factor, offset = self.unit.conversion_parameters_to(other)
        if not isinstance(other, DerivedUnit):
            other = other.as_derived_unit()
        return Quantity(self.value * factor + offset, other)

    def convert_to_terms(
        self,
        units: Sequence[Unit],
        sort=False
    ) -> list[Quantity]:
        """Convert this quantity to other units.

        This method returns a list of Quantity objects in the given units,
        the sum of which are equivalent to this quantity.
        """
        if sort:
            units = sorted(units, reverse=True)
        remaining = self
        quantities = []
        for unit in units:
            result, remaining = divmod(remaining, unit)
            quantities.append(result * unit)
        return quantities

    def as_derived_unit(self, symbol: str = None) -> DerivedUnit:
        if self.unit.si_offset() != 0:
            raise ValueError(
                "converting a quantity with an offset unit to a derived unit "
                "doesn't make sense"
            )
        return DerivedUnit(
            symbol,
            self.unit.unit_exponents,
            self.unit.factor * self.value
        )


@dataclasses.dataclass(slots=True, frozen=True, eq=False)
class DerivedUnit(Unit):
    """Represents a product of one or more base units."""
    symbol: str | None
    unit_exponents: Mapping[BaseUnit, Fraction | float]
    factor: Fraction = Fraction(1)
    offset: Fraction = Fraction(0)


    @classmethod
    def using(
        cls,
        ref: Self, /,
        symbol: str | None = None,
        factor: Fraction | float = Fraction(1),
        offset: Fraction | float = Fraction(0),
    ) -> Self:
        return cls(
            symbol,
            ref.unit_exponents,
            ref.factor * factor,
            ref.offset + offset,
        )

    def __str__(self):
        if self.symbol:
            return self.symbol
        if self.factor == 1:
            if self.offset != 0:
                return f"{self._str_with_multiplicands()} + {self.offset}"
            return self._str_with_multiplicands()
        if self.offset == 0:
            return f"{self.factor} {self._str_with_multiplicands()}"
        return f"{self.factor} {self._str_with_multiplicands()} + {self.offset}"

    def __repr__(self):
        if self.factor == 1:
            _expr = self._str_with_multiplicands()
        else:
            _expr = f"{self.factor} {self._str_with_multiplicands()}"
        if self.offset != 0:
            _expr += f" + {self.offset}"

        if self.symbol:
            return f"<{self.__class__.__name__} {self.symbol} = {_expr}>"
        return f"<{self.__class__.__name__} {_expr}>"

    # region Arithmetic operation handlers
    def __pow__(self, power: int | Fraction | float, modulo=None):
        if not isinstance(power, (float, Decimal)):
            power = Fraction(power)
        return DerivedUnit(
            None,
            {
                base_unit: exponent * power
                for base_unit, exponent in self.unit_exponents.items()
            },
            # For some reason, my type checker thinks Fraction ** int is float.
            self.factor ** power  # type: ignore
        )

    def __mul__(self, other: Any, /):
        if isinstance(other, BaseUnit):
            other = other.as_derived_unit()
        if isinstance(other, DerivedUnit):
            base_units = []
            for unit in self.unit_exponents.keys():
                if unit not in base_units:
                    base_units.append(unit)
            for unit in other.unit_exponents.keys():
                if unit not in base_units:
                    base_units.append(unit)

            return DerivedUnit(
                None,
                {
                    base_unit: exponent
                    for base_unit, exponent in {
                        base_unit:
                            self.unit_exponents.get(base_unit, 0) +
                            other.unit_exponents.get(base_unit, 0)
                        for base_unit in base_units
                    }.items()
                    if exponent != 0
                },
                self.factor * other.factor
            )

        if isinstance(other, (Real, Decimal)):
            return Quantity(other, self)
        return NotImplemented

    def __add__(self, other: Any, /):
        if isinstance(other, Number):
            if isinstance(other, int):
                other = Fraction(other)

            return DerivedUnit(
                symbol=None,
                unit_exponents=self.unit_exponents,
                factor=self.factor,
                offset=self.offset + other
            )

        return NotImplemented

    def __truediv__(self, other: Any, /):
        if other == 1:
            return self
        if isinstance(other, DerivedUnit):
            return self * other.multiplicative_inverse()
        return NotImplemented

    def __rtruediv__(self, other: Any, /):
        if other == 1:
            return self.multiplicative_inverse()
        return other * self.multiplicative_inverse()
    # endregion

    def _str_with_multiplicands(self):
        if not self.unit_exponents:
            return "1"
        return " ".join([
            f"{base_unit}^{exponent}" if exponent != 1 else str(base_unit)
            for base_unit, exponent in self.unit_exponents.items()
        ])

    def dimensions(self):
        dimensions = {}
        for base_unit, exponent in self.unit_exponents.items():
            if base_unit.dimension not in dimensions:
                dimensions[base_unit.dimension] = exponent
            else:
                dimensions[base_unit.dimension] += exponent
                if dimensions[base_unit.dimension] == 0:
                    del dimensions[base_unit.dimension]
        return Dimensions(dimensions)

    def si_factor(self):
        factor = self.factor
        for base_unit, exponent in self.unit_exponents.items():
            factor *= base_unit.si_factor() ** exponent
        return factor

    def si_offset(self) -> Fraction | float:
        return self.offset

    def as_quantity(self) -> Quantity:
        return Quantity(1 if not self.offset else 0, self)

    def multiplicative_inverse(self):
        if self.offset:
            raise ValueError("can't invert offset unit")
        return DerivedUnit(
            None,
            {
                base_unit: -exponent
                for base_unit, exponent in self.unit_exponents.items()
            },
            1 / self.factor
        )

    def as_derived_unit(self, symbol: str | None = None) -> DerivedUnit:
        return DerivedUnit(
            symbol,
            self.unit_exponents,
            self.factor,
            self.offset,
        )


@dataclasses.dataclass(slots=True, frozen=True, eq=False)
class BaseUnit(Unit):
    """A unit of measurement which only has one dimension of power 1.

    What the above statement means in layman's terms is that
    a base unit is a unit, which is not a combination of other units.

    For example, the metre is a base unit, the second is a base unit, but
    metres per second is not a base unit.
    """

    symbol: str
    """The symbol of the unit.

    This value is used to generate human-readable representations of
    quantities."""

    dimension: Dimension
    """The dimension of the unit."""

    factor: Fraction
    """The factor by which the base SI unit of the dimension is multiplied by.
    """

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return f"<{self.__class__.__name__} {self}>"

    # region Arithmetic operation handlers
    def __pow__(self, power: int | Fraction | float, modulo=None):
        if not isinstance(power, (float, Decimal)):
            power = Fraction(power)
        return DerivedUnit(None, {self: power})

    def __mul__(self, other: Any, /):
        if isinstance(other, DerivedUnit):
            return self.as_derived_unit() * other

        if isinstance(other, BaseUnit):
            if self == other:
                return self ** 2
            return self.as_derived_unit() * other.as_derived_unit()

        if isinstance(other, (Real, Decimal)):
            return Quantity(other, self.as_derived_unit())
        return NotImplemented

    def __add__(self, other: Any, /):
        if isinstance(other, Number):
            if isinstance(other, int):
                other = Fraction(other)

            return DerivedUnit(
                symbol=None,
                unit_exponents={self: Fraction(1)},
                factor=Fraction(1),
                offset=other
            )

        return NotImplemented

    def __truediv__(self, other: Any, /):
        if other == 1:
            return self
        if isinstance(other, Unit):
            return self * other.multiplicative_inverse()
        return NotImplemented

    def __rtruediv__(self, other: Any, /):
        if other == 1:
            return self.multiplicative_inverse()
        return other * self.multiplicative_inverse()
    # endregion

    def dimensions(self):
        return Dimensions({self.dimension: Fraction(1)})

    def as_derived_unit(self, symbol: str | None = None) -> DerivedUnit:
        return DerivedUnit(symbol, {self: Fraction(1)})

    def as_quantity(self) -> Quantity:
        return Quantity(Fraction(1), self.as_derived_unit())

    def multiplicative_inverse(self) -> DerivedUnit:
        return DerivedUnit(None, {self: Fraction(-1)})

    @classmethod
    def using(
        cls,
        ref: Self, /,
        symbol: str | None = None,
        factor: Fraction | float = Fraction(1),
    ) -> Self:
        return cls(
            symbol,
            ref.dimension,
            ref.si_factor() * factor,
        )

    def si_factor(self) -> Fraction | float:
        return self.factor

    def si_offset(self) -> Fraction | float:
        return Fraction(0)
