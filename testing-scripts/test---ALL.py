# encoding: utf-8

__author__ = 'Lex Darlog (DRL)'

from pathlib import Path as _Path
from sys import path as _sys_path
# we might need to add the script dir to sys.path before we proceed:
_module_dir = _Path(__file__).parent
_module_dir_str = str(_module_dir).replace('\\', '/')
if _module_dir_str not in _sys_path:
	_sys_path.append(_module_dir)

from bench_data_container import *


keyboard_interrupt_catch_and_exit(test_from_cmd, *(
	tuple,
	list,
	set,
	frozenset,
	dict,
	OrderedDict,
	SimpleNamespace,
	SimpleNamespaceSlots,
	SimpleNamespaceSlotsSet,
	SimpleNamespaceSlotsFrozen,
	namedtuple,
	NamedTuple,
	Class,
	ClassSlots,
	ClassSlotsSet,
	ClassSlotsFrozen,
	DataClass,
	DataClassSlots,
	DataClassSlotsSet,
	DataClassSlotsFrozen,
	AttrClass,
	AttrClassSlots,
	PydanticBase,
	PydanticDataClass,
	PydanticDataClassSlots,
))
