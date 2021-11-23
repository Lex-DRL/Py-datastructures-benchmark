# encoding: utf-8
"""
"""

__author__ = 'Lex Darlog (DRL)'

# noinspection PyPep8Naming
from typing import (
	Callable as _C,
	Iterator as _Iterator,
	Optional as _O,
	Type as _Type,
	TypeVar as _TypeVar,
)

from functools import partial as _partial
from random import choice as _choice
from string import ascii_letters as _letters

from _bench_types import *
from _bench_types import (
	_Defaults,
	_tpl_values,
	_read_attribs,
)


# noinspection PyTypeHints,PyShadowingBuiltins
_T = _TypeVar('T')


_random_char_f = _partial(_choice, tuple(_letters))


def data_values_iterator(n=1_000_000, min_str_len=35, ) -> _Iterator[_tpl_values]:
	n = max(int(n), 1)
	max_padded_number_len = max(
		2,  # even with single-digit number, it will be 2 wit at least 1 char
		len(str(n)) + 1,  # always have at least one non-numeric char
		int(min_str_len) - 2,  # 2 chars are taken by '0:'
	)
	float_scale = 100.0 / (n + 2)

	def generate_str(field_i_str: str, number_str: str, n_prefix_chars: int):
		str_padding = ''.join(_random_char_f() for _ in range(n_prefix_chars))
		return f"{field_i_str}:{str_padding}{number_str}"

	def single_item_values(item_i: int):
		neg_i = -item_i
		float_val = float((item_i + 1.0) * float_scale)
		number_str = str(item_i)
		number_len = len(number_str)
		n_prefix_chars = max(1, max_padded_number_len - number_len)
		return (
			item_i,
			(neg_i, 0), -float_val, generate_str("0", number_str, n_prefix_chars),
			(neg_i, 1), -float_val - 100.0, generate_str("1", number_str, n_prefix_chars),
			(neg_i, 2), -float_val - 200.0, generate_str("2", number_str, n_prefix_chars),
		)

	return map(single_item_values, range(1, n + 1))


# To achieve the most representative results, measuring the ACTUAL instance
# creation and not something else (like iteration over source data),
# we need to:
# 1. unpack the values to individual variables
# 2. pass them to constructor manually, one by one, as separate arguments


def _construct_with_keywords(container: _Type, values: _tpl_values):
	i, it0, f0, s0, it1, f1, s1, it2, f2, s2 = values
	return container(
		i=i, it0=it0, f0=f0, s0=s0, it1=it1, f1=f1, s1=s1, it2=it2, f2=f2, s2=s2,
	)


# noinspection PyUnusedLocal
def _construct_dummy(container: _Type, values: _tpl_values):
	"""
	A special function which does almost everything others do, EXCEPT for
	the actual object creation.

	Used to measure common overhead.
	"""
	i, it0, f0, s0, it1, f1, s1, it2, f2, s2 = values
	return s2


# noinspection PyUnusedLocal
def _construct_tuple(container: _Type[tuple], values: _tpl_values):
	i, it0, f0, s0, it1, f1, s1, it2, f2, s2 = values
	return (
		i, it0, f0, s0, it1, f1, s1, it2, f2, s2,
	)


# noinspection PyUnusedLocal
def _construct_list(container: _Type[list], values: _tpl_values):
	i, it0, f0, s0, it1, f1, s1, it2, f2, s2 = values
	return [
		i, it0, f0, s0, it1, f1, s1, it2, f2, s2,
	]


# noinspection PyUnusedLocal
def _construct_set(container: _Type[set], values: _tpl_values):
	i, it0, f0, s0, it1, f1, s1, it2, f2, s2 = values
	return {
		i, it0, f0, s0, it1, f1, s1, it2, f2, s2,
	}


# noinspection PyUnusedLocal
def _construct_frozenset(container: _Type[frozenset], values: _tpl_values):
	i, it0, f0, s0, it1, f1, s1, it2, f2, s2 = values
	# unfortunately, there's no way to construct a set truly fairly, it has to be
	# done by iterating over another iterable:
	return frozenset(values)


