# encoding: utf-8
"""
"""

__author__ = 'Lex Darlog (DRL)'

from typing import (
	Tuple as _Tuple,
	NamedTuple as _NamedTuple,
)

from collections import namedtuple as _namedtuple
from dataclasses import (
	dataclass as _dataclass,
	field as _field,
)
from itertools import chain as _chain
import string as _string
from types import SimpleNamespace

import attr as _attr


_tpl_ii = _Tuple[int, int]
_attr_names = (
	'i',
	'it0', 'f0', 's0',
	'it1', 'f1', 's1',
	'it2', 'f2', 's2',
)
# print(', '.join(_attr_names))
_slots = tuple(_chain(_attr_names, [
	'__eq__', '__ne__',
	# '__hash__',
	# '__lt__', '__le__', '__gt__', '__ge__',
	'__repr__',
	# '__weakref__',
]))
_slots_set = set(_slots)
_slots_frozen = frozenset(_slots)


class _Defaults:
	i: int = 69
	# Yes, I know, assigning a collection as default argument is anti-pattern,
	# but it's a tuple. And it's guaranteed to be set explicitly to new value
	# for each instance in this specific benchmark.
	it0: _tpl_ii = (-69, 0)
	it1: _tpl_ii = (-69, 1)
	it2: _tpl_ii = (-69, 2)
	f0 = 69.0
	f1 = 169.0
	f2 = 269.0
	s0 = '0:aBcXXx69'
	s1 = '1:aBcXXx69'
	s2 = '2:aBcXXx69'

	def __init__(self):
		raise TypeError(f"{self.__class__} is static.")


def _default_it0_f() -> _tpl_ii:
	return -69, 0


def _default_it1_f() -> _tpl_ii:
	return -69, 1


def _default_it2_f() -> _tpl_ii:
	return -69, 2


# --------------------------- SimpleNamespaceSlots ---------------------------

# slotted SimpleNamespace examples are ridiculous since we basically
# re-implement C-side init in Python, but for the sake of experiment...


class SimpleNamespaceSlots(SimpleNamespace):
	__slots__ = _slots

	# we intentionally re-implement __init__, to make use of slots
	# noinspection PyMissingConstructor
	def __init__(
		self, i: int = _Defaults.i,
		it0: _tpl_ii = _Defaults.it0, f0: float = _Defaults.f0, s0: str = _Defaults.s0,
		it1: _tpl_ii = _Defaults.it1, f1: float = _Defaults.f1, s1: str = _Defaults.s1,
		it2: _tpl_ii = _Defaults.it2, f2: float = _Defaults.f2, s2: str = _Defaults.s2,
	):
		# and for the same reason we do not call super.__init__
		self.i: int = i
		self.it0: _tpl_ii = it0
		self.f0: float = f0
		self.s0: str = s0
		self.it1: _tpl_ii = it1
		self.f1: float = f1
		self.s1: str = s1
		self.it2: _tpl_ii = it2
		self.f2: float = f2
		self.s2: str = s2


class SimpleNamespaceSlotsSet(SimpleNamespace):
	__slots__ = _slots_set

	# noinspection PyMissingConstructor
	def __init__(
		self, i: int = _Defaults.i,
		it0: _tpl_ii = _Defaults.it0, f0: float = _Defaults.f0, s0: str = _Defaults.s0,
		it1: _tpl_ii = _Defaults.it1, f1: float = _Defaults.f1, s1: str = _Defaults.s1,
		it2: _tpl_ii = _Defaults.it2, f2: float = _Defaults.f2, s2: str = _Defaults.s2,
	):
		self.i: int = i
		self.it0: _tpl_ii = it0
		self.f0: float = f0
		self.s0: str = s0
		self.it1: _tpl_ii = it1
		self.f1: float = f1
		self.s1: str = s1
		self.it2: _tpl_ii = it2
		self.f2: float = f2
		self.s2: str = s2


