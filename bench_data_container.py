# encoding: utf-8
"""
"""

__author__ = 'Lex Darlog (DRL)'

import warnings as _warnings

with _warnings.catch_warnings():
	# some modules like to raise warnings on import
	_warnings.simplefilter('ignore')

	from pathlib import Path as _Path
	from sys import path as _sys_path

# we might need to add the script dir to sys.path before we proceed:
_module_dir = _Path(__file__).parent
_module_dir_str = str(_module_dir).replace('\\', '/')
if _module_dir_str not in _sys_path:
	_sys_path.append(_module_dir)


# noinspection PyPep8Naming
from typing import (
	Any as _Any,
	Dict as _Dict,
	Generator as _Generator,
	Iterable as _Iterable,
	NamedTuple as _NamedTuple,
	Optional as _O,
	Type as _Type,
	TypeVar as _TypeVar,
	Union as _U,
)
# noinspection PyTypeHints,PyShadowingBuiltins
_T = _TypeVar('T')
# noinspection PyTypeHints
_if = _TypeVar('IntFloat', int, float)

import time as _time
from dataclasses import dataclass as _dataclass

from _bench_types import (
	_attr_names,
	_type_name,
	_format_items_list,
	_read_attribs, _read_attribs_from_dict, _read_attribs_from_seq,
	_set_attribs, _set_attribs_for_dict, _set_attribs_for_seq,
)
from _bench_data import *

with _warnings.catch_warnings():
	# some modules like to raise warnings on import
	_warnings.simplefilter('ignore')

	from pympler.asizeof import asizeof as _asizeof

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


@_dataclass
class TestResult:
	container: _Type
	n: int
	size_bytes: _O[int] = None
	create_time: float = 0.0
	attr_access_time: _O[float] = None
	attr_set_time: _O[float] = None

	@staticmethod
	def format_result_value(name: str, value, indent='\t'):
		if name == 'n':
			return f'{indent}{name}: {format_thousands(value)}'
		if name == 'size_bytes':
			return f'{indent}{name}: {human_bytes(value)}'
		if name.endswith('_time'):
			return f'{indent}{name}: {value:.3f} seconds'
		return f'{indent}{name}: {value}'

	def formatted_summary(self):
		summ_values_str = '\n'.join(
			self.format_result_value(k, v) for k, v in self.__dict__.items()
			if v is not None and k != 'container'
		)
		return f'{_type_name(self.container)}:\n{summ_values_str}'


def test(
	container: _Type = dict, n=10_000_000, min_str_len=35, as_kwargs=True,
	test_ram=True, test_read=True, test_set=True, leave_progress=False,
	long_greeting=False, print_attrs_list=False, print_summary=True,
	**extra_kwargs_swallower
):
	type_name = _type_name(container)
	attrs_list_str = f': {{\n{_format_items_list(1)}\n}}' if print_attrs_list else ''
	if long_greeting:
		greeting = (
			f"\nBuilding a tuple of {format_thousands(n)} unique <{type_name}> "
			f"instances, each with {len(_attr_names)} values{attrs_list_str}..."
		)
	else:
		greeting = (
			f"\nTuple of {format_thousands(n)} unique <{type_name}> "
			f"items{attrs_list_str}..."
		)
	print(greeting)
	res = TestResult(container, n)

	data_gen = data_generator(
		container, n=n, min_str_len=min_str_len, as_kwargs=as_kwargs
	)
	start_time = _time.process_time()
	big_tuple = tuple(
		_tqdm(data_gen, desc='', total=n, unit=' items', )
	)
	res.create_time = _time.process_time() - start_time

	if test_ram:
		warning_msg = ' (this might take long)' if n > 100_000 else ''
		print(f"Measuring size of the entire tuple in RAM{warning_msg}...")
		res.size_bytes = _asizeof(big_tuple)

	def measure_iteration_over_items(items: _Iterable):
		start_t = _time.process_time()
		for instance in _tqdm(
			items,
			desc='', total=n, leave=leave_progress, unit=' items',
		):
			pass
		return _time.process_time() - start_t

	attr_access_f = _read_attribs
	attr_set_f = _set_attribs
	if as_kwargs:
		if issubclass(container, dict):
			attr_access_f = _read_attribs_from_dict
			attr_set_f = _set_attribs_for_dict
	else:
		attr_access_f = _read_attribs_from_seq
		attr_set_f = _set_attribs_for_seq

	if test_read:
		print(f"Test reading values from <{type_name}> instances...")
		res.attr_access_time = measure_iteration_over_items(
			map(attr_access_f, big_tuple)
		)

	if test_set:
		# use the same instance-values-dict to set attribs for ALL the instances:
		test_values_dict: dict = next(data_generator(
			None, n=1, min_str_len=min_str_len, as_kwargs=True
		))
		test_values_iter = (test_values_dict for _ in range(n))
		print(f"Test setting values for <{type_name}> instances...")
		res.attr_set_time = measure_iteration_over_items(
			map(attr_set_f, big_tuple, test_values_iter)
		)

	if print_summary:
		print(f'\n{res.formatted_summary()}')
	return res


def test_from_cmd(container: type, **forced_kwargs):
	import sys
	from distutils.util import strtobool as bbb

	if not isinstance(container, type):
		raise TypeError(f"Unknown container type: {container}")

	def to_int(val):
		if isinstance(val, str):
			val = val.strip()
		if not val:
			return 0
		return int(val)

	def to_bool(val):
		if not val:
			return False
		if isinstance(val, str):
			val = bbb(val)
		return bool(val)

	args_converters = dict(
		n=to_int, min_str_len=to_int, as_kwargs=to_bool,
		test_ram=to_bool, test_read=to_bool, test_set=to_bool, leave_progress=to_bool,
		long_greeting=to_bool, print_attrs_list=to_bool, print_summary=to_bool,
	)

	kwargs = dict()
	args = iter(sys.argv[1:])
	for arg in args:
		val: _O[str] = None
		assert isinstance(arg, str)
		arg = arg.lstrip('/\\-')
		if '=' in arg:
			arg_split = [x.strip() for x in arg.split('=')]
			if len(arg_split) > 1:
				arg, val, *_ = arg_split
				val = val.strip()
				if not val:
					val = None
			else:
				arg = arg_split[0]

		if arg in args_converters:
			converter = args_converters[arg]
			# noinspection PyBroadException
			while not val:
				try:
					val = next(args)
				except StopIteration:
					break
				val = val.lstrip('=')
			if arg not in forced_kwargs and val:
				kwargs[arg] = converter(val)

	test(container, **forced_kwargs, **kwargs)


if __name__ == '__main__':
	keyboard_interrupt_catch_and_exit(
		test,
		ClassSlotsFrozen, n=100_000, print_attrs_list=False,
	)