def select_constructor(container: _Type[_T]) -> _C[[_tpl_values], _T]:
	if container is None:
		return _partial(_construct_dummy, container)
	map_to_f = {
		frozenset: _construct_frozenset,
		set: _construct_set,
		list: _construct_list,
		tuple: _construct_tuple,
	}
	# yes, we do check for EXACT type match:
	f = map_to_f[container] if container in map_to_f else _construct_with_keywords
	return _partial(f, container)


_dummy_i = _Defaults.i
_dummy_it0 = _Defaults.it0
_dummy_it1 = _Defaults.it1
_dummy_it2 = _Defaults.it2
_dummy_f0 = _Defaults.f0
_dummy_f1 = _Defaults.f1
_dummy_f2 = _Defaults.f2
_dummy_s0 = _Defaults.s0
_dummy_s1 = _Defaults.s1
_dummy_s2 = _Defaults.s2


# noinspection PyUnusedLocal
def _read_attribs_dummy(self):
	return (
		_dummy_i,
		_dummy_it0, _dummy_f0, _dummy_s0,
		_dummy_it1, _dummy_f1, _dummy_s1,
		_dummy_it2, _dummy_f2, _dummy_s2,
	)


def _read_attribs_from_dict(self):
	return (
		self["i"],
		self["it0"], self["f0"], self["s0"],
		self["it1"], self["f1"], self["s1"],
		self["it2"], self["f2"], self["s2"],
	)


def _read_attribs_from_seq(self):
	return (
		self[0],
		self[1], self[2], self[3],
		self[4], self[5], self[6],
		self[7], self[8], self[9],
	)


def _read_attribs_from_set(self):
	# again, not exactly fair (we iterate and don't do it one-by-one),
	# but it's the only thing we can do:
	i, it0, f0, s0, it1, f1, s1, it2, f2, s2 = self
	return (
		i,
		it0, f0, s0,
		it1, f1, s1,
		it2, f2, s2,
	)


def select_attribs_reader(container: _Type[_T]) -> _C[[_T], _tpl_values]:
	if container is None:
		return _read_attribs_dummy
	if issubclass(container, (set, frozenset)):
		return _read_attribs_from_set
	if issubclass(container, dict):
		return _read_attribs_from_dict
	if issubclass(container, (list, tuple)):
		return _read_attribs_from_seq
	return _read_attribs


# noinspection PyUnusedLocal,DuplicatedCode
def _set_attribs_dummy(self):
	i = _dummy_i
	it0 = _dummy_it0
	f0 = _dummy_f0
	s0 = _dummy_s0
	it1 = _dummy_it1
	f1 = _dummy_f1
	s1 = _dummy_s1
	it2 = _dummy_it2
	f2 = _dummy_f2
	s2 = _dummy_s2
	res = (i, it0, f0, s0, it1, f1, s1, it2, f2, s2, )
	return res


# noinspection DuplicatedCode
def _set_attribs(self):
	i = _dummy_i
	it0 = _dummy_it0
	f0 = _dummy_f0
	s0 = _dummy_s0
	it1 = _dummy_it1
	f1 = _dummy_f1
	s1 = _dummy_s1
	it2 = _dummy_it2
	f2 = _dummy_f2
	s2 = _dummy_s2
	res = (i, it0, f0, s0, it1, f1, s1, it2, f2, s2, )
	self.i = i
	self.it0 = it0
	self.f0 = f0
	self.s0 = s0
	self.it1 = it1
	self.f1 = f1
	self.s1 = s1
	self.it2 = it2
	self.f2 = f2
	self.s2 = s2
	return res


# noinspection DuplicatedCode
def _set_attribs_for_dict(self: dict):
	i = _dummy_i
	it0 = _dummy_it0
	f0 = _dummy_f0
	s0 = _dummy_s0
	it1 = _dummy_it1
	f1 = _dummy_f1
	s1 = _dummy_s1
	it2 = _dummy_it2
	f2 = _dummy_f2
	s2 = _dummy_s2
	res = (i, it0, f0, s0, it1, f1, s1, it2, f2, s2, )
	self["i"] = i
	self["it0"] = it0
	self["f0"] = f0
	self["s0"] = s0
	self["it1"] = it1
	self["f1"] = f1
	self["s1"] = s1
	self["it2"] = it2
	self["f2"] = f2
	self["s2"] = s2
	return res