class SimpleNamespaceSlotsFrozen(SimpleNamespace):
	__slots__ = _slots_frozen

	# noinspection PyMissingConstructor
	def __init__(
		self, i: int = _Defaults.i,
		it0: _tpl_ii = _Defaults.it0, f0: float = _Defaults.f0, s0: str = _Defaults.s0,
		it1: _tpl_ii = _Defaults.it1, f1: float = _Defaults.f1, s1: str = _Defaults.s1,
		it2: _tpl_ii = _Defaults.it2, f2: float = _Defaults.f2, s2: str = _Defaults.s2,
	):
		self.i: int = i
		self.it0: _tpl_ii = it0
		self.f0: float = f0
		self.s0: str = s0
		self.it1: _tpl_ii = it1
		self.f1: float = f1
		self.s1: str = s1
		self.it2: _tpl_ii = it2
		self.f2: float = f2
		self.s2: str = s2


# -------------------------------- NamedTuple --------------------------------

namedtuple = _namedtuple('namedtuple', _attr_names, )


# noinspection DuplicatedCode
class NamedTuple(_NamedTuple):
	i: int = _Defaults.i
	it0: _tpl_ii = _Defaults.it0
	f0: float = _Defaults.f0
	s0: str = _Defaults.s0
	it1: _tpl_ii = _Defaults.it1
	f1: float = _Defaults.f1
	s1: str = _Defaults.s1
	it2: _tpl_ii = _Defaults.it2
	f2: float = _Defaults.f2
	s2: str = _Defaults.s2


# ------------------------------- simple Class -------------------------------


class Class:
	def __init__(
		self, i: int = _Defaults.i,
		it0: _tpl_ii = _Defaults.it0, f0: float = _Defaults.f0, s0: str = _Defaults.s0,
		it1: _tpl_ii = _Defaults.it1, f1: float = _Defaults.f1, s1: str = _Defaults.s1,
		it2: _tpl_ii = _Defaults.it2, f2: float = _Defaults.f2, s2: str = _Defaults.s2,
	):
		self.i: int = i
		self.it0: _tpl_ii = it0
		self.f0: float = f0
		self.s0: str = s0
		self.it1: _tpl_ii = it1
		self.f1: float = f1
		self.s1: str = s1
		self.it2: _tpl_ii = it2
		self.f2: float = f2
		self.s2: str = s2


class ClassSlots:
	__slots__ = _slots

	def __init__(
		self, i: int = _Defaults.i,
		it0: _tpl_ii = _Defaults.it0, f0: float = _Defaults.f0, s0: str = _Defaults.s0,
		it1: _tpl_ii = _Defaults.it1, f1: float = _Defaults.f1, s1: str = _Defaults.s1,
		it2: _tpl_ii = _Defaults.it2, f2: float = _Defaults.f2, s2: str = _Defaults.s2,
	):
		self.i: int = i
		self.it0: _tpl_ii = it0
		self.f0: float = f0
		self.s0: str = s0
		self.it1: _tpl_ii = it1
		self.f1: float = f1
		self.s1: str = s1
		self.it2: _tpl_ii = it2
		self.f2: float = f2
		self.s2: str = s2


class ClassSlotsSet:
	__slots__ = _slots_set

	def __init__(
		self, i: int = _Defaults.i,
		it0: _tpl_ii = _Defaults.it0, f0: float = _Defaults.f0, s0: str = _Defaults.s0,
		it1: _tpl_ii = _Defaults.it1, f1: float = _Defaults.f1, s1: str = _Defaults.s1,
		it2: _tpl_ii = _Defaults.it2, f2: float = _Defaults.f2, s2: str = _Defaults.s2,
	):
		self.i: int = i
		self.it0: _tpl_ii = it0
		self.f0: float = f0
		self.s0: str = s0
		self.it1: _tpl_ii = it1
		self.f1: float = f1
		self.s1: str = s1
		self.it2: _tpl_ii = it2
		self.f2: float = f2
		self.s2: str = s2


class ClassSlotsFrozen:
	__slots__ = _slots_frozen

	def __init__(
		self, i: int = _Defaults.i,
		it0: _tpl_ii = _Defaults.it0, f0: float = _Defaults.f0, s0: str = _Defaults.s0,
		it1: _tpl_ii = _Defaults.it1, f1: float = _Defaults.f1, s1: str = _Defaults.s1,
		it2: _tpl_ii = _Defaults.it2, f2: float = _Defaults.f2, s2: str = _Defaults.s2,
	):
		self.i: int = i
		self.it0: _tpl_ii = it0
		self.f0: float = f0
		self.s0: str = s0
		self.it1: _tpl_ii = it1
		self.f1: float = f1
		self.s1: str = s1
		self.it2: _tpl_ii = it2
		self.f2: float = f2
		self.s2: str = s2


