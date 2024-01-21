from fractions import Fraction as _Fraction

from ...constants import speed_of_light_in_vacuum as _speed_of_light_in_vacuum

from ..imperial import mile as _mile, foot as _foot
from ..si_base.metre import metre as _metre, kilometre as _kilometre
from ..si_base.second import second as _second
from ..common.time import year as _year

light_mile = (_mile / _speed_of_light_in_vacuum).as_derived_unit("light-mile")
light_foot = (_foot / _speed_of_light_in_vacuum).as_derived_unit("light-foot")
light_metre = (
    _metre / _speed_of_light_in_vacuum).as_derived_unit("light-metre")
light_kilometre = (
    _kilometre / _speed_of_light_in_vacuum).as_derived_unit("light-kilometre")
microfortnight = (_Fraction(756, 625) * _second).as_derived_unit("μfn")
sidereal_day = (
    _Fraction(86164_0905, 1_0000) * _second).as_derived_unit("Sidereal day")
sol = (88_775 * _second).as_derived_unit("sol")
dog_year = (_Fraction(1, 7) * _year).as_derived_unit("dog year")
