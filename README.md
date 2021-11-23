# Python data-structures benchmark

## TLDR:

`attrs` > (`__slots__` + `@dataclass`) > `@dataclass` > `NamedTuple` > `tuple` > `dict` > `set` > `OrderedDict`

## Motivation

This repo was inspired by a small debate I had in comments under this video:

[![mCoding: Which Python @dataclass is best? Feat. Pydantic, NamedTuple, attrs...](https://img.youtube.com/vi/vCLetdhswMg/mqdefault.jpg)](https://www.youtube.com/watch?v=vCLetdhswMg&lc=Ugz_dxz6I-KD8Pvn_MF4AaABAg)

The author's ([mCoding](https://www.youtube.com/channel/UCaiL2GDNpLYH6Wokkk1VNcg)) claims contradicted with what I've previously heard from other sources, one of which being another YouTube video on the subject (it's a russian channel, quite a respectable one):

[![Диджитализируй: Эффективно работаем со сложными структурами данных в Python 3.7+](https://img.youtube.com/vi/tsEG0WM3m_M/mqdefault.jpg)](https://www.youtube.com/watch?v=tsEG0WM3m_M)

Specifically, the disparity in RAM consumption is much more pronounced on the graphs that mCoding (James Murphy) provides. Not to mention that according to his results, plain class with `__slots__` consumes **LESS** than even a tuple containing the same data. Which looked hard to believe for me.

So hard, that it motivated me to finally write a small toolset to actually test it.

## Testing methodology

<details>
<summary>Detailed description</summary>
  
The benchmarking scripts here are designed to: 
1. intentionally break low-level optimisations that Python might do *(such as multiple objects pointing to the same area in memory)*;
2. have the actual data somewhat representative of real-life usage scenarios *(e.g., it's not just ints or floats or strings from a pre-defined set)*;
3. be reproducible *(where possible, more on this at the very end, in Conclusions section)*.

So it seems to me the dumbest possible approach is the best one here:
1. When testing each container datatype, we need to create a big enough set (tuple) of this container instances, each having unique values for all of it's attributes. They need to be unique not just inside this instance, but across the whole set.
2. Attributes need to be of various types at once. I came up with this attributes layout:
	* i: int - number of the instance. (for this example, let's say it's 42)
	* 3 floats: `f0`, `f1`, `f2`.

		f0 ranges from 0 to -100 across the whole set. Similarly, f1 is in `[-100, -200)` range, f2 is in `[-200, -300)`. Negative numbers prevent them from being collapsed with `i` if they happen to have the same value and the tested container is `set()`.
	* 3 sub-tuples as pairs of ints:
		- `it0` *(short for int-tuple)* = (-i, 0). *i.e., (-42, 0)*
		- `it1` = (-i, 1)
		- `it2` = (-i, 2)
	* 3 strings: `s0`, `s1`, `s2` in format like this: `"0:aBcXXx42"`.  Where:
		* first char is 0 for `s0`, 1 for `s1`, 2 for `s2`.
		* `aBcXXx` is a random string of ASCII letters - both upper- and lowercase, unique for each of 3 strings.
		* 42 is the actual `i` value.
		* the total string length is the same across the set. Random characters are used as padding for smaller number. 
		
	All of the above ensures each attribute for each instance across the set has it's own unique value. It also guarantees this underlying data always has the same size *(exception: python internally optimizes all the ints in `[-5, 256]` range - see [stackoverflow](https://stackoverflow.com/questions/306313/is-operator-behaves-unexpectedly-with-integers) - but it will be negligible considering total number of instances we'll create)*.
	And it prevents Python from optimizing anything under the hood (like it might be, if we used just leading zeros instead of random chars).
3. Then, we generate a big set of those values, enough to fill GiBs of RAM *(it's millions of instances)*. We go that big to average out results.
4. And finally, we start testing each type of data container for:
	* how fast it's instance is created *(with `time.process_time()`)*
	* how fast those attributes are:
		* accessed (read)
		* set
	* how much RAM all the instances take in total *(with `pympler.asizeof()`)*
5. Obviously, instance creation or attribute reading/setting is done differently for different container types. But the corresponding functions are made to be as close as possible.
	
	Furthermore, for each measured time-sensitive aspect (create/get/set), a "dummy" run performed, which does all the same stuff except for the actual measured thing. I.e., in case of attribute setting - it would unpack values, build a temporary tuple of them (if setters for other types do that), but it won't actually set attributes.
	This "dummy run" is performed multiple times, their results are averaged and **subtracted** from the results of each tested type. This removes any common denominator and leaves us with a pure overhead caused by each container type.
</details>

## Tested container types

1. Standard types:
	* tuple
	* list
	* set
	* frozenset
	* dict
	* OrderedDict
	* regular class
2. "Advanced" standard types:
	* SimpleNamespace
	* namedtuple (both old-style factory-type and new Typed)
	* `@dataclass`
3. External packages:
	* `@attr.s` from `attr` package
	* `@pydantic.dataclasses.dataclass`
	* `pydantic.BaseModel`

Wherever possible, I also tried to make a slotted variant. And in addition to defining the `__slots__` attribute itself as a standard `tuple()`, I tried `__slots__` as `set()` and `frozenset()` just to see if it makes difference. In theory - it should, considering how much checking against presence in set is praised.

Though, even ahead of time I was pretty sure that some nuances of implementation of specific advanced classes *(like `SimpleNamespace`)* would stop slots from actually working, but I kept those anyway.

Another note:
`attrs` and `pydantic` classes all have validators, since that's the core reason to use them. They don't do anything too fancy, just mimic some really basic validation. Specifically, they check that all 10 assigned values match the format explained above. 

## Requirements

All the scripts make use of f-strings, so Python 3.6 (I guess, not tested).

I ran it on Python `3.7.9`.

Extra packages:
* attrs
* pydantic
* pympler
* tqdm

## Usage

TLDR:

`python test---ALL.py n=100_000`

<details>
<summary>Options</summary>

Under `testing-scripts` folder, there's a separate script named `test-{DataType}.py` for each container. They can be just launched from command line / double-clicking.

However, launching them one by one would cause the initial big set of values to be re-generated on each launch. Therefore, there's also `test---ALL.py` which generates this pool of data once and tests each container with the same attribute values from it.

Keep in mind that while script runs, it uses 1.5x-2x of RAM consumed by the tested data type itself, especially when you enabled `test_ram`.

Also, you can use this repo programmatically, `import bench_data_container`.

When launched from command line, the following arguments supported - as `arg=val`, `/arg val` or `-arg val`:
* `n` = 1_000_000. Number of instances to create.
	
	**ATTENTION:** 1 million is specified by default. It's good for benchmarking, but it will eat up your RAM  and take LOOONG to finish.
* `min_str_len` = 35. This is how long generated strings need to be.
	
	Obviously, if you specify 2 here but create 10k items, the script will detect it and make all the strings as long as needed to make them all the same size. I.e., to fit: `"0:"` prefix + at least one random letter + the longest number. I.e, `"0:z1000"` - or 7 in this case.
* `test_ram` = `False`. Whether to measure memory consumption.
	
	**ATTENTION:** this is by far the longest part of benchmark. My tests have shown that consumed memory scales proportionally anyway, so it's off by default.
* `test_read` = `True`. Whether to test attribute-read speed (for those types that support it).
* `test_set` = `True`. Whether to test attribute-assign speed (for those types that support it).
* `leave_progress` = `False`. Whether to keep progress-bar for each performed measurement after it's finished. The main progressbar for initial data generation is always kept (unless `no_prints` is `True`).
* `long_greeting` = `False`. If `True`, shows a bit more detailed prompt for initial data generation.
* `print_attrs_list` = `False`. If `True`, appends the list of names and types for the attributes on created instances.
* `print_summary` = `True`. By default, outputs a summary with results for each type, as well as combined chart.
* `no_prints` = `False`. Suppress all the prints (useful when called from code).
* `no_progress` = `False`. Display no progress bars. *(They also won't be shown - with no errors - if `tqdm` package is not installed).*
</details>

## Test results

With all the preamble out of the way, here's' the stuff you came for.

I've ran the benchmark two times - with 300K items and with 5M - on AMD Ryzen 2700x with 32 GiB of RAM.

Detailed results are  in attached files *(look at the very end for summary, sorted by overhead[^pyd_dataclass_note])*:
* [___result_300_000.txt](https://github.com/Lex-DRL/Py-datastructures-benchmark/blob/main/___result_300_000.txt)
* [___result_5_000_000.txt](https://github.com/Lex-DRL/Py-datastructures-benchmark/blob/main/___result_5_000_000.txt)

### 300 K

|                | RAM | create | read | set |
| -------------- | --- | ------ | ---- | --- |
| **MAX VALUES** | 423.432 MiB | 20.0300 sec | 0.1088 sec | 26.2344 sec |

| data container | RAM | create | read | set |
| -------------- | --- | ------ | ---- | --- |
| tuple       | 49.189% | 0.150% | 28.161% | ❌ |
| list        | 50.270% | 0.774% | 13.793% | 0.298% |
| set         | 90.270% | 2.802% | 71.264%[^set_note] | 1.429%[^set_note] |
| frozenset   | 90.270% | 2.880% | 56.897%[^set_note] | ❌ |
| dict        | 65.405% | 0.930% | 42.529% | 0.417% |
| OrderedDict | 100% | 3.660% | 28.161% | 0.536% |
| SimpleNamespace            | 68.649% | 1.086% | 42.529% | 0.357% |
| SimpleNamespaceSlots       | 65.405% | 2.334% | 28.161% | 0.298% |
| SimpleNamespaceSlotsSet    | 65.405% | 2.490% | 28.161% | 0.298% |
| SimpleNamespaceSlotsFrozen | 65.405% | 2.334% | 13.793% | 0.298% |
| namedtuple       | 49.189% | 1.944% | 13.793% | ❌ |
| NamedTuple       | 49.189% | 1.944% | 13.793% | ❌ |
| Class            | 54.595% | 1.944% | 28.161% | 0.357% |
| ClassSlots       | 48.649% | 1.944% | 28.161% | 0.298% |
| ClassSlotsSet    | 48.649% | 2.022% | 28.161% | 0.298% |
| ClassSlotsFrozen | 48.649% | 2.100% | 28.161% | 0.357% |
| DataClass            | 54.595% | 2.100% | 42.529% | 0.417% |
| DataClassSlots       | 57.297% | 2.334% | 28.161% | 0.298% |
| DataClassSlotsSet    | 57.297% | 2.334% | 28.161% | 0.357% |
| DataClassSlotsFrozen | 57.297% | 2.256% | 28.161% | 0.357% |
| AttrClass      | 54.595% | 25.502% | 56.897% | 0.417% |
| AttrClassSlots | 49.189% | 26.126% | 42.529% | 0.357% |
| PydanticDataClass[^pyd_dataclass_note] | 88.108% | 100% | 49.713% | 69.506% |
| PydanticBase      | 69.189% | 94.149% | 100% | 100% |

### 5 M

|                | RAM | create | read | set |
| -------------- | --- | ------ | ---- | --- |
| **MAX VALUES** | 6.892 GiB | 348.85 sec | 1.84 sec | 448.6369 sec |

| data container | RAM | create | read | set |
| -------------- | --- | ------ | ---- | --- |
| tuple                  | 49.189% | 0.212% | 23.573% | ❌ |
| list                   | 50.270% | 1.395% | 21.875% | 0.288% |
| set                    | 90.270% | 4.221% | 69.429%[^set_note] | 1.535%[^set_note] |
| frozenset              | 90.270% | 4.266% | 70.279%[^set_note] | ❌ |
| dict                   | 65.405% | 0.862% | 38.859% | 0.386% |
| OrderedDict            | 100%    | 4.691% | 40.557% | 0.532% |
| SimpleNamespace            | 68.649% | 1.292% | 44.803% | 0.410% |
| SimpleNamespaceSlots       | 65.405% | 3.092% | 32.914% | 0.323% |
| SimpleNamespaceSlotsSet    | 65.405% | 3.106% | 33.764% | 0.313% |
| SimpleNamespaceSlotsFrozen | 65.405% | 3.088% | 30.367% | 0.327% |
| namedtuple              | 49.189% | 2.586% | 22.724% | ❌ |
| NamedTuple              | 49.189% | 2.671% | 21.875% | ❌ |
| Class                   | 54.595% | 2.076% | 53.295% | 0.417% |
| ClassSlots              | 48.649% | 2.667% | 29.518% | 0.313% |
| ClassSlotsSet           | 48.649% | 2.680% | 32.065% | 0.320% |
| ClassSlotsFrozen        | 48.649% | 2.685% | 30.367% | 0.323% |
| DataClass            | 54.595% | 2.340% | 49.049% | 0.441% |
| DataClassSlots       | 57.297% | 2.998% | 32.914% | 0.323% |
| DataClassSlotsSet    | 57.297% | 2.989% | 32.065% | 0.323% |
| DataClassSlotsFrozen | 57.297% | 3.030% | 29.518% | 0.323% |
| AttrClass         | 54.595% | 25.881% | 50.747% | 0.417% |
| AttrClassSlots    | 49.189% | 26.652% | 30.367% | 0.313% |
| PydanticDataClass[^pyd_dataclass_note] | 88.108% | 100%    | 60.937% | 69,901% |
| PydanticBase      | 69.189% | 93.792% | 100%    | 100% |

[^set_note]:
	You can't really read or assign values to set members. Therefore, my code does the next best thing: calls `set.update()` to "set" values and just unpacks set contents as "read".

[^pyd_dataclass_note]:
	At the moment of testing, `pydantic` haven't implemented slots in it's version of dataclass *(at least for Python 3.7)*. In my tests I try define `PydanticDataClassSlots` as if slots support was there, and fall back to "simple" `PydanticDataClass` if it's not.
	
	So for now, `PydanticDataClassSlots` in my code is just another alias for `PydanticDataClass` which causes it to be tested twice. Here I show an averaged result.

## Conclusions

As expected, the truth is somewhere in between.

James Murphy was right that `pydantic` and in some cases `attrs` are expensive. With `pydantic` being ridiculously expensive (relative to others). However, I was right with my concerns, too. The distribution is nowhere near the results James shown. Especially for RAM, where the winner (regular class with slots) is only twice better than loser (`OrderedDict`). And if you exclude the types that are **supposed** to be memory-hungry by definition (`dict`, `set`), the gap shrinks even further.

Before continuing, there's very important thing to clarify: even though there's a clear performance difference in instance creation / attribute get/set time, *(almost)* all of them are basically nothing compared to the rest of your program running *(they're so small that it's even hard to reproduce **exactly** the same results for any test other than RAM)*.
Even in this, extremely simple test example, an overwhelming majority of time was spent to pre-generate the test data, not to perform the actual tests. So bear in mind that *(almost)* every test took seconds to process millions of instances, while **source data** for those instances took minutes to generate.

The only exception is `pydantinc`, which is orders of magnitude slower than the others, but even it took about as much time as was spent to data preparation. Which is quite simple here.

Let alone how much it would take if the same amount of data was processed in some way / parsed / scraped.

So to me, the only really important metric here is RAM consumption. With that said, though...

### Tuples

* There seems to be absolutely no reason to use regular tuples as containers: `NamedTuple` is both faster to access it's members and takes a bit less RAM.
* Regular tuples lose even to lists in every aspect other than RAM, but even there the difference is barely noticeable.

### Dicts / sets

* Using dicts as JSON-style data containers is clearly an anti-pattern for Python. If you still do it for anything other than "jump tables" (mappings), you should use `NamedTuple` / `@dataclass` instead.
* `OrderedDict` is **VERY** memory-hungry, 1.5x to a regular dict, which is quite heavy, on it's own. With latest efforts by Python devs in making core dicts to keep items ordered, we should move away from `OrderedDict`.
* `frozenset` provides virtually no benefits from performance standpoint.
* Sets in general are quite heavy and slow at everything but the only thing they're designed for: checking whether something is already in the set.

### `__slots__`

* I was surprised by **HOW MUCH** using slots increased performance in every aspect.
* Using `frozenset` or `set` for slots produced some contradicting results. In one case, a regular tuple-slots was better. In other one, it could be `set` or `frozenset`.
	
	My guess is that some of the tested types simply stopped me from implementing slots properly, therefore they didn't work at all, and the difference in results is a pure random *(the **approximate** results are reproducible though)*.

### `@dataclass`

* No surprise they do better than regular classes as data containers. If not memory footprint, they'd outperform even `NamedTuple`s.
* The only reason they leave a room for regular classes is `__slots__`, which are supported by dataclasses only since Python 3.10... And without native slots support, it's such a headache to add slots to a dataclass yourself, definitely not worth it. In my test, I did kinda dirty hack, inheriting and defining slots on a subclass. But it caused some issues (and it might affect results).
	
	So for production use, it's not an option until 3.10 becomes a widespread default, including google collab, support by ML libs, etc. Therefore...

### `attrs` and `pydantic`

* Slotted `@attr.s` class is in the leaders in every aspect other than initialisation. But keep in mind that these two container types had validators while others didn't. Pros and cons for `attrs` are explained well in aforementioned video (mCoding/James Murphy) but in general it's such a tempting default choice, outperforming even built-in dataclasses (not by much, though).
* `pydantic` is the worst in every measurable way... until you factor in it's sole reason for existence: serializing entire hierarchies from/to JSON. `attrs` seems to have some separate packages doing the same thing, but at a first glance workflow seems much more complicated (at least to me).
* If you stick to `pydantic` though, it's `@dataclass` implementation uses slightly more RAM (approx. +25%) than `BaseModel`. But it's also 30-40% faster in attribute setting/accessing. Ignoring the fact that `BaseModel` is more feature-rich.