# noinspection DuplicatedCode
def _set_attribs_for_seq(self):
	i = _dummy_i
	it0 = _dummy_it0
	f0 = _dummy_f0
	s0 = _dummy_s0
	it1 = _dummy_it1
	f1 = _dummy_f1
	s1 = _dummy_s1
	it2 = _dummy_it2
	f2 = _dummy_f2
	s2 = _dummy_s2
	res = (i, it0, f0, s0, it1, f1, s1, it2, f2, s2, )
	self[0] = i
	self[1] = it0
	self[2] = f0
	self[3] = s0
	self[4] = it1
	self[5] = f1
	self[6] = s1
	self[7] = it2
	self[8] = f2
	self[9] = s2
	return res


# noinspection DuplicatedCode
def _set_attribs_for_set(self):
	i = _dummy_i
	it0 = _dummy_it0
	f0 = _dummy_f0
	s0 = _dummy_s0
	it1 = _dummy_it1
	f1 = _dummy_f1
	s1 = _dummy_s1
	it2 = _dummy_it2
	f2 = _dummy_f2
	s2 = _dummy_s2
	res = (i, it0, f0, s0, it1, f1, s1, it2, f2, s2, )
	self.update(res)
	return res


def select_attribs_setter(container: _Type[_T]) -> _O[_C[[_T], _tpl_values]]:
	if container is None:
		return _set_attribs_dummy
	if issubclass(container, (tuple, frozenset)):
		return None
	if issubclass(container, set):
		return _set_attribs_for_set
	if issubclass(container, dict):
		return _set_attribs_for_dict
	if issubclass(container, list):
		return _set_attribs_for_seq
	return _set_attribs


def _data_generator(
	container: _Type[_T] = None, n=1_000_000, min_str_len=35,
) -> _Iterator[_T]:
	constructor = select_constructor(container)
	return (
		constructor(args) for args in data_values_iterator(n=n, min_str_len=min_str_len)
	)


if __name__ == '__main__':
	# noinspection DuplicatedCode
	def __test(n=69):
		from pprint import pprint as pp

		pp(tuple(_data_generator(tuple, n)))
		pp(tuple(_data_generator(list, n)))
		pp(tuple(_data_generator(set, n)))
		pp(tuple(_data_generator(frozenset, n)))
		pp(tuple(_data_generator(dict, n)))
		pp(tuple(_data_generator(OrderedDict, n)))

		pp(tuple(_data_generator(SimpleNamespace, n)))
		pp(tuple(_data_generator(SimpleNamespaceSlots, n)))
		pp(tuple(_data_generator(SimpleNamespaceSlotsSet, n)))
		pp(tuple(_data_generator(SimpleNamespaceSlotsFrozen, n)))

		pp(tuple(_data_generator(namedtuple, n)))
		pp(tuple(_data_generator(NamedTuple, n)))

		pp(tuple(_data_generator(Class, n)))
		pp(tuple(_data_generator(ClassSlots, n)))
		pp(tuple(_data_generator(ClassSlotsSet, n)))
		pp(tuple(_data_generator(ClassSlotsFrozen, n)))

		pp(tuple(_data_generator(DataClass, n)))
		pp(tuple(_data_generator(DataClassSlots, n)))
		pp(tuple(_data_generator(DataClassSlotsSet, n)))
		pp(tuple(_data_generator(DataClassSlotsFrozen, n)))

		pp(tuple(_data_generator(AttrClass, n)))
		pp(tuple(_data_generator(AttrClassSlots, n)))

		pp(tuple(_data_generator(PydanticBase, n)))

		pp(tuple(_data_generator(PydanticDataClass, n)))
		pp(tuple(_data_generator(PydanticDataClassSlots, n)))

	keyboard_interrupt_catch_and_exit(
		__test
	)