# --------------------------------- DataClass ---------------------------------


# We do unsafe_hash, just to be able to put items into set.
# They're ne not mutated in this benchmark.


# noinspection DuplicatedCode
@_dataclass(order=True, unsafe_hash=True, frozen=False, )
class DataClass:
	i: int = _Defaults.i
	it0: _tpl_ii = _field(default_factory=_default_it0_f)
	f0: float = _Defaults.f0
	s0: str = _Defaults.s0
	it1: _tpl_ii = _field(default_factory=_default_it1_f)
	f1: float = _Defaults.f1
	s1: str = _Defaults.s1
	it2: _tpl_ii = _field(default_factory=_default_it2_f)
	f2: float = _Defaults.f2
	s2: str = _Defaults.s2


# The only way to use slots for python pre-3.10 is via inheritance:


# noinspection PyBroadException
try:
	# python 3.10: built-in support for slots:
	# noinspection DuplicatedCode,PyArgumentList
	@_dataclass(order=True, unsafe_hash=True, frozen=False, slots=True, )
	class DataClassSlots:
		i: int = _Defaults.i
		it0: _tpl_ii = _field(default_factory=_default_it0_f)
		f0: float = _Defaults.f0
		s0: str = _Defaults.s0
		it1: _tpl_ii = _field(default_factory=_default_it1_f)
		f1: float = _Defaults.f1
		s1: str = _Defaults.s1
		it2: _tpl_ii = _field(default_factory=_default_it2_f)
		f2: float = _Defaults.f2
		s2: str = _Defaults.s2
except Exception:
	# noinspection DuplicatedCode
	class DataClassSlots(DataClass):
		__slots__ = _slots


# noinspection DuplicatedCode
class DataClassSlotsSet(DataClass):
	__slots__ = _slots_set


# noinspection DuplicatedCode
class DataClassSlotsFrozen(DataClass):
	__slots__ = _slots_frozen


# ----------------------------- attrs: validators -----------------------------


_val_int = _attr.validators.instance_of(int)
_val_tpl = _attr.validators.instance_of(tuple)
_val_flt = _attr.validators.instance_of(float)
_val_str = _attr.validators.instance_of(str)


def _val_i(inst, attr: _attr.Attribute, value):
	# print('types:\t' + ',\t'.join(
	# 	f'{type(x)}' for x in (inst, attr, value)
	# ))
	# print('values:\n' + ',\n'.join(
	# 	repr(x) for x in (inst, attr, value)
	# ))
	_val_int(inst, attr, value)
	assert isinstance(
		inst, (AttrClass, AttrClassSlots)
	)
	assert isinstance(value, int)
	if value < 0:
		raise ValueError(f"'{attr.name}' must be positive int (got: {value!r})")


def _val_it_f(i: int):
	def _val_it_x(inst, attr: _attr.Attribute, value):
		"""A tuple validator mimicking some real-world checks."""
		_val_tpl(inst, attr, value)
		assert isinstance(
			inst, (AttrClass, AttrClassSlots)
		)
		assert isinstance(value, tuple)

		def error(suffix=''):
			return ValueError(
				f"'{attr.name}' must be a tuple of 2 ints{suffix} (got: {value!r})"
			)

		if len(value) != 2:
			raise error()
		a, b = value
		if a > 0:
			raise error(', first being negative')
		if b != i:
			raise error(f', second being {i}')

	_val_it_x.__name__ = f'_val_it{i}'
	return _val_it_x


_val_it0 = _val_it_f(0)
_val_it1 = _val_it_f(1)
_val_it2 = _val_it_f(2)


# noinspection PyShadowingBuiltins
def _val_flt_f(i: int, min=0.0, max=100.0):
	def _val_f_x(inst, attr: _attr.Attribute, value):
		_val_flt(inst, attr, value)
		assert isinstance(
			inst, (AttrClass, AttrClassSlots)
		)
		assert isinstance(value, float)
		if not(min <= value <= max):
			raise ValueError(
				f"'{attr.name}' must be a float in range: "
				f"[{min:.2f}, {max:.2f}] (got: {value!r})"
			)

	_val_f_x.__name__ = f'_val_f{i}'
	return _val_f_x


