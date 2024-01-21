from fractions import Fraction as _Fraction

from ... import BaseUnit as _BaseUnit
from ..si_base.metre import metre as _metre

foot = _BaseUnit.using(_metre, "ft", _Fraction(381, 1250))

twip = _BaseUnit.using(foot, "twip", _Fraction(1, 17280))
thou = _BaseUnit.using(foot, "th", _Fraction(1, 12000))
barleycorn = _BaseUnit.using(foot, "barleycorn", _Fraction(1, 36))
inch = _BaseUnit.using(foot, "in", _Fraction(1, 12))
hand = _BaseUnit.using(foot, "hh", _Fraction(1, 3))

yard = _BaseUnit.using(foot, "yd", _Fraction(3))
chain = _BaseUnit.using(foot, "ch", _Fraction(66))
furlong = _BaseUnit.using(foot, "fur", _Fraction(660))
mile = _BaseUnit.using(foot, "mi", _Fraction(5280))
league = _BaseUnit.using(foot, "lea", _Fraction(15840))

# Maritime units
fathom = _BaseUnit.using(_metre, "ftm", _Fraction(1852, 1000))
cable = _BaseUnit.using(fathom, "cable", _Fraction(100))
nautical_mile = _BaseUnit.using(cable, "nmi", _Fraction(10))

# Gunter's survey units
link = _BaseUnit.using(foot, "link", _Fraction(66, 100))
rod = _BaseUnit.using(link, "rod", _Fraction(25))
