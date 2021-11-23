# encoding: utf-8
"""
"""

__author__ = 'Lex Darlog (DRL)'

import warnings as _warnings

with _warnings.catch_warnings():
	# some modules like to raise warnings on import
	_warnings.simplefilter('ignore')

	from gc import collect as _gc_collect
	from pathlib import Path as _Path
	from sys import path as _sys_path

# we might need to add the script dir to sys.path before we proceed:
_module_dir = _Path(__file__).parent
_module_dir_str = str(_module_dir).replace('\\', '/')
if _module_dir_str not in _sys_path:
	_sys_path.append(_module_dir)


# noinspection PyPep8Naming
from typing import (
	Callable as _C,
	Iterable as _Iterable,
	Optional as _O,
	Tuple as _Tuple,
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
	_tpl_values,

	_attr_names,
	_type_name,
	_format_items_list,
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
	container: _O[_Type]
	size_bytes: _O[int] = None
	create_time: _if = 0.0
	attr_access_time: _O[_if] = None
	attr_set_time: _O[_if] = None

	@staticmethod
	def format_result_value(name: str, value, indent='\t'):
		if name == 'container':
			return f'{indent}{name}: {_type_name(value)}'
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
		type_name = (
			'dummy run' if (self.container is None) else _type_name(self.container)
		)
		return f'{type_name}:\n{summ_values_str}'


def test(
	*tested_containers: _Type,
	n=1_000_000, min_str_len=35,
	test_ram=True, test_read=True, test_set=True,
	leave_progress=False,
	long_greeting=False, print_attrs_list=False, print_summary=True,
	**extra_kwargs_swallower
):
	n_str = format_thousands(n)
	warning_msg = ' (this might take long)' if n > 100_000 else ''
	ram_test_msg = f"Measuring size of the entire tuple in RAM{warning_msg}..."

	def build_source_data_tuple() -> _Tuple[_tpl_values, ...]:
		attrs_list_str = f': {{\n{_format_items_list(1)}\n}}' if print_attrs_list else ''
		if long_greeting:
			greeting = (
				f"\nPre-generating a common tuple of {n_str} unique data tuples"
				f", each with {len(_attr_names)} values{attrs_list_str}..."
			)
		else:
			greeting = (
				f"\nTuple of {n_str} unique data tuples{attrs_list_str}..."
			)
		print(greeting)

		data_gen = data_values_iterator(n=n, min_str_len=min_str_len, )
		return tuple(
			_tqdm(data_gen, desc='', total=n, unit=' items', )
		)

	prepared_data = build_source_data_tuple()
	dummy = TestResult(None, create_time=0.0, attr_access_time=0.0, attr_set_time=0.0)
	dummy_runs = TestResult(None, create_time=0, attr_access_time=0, attr_set_time=0)
	dummy_constructor: _C[[_tpl_values], _T] = select_constructor(None)
	dummy_attr_reader = select_attribs_reader(None)
	dummy_attr_setter = select_attribs_setter(None)

	# noinspection SpellCheckingInspection
	def tuple_with_tqdm(iterable: _Iterable[_T]) -> _Tuple[float, _Tuple[_T, ...]]:
		seq = _tqdm(iterable, desc='', total=n, leave=leave_progress, unit=' items', )
		start_time = _time.process_time()
		res_tuple = tuple(seq)
		return _time.process_time() - start_time, res_tuple

	# noinspection SpellCheckingInspection
	def measure_with_tqdm(items: _Iterable):
		start_t = _time.process_time()
		# noinspection PyUnusedLocal
		for instance in _tqdm(
			items, desc='', total=n, leave=leave_progress, unit=' items',
		):
			pass
		return _time.process_time() - start_t

	def test_single_container(container: _Type):
		if not isinstance(container, type):
			raise TypeError(f"Unknown container type: {container}")

		type_name = _type_name(container)
		constructor: _C[[_tpl_values], _T] = select_constructor(container)
		attr_reader = select_attribs_reader(container)
		attr_setter = select_attribs_setter(container)

		result = TestResult(container)

		print(f"\nCreating a tuple of {n_str} <{type_name}> instances:")
		print(
			"Evaluating base-level creation overhead, not involving "
			"actual instance creation..."
		)
		dummy_t, _dummy = tuple_with_tqdm(
			map(dummy_constructor, prepared_data)
		)
		dummy.create_time += dummy_t
		dummy_runs.create_time += 1
		del _dummy

		print(
			f"Creating the actual tuple of <{type_name}> items..."
		)
		result.create_time, big_tuple = tuple_with_tqdm(
			map(constructor, prepared_data)
		)

		if test_ram:
			print(ram_test_msg)
			result.size_bytes = _asizeof(big_tuple)
			print(human_bytes(result.size_bytes))
		_gc_collect()

		if test_read and attr_reader is not None:
			print("Testing attribute-access time:")
			print("Evaluating base-level read overhead...")
			dummy.attr_access_time += measure_with_tqdm(
				map(dummy_attr_reader, big_tuple)
			)
			dummy_runs.attr_access_time += 1

			print(f"Reading values from <{type_name}> instances...")
			result.attr_access_time = measure_with_tqdm(
				map(attr_reader, big_tuple)
			)

		if test_set and attr_setter is not None:
			print("Testing attribute-set time:")
			print("Evaluating base-level setting overhead...")
			dummy.attr_set_time += measure_with_tqdm(
				map(dummy_attr_setter, big_tuple)
			)
			dummy_runs.attr_set_time += 1

			print(f"Setting values for <{type_name}> instances...")
			result.attr_set_time = measure_with_tqdm(
				map(attr_setter, big_tuple)
			)

		del big_tuple
		_gc_collect()
		return result

	all_results = tuple(
		test_single_container(cont) for cont in tested_containers
	)

	# calculate average base-level times (for more precision):
	dummy.create_time /= dummy_runs.create_time if dummy_runs.create_time > 0 else 1
	dummy.attr_access_time /= (
		dummy_runs.attr_access_time if dummy_runs.attr_access_time > 0 else 1
	)
	dummy.attr_set_time /= (
		dummy_runs.attr_set_time if dummy_runs.attr_set_time > 0 else 1
	)

	print(f"\nBenchmark complete: {n_str} items.")

	for res in all_results:
		res.create_time -= dummy.create_time
		if res.attr_access_time is not None:
			res.attr_access_time -= dummy.attr_access_time
		if res.attr_set_time is not None:
			res.attr_set_time -= dummy.attr_set_time

		if print_summary:
			print(f'\n{res.formatted_summary()}')

	if not(print_summary and len(tested_containers) > 1):
		return all_results

	print(f"\n{'=' * 40}\nRelative results:")

	def print_value_summary(
		attr_getter: _C, val_name='Instance creation time',
		val_formatter=lambda v: f'{v:.4f}', unit=' seconds'
	):
		max_val = max(
			attr_getter(x) for x in all_results if attr_getter(x) is not None
		)
		if max_val < 0.0001:
			print(f"{val_name} - all values are too small")
			return

		print(
			f"\n{val_name} (max = {val_formatter(max_val)}{unit}, "
			f"{val_formatter(max_val*100/n)} per 100 instances):"
		)
		for percent, tp_nm in sorted(
			(100.0 * attr_getter(x) / max_val, _type_name(x.container))
			for x in all_results if attr_getter(x) is not None
		):
			print(f'\t{percent:.3f}% - {tp_nm}')

	if test_ram:
		print_value_summary(lambda x: x.size_bytes, 'RAM usage', human_bytes, '')

	print_value_summary(lambda x: x.create_time, 'Instance creation time')

	if test_read:
		print_value_summary(lambda x: x.attr_access_time, 'Attribute-access time')

	if test_set:
		print_value_summary(lambda x: x.attr_set_time, 'Attribute-set time')

	return all_results


def test_from_cmd(*containers: type, **forced_kwargs):
	import sys
	from distutils.util import strtobool as bbb

	def to_int(value):
		if isinstance(value, str):
			value = value.strip()
		if not value:
			return 0
		return int(value)

	def to_bool(value):
		if not value:
			return False
		if isinstance(value, str):
			value = bbb(value)
		return bool(value)

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

	test(*containers, **forced_kwargs, **kwargs)


if __name__ == '__main__':
	keyboard_interrupt_catch_and_exit(
		test,
		ClassSlotsFrozen, n=100_000, print_attrs_list=False,
	)
