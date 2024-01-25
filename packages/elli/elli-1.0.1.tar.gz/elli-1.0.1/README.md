# Elli

Elli is a python library for reading, manipulating, merging, and writing intel hex files, raw binary files, or operating on memory slices in general.

## Common use cases at a glance

The most common use cases for Elli are reading, merging, and writing hex files,
as well as converting binary files to hex files or vice versa.

```python
from elli import Elli
from pathlib import Path

# Merge hex files
file_one = Elli("/path/to/one.hex")
file_two = Elli("/path/to/two.hex")

merged = file_one.merge(file_two, allow_overwrites=False)

output = Path("/path/to/merged/output.hex")
merged.write(output, "hex")

# Convert a binary file to a hex file
bin_file = Path("/path/to/file.bin")
hex_file = Path("/path/to/file.hex")

el = Elli(bin_file.read_bytes())
el.write(hex_file, "hex")
```

## In depth usage

The class `Elli` is the main workhorse of this package.
To get started, you'll want something along the lines of

```python
from elli import Elli
```

### Construction

To construct an object of the class Elli, you have a few options:

```python
# Read and parse an intel hex file
el = Elli("/path/to/file.hex")

# The same, but using `Path` from the standard library `pathlib`
from pathlib import Path
hex_file = Path("/path/to/file.hex")
el = Elli(hex_file)

# Construct from a python dictionary representing the relevant memory
el = Elli({0: 190, 1: 241, 2: 140, 3: 213})

# Construct from raw bytes. This assumes a start address of 0
el = Elli(bytes([1, 2, 3, 4]))
```

### Basic memory manipulation

Memory in the Elli can be set byte-wise, or word-wise (a word being 4 bytes):

```python
# Get and set individual bytes
byte = el[0xae1f3256]
el[0xae1f3256] = byte - 15

# Get and set whole words without alignment requirements
word = el.get_word(0xae1f3256)
el.set_word(0xae1f3256, 0)
```

### Query memory slice information

Information about the contents of Ellis are available with built in operators.

```python
# Check whether an address is present in an Elli
el = Elli({1: 1, 2: 2})
address = 1

address in el # True

address = 3
address in el # False

# Check whether two Ellis have the same memory content
other = Elli({1: 1, 2: 2})

el == other # True

other[3] = 3
el == other # False

# Get the span of an Elli. The span being lower and upper bounds in
# the address space of an Elli
span_el = el.span # (1, 2)
span_other = other.span # (1, 3)

# Get and set start addresses of Ellis
start = el.start_address # 1

# Setting the start address shifts all memory along with the new start address
el.start_address = 3 # {1: 1, 2: 2} -> {3: 1, 4: 2}
```

### Merge and obtain sub-ranges of Ellis

Elli can merge and split memory content.

```python
one = Elli("/path/to/file_one.hex")
two = Elli("/path/to/file_two.hex")

# Merge `one` and `two` into a new Elli, raising a `ValueError` on collisions
three = one.merge(two)

# To overwrite collisions, taking values from `two`
three = one.merge(two, allow_overwrites=True)

# Create an Elli with a subset of the memory of `three`, from address
# `start_address`, up to and including address `end_address`
start_address = 0x2567
end_address = 0x31ab
four = three.range(start_address, end_address)
```

### Intel hex related operations

Elli can get and set intel hex specific memory information.

```python
# Get and set the `Start segment address` of an Elli
cs, ip = el.hex_start_segment_address
el.hex_start_segment_address = new_cs, new_ip

# Or clear such information from the Elli
el.hex_start_segment_address = None

# Get and set the `Start linear address` of an Elli
exec_start = el.hex_start_linear_addrss
el.hex_start_linear_address = new_exec_start

# Or clear such information from the Elli
el.hex_start_linear_address = None
```

### Export an Elli to different formats

Ellis can be exported as intel hex, python dictionaries, or raw bytes.

```python
# Get a string representation of an intel hex file
hex_string = el.to_hex()

# Get a binary blob representing all the bytes of the Elli,
# with `fill` used for addresses that are not set
byte_string = el.to_bin(fill=0xFF)

# Get a python dictionary of the underlying memory,
# mapping addresses to bytes
mapping = el.to_dict()
```

### Write Ellis to files

An Elli can be directly written to a file as either an intel hex file, or a raw binary file.

```python
# Write an intel hex file
el.write("/path/to/file.hex", "hex")

# Write a raw binary file, setting unspecified byte values to `0xFF`
el.write("/path/to/file.bin", "bin", fill=0xFF)
```

## Contribution guidelines

Elli should remain a slim and lightweight piece of software.
As such, the python standard library should be used over third party packages as far as possible.

Elli's code is formatted with [black](https://pypi.org/project/black/).

Elli's code should run error free through `pylint`, `pyflakes`, `mypy`, and `pycodestyle`.
The following `pycodestyle` options can be disabled:
* E203: whitespace before ":"
* E402: module level import not at top of file
