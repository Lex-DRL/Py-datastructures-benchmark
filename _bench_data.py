# encoding: utf-8
"""
"""

__author__ = 'Lex Darlog (DRL)'

from typing import (
	Any as _Any,
	Dict as _Dict,
	Tuple as _Tuple,
	Type as _Type,
	TypeVar as _TypeVar,
)

from collections import OrderedDict
from functools import partial
from random import choice as _choice
from string import ascii_letters as _letters


_random_char_f = partial(_choice, tuple(_letters))


def data_values_iterator(n=1_000_000, min_str_len=35):
	n = max(n, 1)
	max_len = len(str(n)) + 1  # always have at least one non-numeric char
	max_len = max(max_len, min_str_len)

	float_scale = float(100.0 / n)

	def generate_str(field_i_str: str, number_str: str, n_prefix_chars: int):
		str_padding = ''.join(_random_char_f() for _ in range(n_prefix_chars))
		return f"{field_i_str}:{str_padding}{number_str}"

	def single_item_values(item_i: int):
		neg_i = -item_i
		float_val = item_i * float_scale
		number_str = str(item_i)
		number_len = len(number_str)
		n_prefix_chars = max(0, max_len - number_len)
		return (
			item_i,
			(neg_i, 0),         float_val, generate_str("0", number_str, n_prefix_chars),
			(neg_i, 1), 100.0 + float_val, generate_str("1", number_str, n_prefix_chars),
			(neg_i, 2), 200.0 + float_val, generate_str("2", number_str, n_prefix_chars),
		)

	return map(single_item_values, range(n))


def data_dicts_iterator(n=1_000_000, min_str_len=35):
	def single_item_dict(values_tuple: tuple) -> _Dict[str, _Any]:
		i, it0, f0, s0, it1, f1, s1, it2, f2, s2 = values_tuple
		return OrderedDict(
			i=i,
			it0=it0, f0=f0, s0=s0,
			it1=it1, f1=f1, s1=s1,
			it2=it2, f2=f2, s2=s2,
		)
	return map(single_item_dict, data_values_iterator(n=n, min_str_len=min_str_len))


# noinspection PyTypeHints,PyShadowingBuiltins
_T = _TypeVar('T')


def data_tuple(
	container: _Type[_T], n=1_000_000, min_str_len=35
) -> _Tuple[_T, ...]:
	return tuple(
		container(**x) for x in data_dicts_iterator(n=n, min_str_len=min_str_len)
	)


if __name__ == '__main__':
	from _bench_types import *

	# noinspection DuplicatedCode
	def __test():
		from pprint import pprint as pp

		n = 101
		
		pp(data_tuple(SimpleNamespace, n))
		pp(data_tuple(SimpleNamespaceSlots, n))
		pp(data_tuple(SimpleNamespaceSlotsSet, n))
		pp(data_tuple(SimpleNamespaceSlotsFrozen, n))

		pp(data_tuple(namedtuple, n))
		pp(data_tuple(NamedTuple, n))

		pp(data_tuple(Class, n))
		pp(data_tuple(ClassSlots, n))
		pp(data_tuple(ClassSlotsSet, n))
		pp(data_tuple(ClassSlotsFrozen, n))

		pp(data_tuple(DataClass, n))
		pp(data_tuple(DataClassSlots, n))
		pp(data_tuple(DataClassSlotsSet, n))
		pp(data_tuple(DataClassSlotsFrozen, n))

		pp(data_tuple(AttrClass, n))
		pp(data_tuple(AttrClassSlots, n))

		pp(data_tuple(PydanticBase, n))

		pp(data_tuple(PydanticDataClass, n))
		pp(data_tuple(PydanticDataClassSlots, n))

	__test()
