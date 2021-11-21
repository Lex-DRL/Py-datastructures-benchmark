# encoding: utf-8
"""
"""

__author__ = 'Lex Darlog (DRL)'

from typing import (
	Any as _Any,
	Dict as _Dict,
	Generator as _Generator,
	Type as _Type,
	TypeVar as _TypeVar,
)

from collections import OrderedDict
from functools import partial as _partial
from random import choice as _choice
from string import ascii_letters as _letters

from _bench_types import *


_random_char_f = _partial(_choice, tuple(_letters))


def _data_values_iterator(n=1_000_000, min_str_len=35, ):
	n = max(int(n), 1)
	max_padded_number_len = max(
		2,  # even with single-digit number, it will be 2 wit at least 1 char
		len(str(n)) + 1,  # always have at least one non-numeric char
		int(min_str_len) - 2,  # 2 chars are taken by '0:'
	)
	float_scale = float(100.0 / n)

	def generate_str(field_i_str: str, number_str: str, n_prefix_chars: int):
		str_padding = ''.join(_random_char_f() for _ in range(n_prefix_chars))
		return f"{field_i_str}:{str_padding}{number_str}"

	def single_item_values(item_i: int):
		neg_i = -item_i
		float_val = item_i * float_scale
		number_str = str(item_i)
		number_len = len(number_str)
		n_prefix_chars = max(1, max_padded_number_len - number_len)
		return (
			item_i,
			(neg_i, 0),         float_val, generate_str("0", number_str, n_prefix_chars),
			(neg_i, 1), 100.0 + float_val, generate_str("1", number_str, n_prefix_chars),
			(neg_i, 2), 200.0 + float_val, generate_str("2", number_str, n_prefix_chars),
		)

	return map(single_item_values, range(1, n + 1))


def _data_dicts_iterator(n=1_000_000, min_str_len=35, ):
	def single_item_dict(values_tuple: tuple) -> _Dict[str, _Any]:
		i, it0, f0, s0, it1, f1, s1, it2, f2, s2 = values_tuple
		return OrderedDict(
			i=i,
			it0=it0, f0=f0, s0=s0,
			it1=it1, f1=f1, s1=s1,
			it2=it2, f2=f2, s2=s2,
		)
	return map(single_item_dict, _data_values_iterator(n=n, min_str_len=min_str_len))


# noinspection PyTypeHints,PyShadowingBuiltins
_T = _TypeVar('T')


def data_generator(
	container: _Type[_T], n=1_000_000, min_str_len=35, as_kwargs=True,
) -> _Generator[_T, _Any, None]:
	if as_kwargs:
		return (
			container(**kws) for kws in _data_dicts_iterator(n=n, min_str_len=min_str_len)
		)
	return (
		container(args) for args in _data_values_iterator(n=n, min_str_len=min_str_len)
	)


if __name__ == '__main__':
	# noinspection DuplicatedCode
	def __test():
		from pprint import pprint as pp

		n = 69
		
		pp(tuple(data_generator(tuple, n, as_kwargs=False)))
		pp(tuple(data_generator(list, n, as_kwargs=False)))
		pp(tuple(data_generator(set, n, as_kwargs=False)))
		pp(tuple(data_generator(frozenset, n, as_kwargs=False)))
		pp(tuple(data_generator(dict, n)))
		pp(tuple(data_generator(OrderedDict, n)))

		pp(tuple(data_generator(SimpleNamespace, n)))
		pp(tuple(data_generator(SimpleNamespaceSlots, n)))
		pp(tuple(data_generator(SimpleNamespaceSlotsSet, n)))
		pp(tuple(data_generator(SimpleNamespaceSlotsFrozen, n)))

		pp(tuple(data_generator(namedtuple, n)))
		pp(tuple(data_generator(NamedTuple, n)))

		pp(tuple(data_generator(Class, n)))
		pp(tuple(data_generator(ClassSlots, n)))
		pp(tuple(data_generator(ClassSlotsSet, n)))
		pp(tuple(data_generator(ClassSlotsFrozen, n)))

		pp(tuple(data_generator(DataClass, n)))
		pp(tuple(data_generator(DataClassSlots, n)))
		pp(tuple(data_generator(DataClassSlotsSet, n)))
		pp(tuple(data_generator(DataClassSlotsFrozen, n)))

		pp(tuple(data_generator(AttrClass, n)))
		pp(tuple(data_generator(AttrClassSlots, n)))

		pp(tuple(data_generator(PydanticBase, n)))

		pp(tuple(data_generator(PydanticDataClass, n)))
		pp(tuple(data_generator(PydanticDataClassSlots, n)))

	__test()