_val_f0 = _val_flt_f(0, 0.0, 100.0)
_val_f1 = _val_flt_f(1, 100.0, 200.0)
_val_f2 = _val_flt_f(2, 200.0, 300.0)


def _val_s_f(i: int):
	i_str = str(i)

	def _val_s_x(inst, attr: _attr.Attribute, value):
		_val_str(inst, attr, value)
		assert isinstance(
			inst, (AttrClass, AttrClassSlots)
		)
		assert isinstance(value, str)

		def error(suffix=''):
			return ValueError(
				f"'{attr.name}' must be a string in format: "
				f"'{i}:RandomPaddingLettersWithNoZeroes{{i}}'; got: {value!r}{suffix}"
			)

		split = value.split(':')
		if len(split) != 2:
			raise error()
		if split[0] != i_str:
			raise error(f" (starting int {split[0]!r} != {i_str})")

		b = split[1].lstrip(_string.ascii_letters)
		if b.startswith('0') and b != '0':
			raise error(f" (there are zeroes in int-padding part: {b!r})")
		if not b:
			raise error(" (there's no int at the end)")

		try:
			b_int = int(b)
		except ValueError:
			raise error(f" (there's {b!r} at the end instead of valid int)")
		if b_int != inst.i or b == '-0':
			raise error(f" (trailing int {b!r} is not equal to 'i' value: {inst.i})")

	_val_s_x.__name__ = f'_val_s{i_str}'
	return _val_s_x


_val_s0 = _val_s_f(0)
_val_s1 = _val_s_f(1)
_val_s2 = _val_s_f(2)


# ------------------------------ attrs: classes ------------------------------


# noinspection DuplicatedCode
@_attr.s(auto_detect=True, hash=True, frozen=False, slots=False, )
class AttrClass:
	# Even though attrs claims type-hint syntax works, attribs defined in such way
	# won't be slotted. I.e., `i: int = 69` wont work.
	# So for consistency let's define them in a same full way for both classes:
	i: int = _attr.ib(_Defaults.i, validator=_val_i, )
	# noinspection PyDataclass
	it0: _tpl_ii = _attr.ib(factory=_default_it0_f, validator=_val_it0, )
	f0: float = _attr.ib(_Defaults.f0, validator=_val_f0, )
	s0: str = _attr.ib(_Defaults.s0, validator=_val_s0, )
	# noinspection PyDataclass
	it1: _tpl_ii = _attr.ib(factory=_default_it1_f, validator=_val_it1, )
	f1: float = _attr.ib(_Defaults.f1, validator=_val_f1, )
	s1: str = _attr.ib(_Defaults.s1, validator=_val_s1, )
	# noinspection PyDataclass
	it2: _tpl_ii = _attr.ib(factory=_default_it2_f, validator=_val_it2, )
	f2: float = _attr.ib(_Defaults.f2, validator=_val_f2, )
	s2: str = _attr.ib(_Defaults.s2, validator=_val_s2, )


# noinspection DuplicatedCode
@_attr.s(auto_detect=True, hash=True, frozen=False, slots=True, )
class AttrClassSlots:
	i: int = _attr.ib(_Defaults.i, validator=_val_i, )
	# noinspection PyDataclass
	it0: _tpl_ii = _attr.ib(factory=_default_it0_f, validator=_val_it0, )
	f0: float = _attr.ib(_Defaults.f0, validator=_val_f0, )
	s0: str = _attr.ib(_Defaults.s0, validator=_val_s0, )
	# noinspection PyDataclass
	it1: _tpl_ii = _attr.ib(factory=_default_it1_f, validator=_val_it1, )
	f1: float = _attr.ib(_Defaults.f1, validator=_val_f1, )
	s1: str = _attr.ib(_Defaults.s1, validator=_val_s1, )
	# noinspection PyDataclass
	it2: _tpl_ii = _attr.ib(factory=_default_it2_f, validator=_val_it2, )
	f2: float = _attr.ib(_Defaults.f2, validator=_val_f2, )
	s2: str = _attr.ib(_Defaults.s2, validator=_val_s2, )


# --------------------------------- pydantic ---------------------------------
