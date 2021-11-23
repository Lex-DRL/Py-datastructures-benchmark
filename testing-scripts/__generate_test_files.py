# encoding: utf-8
"""
"""

__author__ = 'Lex Darlog (DRL)'

from typing import *

from pathlib import Path as _Path
from sys import path as _sys_path
# we might need to add the script dir to sys.path before we proceed:
# __file__ = 'P:/1-Scripts/_Python/Py-datastructures-benchmark/testing-scripts/bench_data_container.py'
_tests_dir = _Path(__file__).absolute().parent
_module_dir = _tests_dir.parent
_module_dir_str = str(_module_dir).replace('\\', '/')
if _module_dir_str not in _sys_path:
	_sys_path.append(_module_dir_str)

from itertools import chain
out_file_base = _tests_dir / 'test-'


template = r"""# encoding: utf-8

__author__ = 'Lex Darlog (DRL)'

from pathlib import Path as _Path
from sys import path as _sys_path
# we might need to add the script dir to sys.path before we proceed:
_module_dir = _Path(__file__).absolute().parent.parent
_module_dir_str = str(_module_dir).replace('\\', '/')
if _module_dir_str not in _sys_path:
	_sys_path.append(_module_dir_str)

from bench_data_container import *

""".split('\n')

last_line = 'keyboard_interrupt_catch_and_exit(test_from_cmd, {})'


def format_options(**opts):
	return ', '.join(f'{k}={v!r}' for k, v in opts.items())


options_per_type: Dict[str, Dict] = dict(
	tuple=dict(),
	list=dict(),
	set=dict(),
	frozenset=dict(),
	dict=dict(),
	OrderedDict=dict(),
	SimpleNamespace=dict(),
	SimpleNamespaceSlots=dict(),
	SimpleNamespaceSlotsSet=dict(),
	SimpleNamespaceSlotsFrozen=dict(),
	namedtuple=dict(test_set=False),
	NamedTuple=dict(test_set=False),
	Class=dict(),
	ClassSlots=dict(),
	ClassSlotsSet=dict(),
	ClassSlotsFrozen=dict(),
	DataClass=dict(),
	DataClassSlots=dict(),
	DataClassSlotsSet=dict(),
	DataClassSlotsFrozen=dict(),
	AttrClass=dict(),
	AttrClassSlots=dict(),
	PydanticBase=dict(),
	PydanticDataClass=dict(),
	PydanticDataClassSlots=dict(),
)

for out_type, options in options_per_type.items():
	func_args = format_options(**options)
	func_args = ', '.join([out_type, func_args]) if func_args else out_type

	file_path = f"{out_file_base}{out_type}.py"
	print(file_path)
	with open(file_path, 'wt', encoding='utf-8', newline='\n') as f:
		f.writelines(
			f"{x}\n" for x in chain(template, [last_line.format(func_args), ])
		)
print('\nDONE!\n\n')