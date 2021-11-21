# encoding: utf-8
"""
"""

__author__ = 'Lex Darlog (DRL)'

from pathlib import Path as _Path
from sys import path as _sys_path
# we might need to add the script dir to sys.path before we proceed:
_module_dir = _Path(__file__).parent
_module_dir_str = str(_module_dir).replace('\\', '/')
if _module_dir_str not in _sys_path:
	_sys_path.append(_module_dir)


from typing import (
	Any as _Any,
	Dict as _Dict,
	Generator as _Generator,
	Iterable as _Iterable,
	Type as _Type,
	TypeVar as _TypeVar,
	Union as _U,
)
# noinspection PyTypeHints,PyShadowingBuiltins
_T = _TypeVar('T')
# noinspection PyTypeHints
_if = _TypeVar('IntFloat', int, float)

from _bench_types import _attr_names, _type_name, _format_items_list
from _bench_data import *

# optional: progressbar
try:
	# noinspection SpellCheckingInspection
	from tqdm import tqdm as _tqdm
except ImportError:
	# noinspection SpellCheckingInspection
	_tqdm = None
if not callable(_tqdm):
	# noinspection SpellCheckingInspection,PyUnusedLocal
	def _tqdm(iterable: _Iterable[_T] = None, *args, **kwargs):
		"""Dummy tqdm placeholder."""
		return iterable


_byte_kilo_sizes = ('', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi')
_byte_yobi = 'Yi'
_byte_kilo_step = 1024.0


def human_bytes(
	size: _if, size_in_bits=False, space=' ', suffix='B'
):
	"""Format bytes/bits size in a human-readable form."""

	def format_decimal(size_):
		return f'{size_:.3f}'.rstrip('0').rstrip('.')

	sign = -1 if size < 0 else 1
	size *= sign  # make absolute
	if size_in_bits:
		size = size / 8

	for unit in _byte_kilo_sizes:
		if size < _byte_kilo_step:
			return f'{format_decimal(size * sign)}{space}{unit}{suffix}'
		size /= _byte_kilo_step

	# We're in yobibytes.
	if size < _byte_kilo_step:
		return f'{format_decimal(size * sign)}{space}{_byte_yobi}{suffix}'

	# OK, it's ridiculous now, but we're _AT_LEAST_ in thousands of yobibytes.
	# Let's output in scientific notation.

	# The function can still crash if a user provided number so big that it utilizes
	# long math and can't be casted to a float. But if they deal with THAT order
	# of sizes, it would be the least of their problems.
	order = 0
	while size >= _byte_kilo_step:
		size /= _byte_kilo_step
		order += 3
	return f'{format_decimal(size * sign)}*10^{order}{space}{_byte_yobi}{suffix}'


def format_thousands(number: _U[_if, str], spacer="_"):
	"""Format a number, splitting thousands with spacer."""

	number_str = str(number).replace(',', '.').strip()
	sign = ''
	if number_str.startswith('-'):
		sign = '-'
		number_str = number_str.lstrip('-')

	if '.' in number_str:
		number_str = number_str.rstrip('0').rstrip('.')
	number_str = number_str.lstrip('0')

	if not number_str:
		return '0'

	reversed_pieces = list()
	while number_str:
		number_str, piece = number_str[:-3], number_str[-3:]
		reversed_pieces.append(piece)
	return sign + spacer.join(reversed(reversed_pieces))


def test(
	container: _Type[_T] = dict, n=10_000_000, min_str_len=35, as_kwargs=True,
	long_greeting=False, print_attrs_list=False,
):
	attrs_list_str = f': {{\n{_format_items_list(1)}\n}}' if print_attrs_list else ''
	if long_greeting:
		greeting = (
			f"Building a tuple of {format_thousands(n)} <{_type_name(container)}> "
			f"instances, each with {len(_attr_names)} values{attrs_list_str}..."
		)
	else:
		greeting = (
			f"Tuple of {format_thousands(n)} <{_type_name(container)}> "
			f"items{attrs_list_str}..."
		)
	print(greeting)

	data_gen = data_generator(
		container, n=n, min_str_len=min_str_len, as_kwargs=as_kwargs
	)
	big_tuple = tuple(
		_tqdm(data_gen, desc='', total=n, unit=' items')
	)


if __name__ == '__main__':
	keyboard_interrupt_catch_and_exit(
		test,
		ClassSlotsFrozen, n=1_000_000, print_attrs_list=False,
	)
