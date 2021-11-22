# encoding: utf-8
"""
"""

__author__ = 'Lex Darlog (DRL)'

from pathlib import Path as _Path
from subprocess import check_call
import sys
# we might need to add the script dir to sys.path before we proceed:
_module_dir = _Path(__file__).parent
_module_dir_str = str(_module_dir).replace('\\', '/')
if _module_dir_str not in sys.path:
	sys.path.append(_module_dir)

from bench_data_container import *

tests = (
	"tuple",
	"list",
	"set",
	"frozenset",
	"dict",
	"OrderedDict",
	"SimpleNamespace",
	"SimpleNamespaceSlots",
	"SimpleNamespaceSlotsSet",
	"SimpleNamespaceSlotsFrozen",
	"namedtuple",
	"NamedTuple",
	"Class",
	"ClassSlots",
	"ClassSlotsSet",
	"ClassSlotsFrozen",
	"DataClass",
	"DataClassSlots",
	"DataClassSlotsSet",
	"DataClassSlotsFrozen",
	"AttrClass",
	"AttrClassSlots",
	"PydanticBase",
	"PydanticDataClass",
	"PydanticDataClassSlots",
)


def main():
	python_exe_path = sys.executable
	print(python_exe_path)

	args = sys.argv[1:]
	file_base = _module_dir / 'test-'
	for test in tests:
		file_path = f"{file_base}{test}.py"
		check_call([python_exe_path, file_path, *args])


if __name__ == '__main__':
	keyboard_interrupt_catch_and_exit(main)
