#    Elli is a library for reading, modifying, and writing memory content
#    to and from intel hex files and raw binary files. It can also operate
#    on arbitrary memory slices that fit within a 4 GiB address space.
#
#    Copyright (C) 2024 Kolbjørn Austreng
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path
from enum import IntEnum
from typing import Dict, Iterator, List, Literal, NamedTuple, Optional, Tuple, Union
import warnings


class _HexRecordType(IntEnum):
    DATA = 0
    END_OF_FILE = 1
    EXTENDED_SEGMENT_ADDRESS = 2
    START_SEGMENT_ADDRESS = 3
    EXTENDED_LINEAR_ADDRESS = 4
    START_LINEAR_ADDRESS = 5

    def __str__(self):
        if self == _HexRecordType.DATA:
            return "Data"
        elif self == _HexRecordType.END_OF_FILE:
            return "End of file"
        elif self == _HexRecordType.EXTENDED_SEGMENT_ADDRESS:
            return "Extended segment address"
        elif self == _HexRecordType.START_SEGMENT_ADDRESS:
            return "Start segment address"
        elif self == _HexRecordType.EXTENDED_LINEAR_ADDRESS:
            return "Extended linear address"
        elif self == _HexRecordType.START_LINEAR_ADDRESS:
            return "Start linear address"
        else:
            raise RuntimeError("Invalid record type")


class _HexRecordInvalidType(Exception):
    def __init__(self, record_type: int):
        self.record_type = record_type


class _HexRecordChecksumMismatch(Exception):
    def __init__(self, given: int, calculated: int):
        self.given = given
        self.calculated = calculated


class _HexRecordWrongByteCount(Exception):
    def __init__(self, record_type: _HexRecordType, expected: int, actual: int):
        self.record_type = record_type
        self.expected = expected
        self.actual = actual


class _HexRecord:
    def __init__(
        self,
        byte_count: int,
        address: int,
        record_type: _HexRecordType,
        data: List[int],
    ):
        assert address < 2**16, ValueError(
            f"Address `{address:x}` does not fit within 16 bits."
            " Use `Extended linear address` records to address a"
            " larger memory space up to 4 GiB."
        )

        self._byte_count = byte_count
        self._address = address
        self._record_type = record_type
        self._data = data

    @classmethod
    def from_record(cls, record: str):
        # Intel hex allows for any number of symbols before the
        # start of record colon. Some old systems even mandate kt
        # least 25 NULL characters preceding the start of record
        start = record.find(":")

        byte_count = int(record[start + 1 : start + 3], 16)

        raw = [
            int(record[i : i + 2], 16)
            for i in range(start + 1, start + 11 + 2 * byte_count, 2)
        ]

        address = (raw[1] << 8) | raw[2]

        try:
            record_type = _HexRecordType(raw[3])
        except ValueError:
            raise _HexRecordInvalidType(raw[3])

        data = bytes(raw[4:-1])

        if record_type == _HexRecordType.EXTENDED_SEGMENT_ADDRESS and byte_count != 2:
            raise _HexRecordWrongByteCount(record_type, 2, byte_count)
        elif record_type == _HexRecordType.START_SEGMENT_ADDRESS and byte_count != 4:
            raise _HexRecordWrongByteCount(record_type, 4, byte_count)
        elif record_type == _HexRecordType.EXTENDED_LINEAR_ADDRESS and byte_count != 2:
            raise _HexRecordWrongByteCount(record_type, 4, byte_count)
        elif record_type == _HexRecordType.START_LINEAR_ADDRESS and byte_count != 4:
            raise _HexRecordWrongByteCount(record_type, 4, byte_count)

        checksum = raw[-1]
        calculated_checksum = ((sum(raw[:-1]) ^ 0xFF) + 1) & 0xFF

        if checksum != calculated_checksum:
            raise _HexRecordChecksumMismatch(checksum, calculated_checksum)

        return cls(byte_count, address, record_type, data)

    @classmethod
    def record_data(cls, address: int, data: bytes):
        return cls(len(data), address, _HexRecordType.DATA, data)

    @classmethod
    def record_eof(cls):
        return cls(0, 0, _HexRecordType.END_OF_FILE, bytes())

    @classmethod
    def record_ext_segment(cls, address: int):
        data = int.to_bytes(address, 2)
        return cls(2, 0, _HexRecordType.EXTENDED_SEGMENT_ADDRESS, data)

    @classmethod
    def record_start_segment(cls, cs: int, ip: int):
        data = int.to_bytes(cs, 2) + int.to_bytes(ip, 2)
        return cls(4, 0, _HexRecordType.START_SEGMENT_ADDRESS, data)

    @classmethod
    def record_ext_linear(cls, address: int):
        data = int.to_bytes(address, 2)
        return cls(2, 0, _HexRecordType.EXTENDED_LINEAR_ADDRESS, data)

    @classmethod
    def record_start_linear(cls, address: int):
        data = int.to_bytes(address, 4)
        return cls(4, 0, _HexRecordType.START_LINEAR_ADDRESS, data)

    @property
    def address(self) -> int:
        return self._address

    @property
    def data(self) -> bytes:
        return self._data

    @property
    def record_type(self) -> _HexRecordType:
        return self._record_type

    def __str__(self) -> str:
        raw = (
            int.to_bytes(self._byte_count, 1)
            + int.to_bytes(self._address, 2)
            + int.to_bytes(self._record_type, 1)
            + self._data
        )

        header = f"{self._byte_count:02X}{self._address:04X}{self._record_type:02X}"
        data = "".join([f"{byte:02X}" for byte in self._data])
        checksum = ((sum(raw) ^ 0xFF) + 1) & 0xFF

        return f":{header}{data}{checksum:02X}"


def _hex_records_from_file(hex_file: Path) -> Iterator[Tuple[int, _HexRecord]]:
    reached_eof = False

    for record_number, record in enumerate(hex_file.read_text().splitlines()):
        line_number = record_number + 1

        if reached_eof:
            warnings.warn(
                f"Hex file EOF record reached at line {line_number - 1}"
                f" of `{str(hex_file)}`, but the file does not end there."
                " Any following lines will be ignored."
            )
            return StopIteration

        try:
            record = _HexRecord.from_record(record)
            if record.record_type == _HexRecordType.END_OF_FILE:
                reached_eof = True
            yield record_number + 1, record

        except _HexRecordInvalidType as e:
            raise RuntimeError(
                f"Invalid record type `{e.record_type:02X}` on line {line_number}"
            )

        except _HexRecordChecksumMismatch as e:
            raise RuntimeError(
                f"Checksum mismatch on line {line_number}."
                f" Given `{e.given:02X}`, calculated `{e.calculated:02X}`"
            )

        except _HexRecordWrongByteCount as e:
            raise RuntimeError(
                f"Record of type `{e.record_type}` on line {line_number}"
                f" has {e.actual} data bytes, but should have {e.expected}"
            )


def _hex_data_records_from_dict(memory: Dict[int, int]) -> Iterator[Tuple[int, bytes]]:
    if len(memory) == 0:
        return StopIteration

    start = min(memory)
    last_address = start - 1
    length = 0

    for address in sorted(memory.keys()):
        # The maximum length could be much larger, but
        # some systems only support data fields of 16 bytes
        if length == 16 or address != last_address + 1:
            data = bytes([memory[start + offset] for offset in range(0, length)])
            yield start, data
            start = address
            length = 0

        last_address = address
        length += 1

    data = bytes([memory[start + offset] for offset in range(0, length)])
    yield start, data


class _HexTrackedMemory(NamedTuple):
    byte: int
    set_by_record_line: int


class Elli:
    """
    Elli is a byte wise representation of memory. Elli can be read from,
    and write to intel hex files, raw binary blobs, or python dictionaries.

    Elli can be used to tweak memory, merge files, convert between hex and
    binary files, verify memory consistencies, among other tasks.
    """

    def __init__(self, base: Optional[Union[str, Path, Dict[int, int], bytes]] = None):
        """
        Construct Elli from `base`, where base can be one of the following:
            * None: Elli with empty memory content.
            * str or Path: Path to an intel hex file.
            * Dict: Python dictionary mapping addresses (int) to bytes (int).
            * bytes: Raw binary data. The start address may be set after
              construction using the `start_address` property setter.
        """
        self._exec_start_address: Optional[int] = None
        self._start_segment_cs: Optional[int] = None
        self._start_segment_ip: Optional[int] = None
        self._memory: Dict[int, int] = {}

        if base is None:
            pass
        elif isinstance(base, Dict):
            self._init_from_dict(base)
        elif isinstance(base, bytes):
            self._init_from_bytes(base)
        elif isinstance(base, str):
            hex_file = Path(base).expanduser().absolute()
            self._init_from_path(hex_file)
        elif isinstance(base, Path):
            self._init_from_path(base)
        else:
            raise TypeError(
                f"Cannot construct {Elli.__name__} from object of"
                f" type `{type(base).__name__}`"
            )

    def _init_from_dict(self, base: Dict[int, int]):
        for address, byte in base.items():
            if not isinstance(address, int) or not isinstance(byte, int):
                raise TypeError(
                    f"When constructing {Elli.__name__} from dictionaries,"
                    " the dictionary must be a mapping from address to byte,"
                    " where both address and byte are integers."
                )

            if address < 0 or address >= 2**32:
                raise ValueError(
                    f"Address `0x{address:x}` is outside of the 4 GiB"
                    f" memory space supported by {Elli.__name__}."
                )

            if byte < 0 or byte >= 2**8:
                raise ValueError(
                    f"Value at address `0x{address:08x}` has to be"
                    f" between 0 and 255, inclusive. Got `{byte}`."
                )

        self._memory = base

    def _init_from_bytes(self, base: bytes):
        self._memory = {address: byte for address, byte in enumerate(base)}

    def _init_from_path(self, hex_file: Path):
        tracked_memory: Dict[int, _HexTrackedMemory] = {}
        base_address = 0

        for line, record in _hex_records_from_file(hex_file):
            if record.record_type == _HexRecordType.DATA:
                for offset, byte in enumerate(record.data):
                    address = base_address + record.address + offset

                    if address in tracked_memory:
                        first_set_line = tracked_memory[address].set_by_record_line

                        raise RuntimeError(
                            f"Byte at address `0x{address:08x}` is set twice."
                            f" First on line {first_set_line}, then on line {line}."
                        )

                    tracked_memory[address] = _HexTrackedMemory(
                        byte=byte, set_by_record_line=line
                    )

            elif record.record_type == _HexRecordType.EXTENDED_SEGMENT_ADDRESS:
                base_address = 16 * int.from_bytes(record.data)

            elif record.record_type == _HexRecordType.START_SEGMENT_ADDRESS:
                self._start_segment_cs = int.from_bytes(record.data[0:2])
                self._start_segment_ip = int.from_bytes(record.data[2:4])

            elif record.record_type == _HexRecordType.EXTENDED_LINEAR_ADDRESS:
                base_address = int.from_bytes(record.data) << 16

            elif record.record_type == _HexRecordType.START_LINEAR_ADDRESS:
                self._exec_start_address = int.from_bytes(record.data)

        self._memory = {
            address: tracked_byte.byte
            for address, tracked_byte in tracked_memory.items()
        }

    def _hex_records(self) -> Iterator[_HexRecord]:
        base = 0

        for address, data in _hex_data_records_from_dict(self._memory):
            if address - base > 0xFFFF:
                base = address & 0xFFFF0000
                yield _HexRecord.record_ext_linear(base >> 16)

            yield _HexRecord.record_data(address & 0xFFFF, data)

        if self._start_segment_cs is not None:
            yield _HexRecord.record_start_segment(
                self._start_segment_cs, self._start_segment_ip
            )

        if self._exec_start_address is not None:
            yield _HexRecord.record_start_linear(self._exec_start_address)

        yield _HexRecord.record_eof()

    def _min(self) -> int:
        return 0 if len(self._memory) == 0 else min(self._memory)

    def _max(self) -> int:
        return 0 if len(self._memory) == 0 else max(self._memory)

    def __contains__(self, address: int) -> bool:
        """
        Check whether an address is contained in the memory view or not.
        """
        return address in self._memory

    def __eq__(self, other: Elli) -> bool:
        """
        Check whether two Ellis have the same memory content, along
        with `Start segment address` and `Start linear address` values.
        """
        return (
            self._exec_start_address == other._exec_start_address
            and self._start_segment_cs == other._start_segment_cs
            and self._start_segment_ip == other._start_segment_ip
            and self._memory == other._memory
        )

    def __getitem__(self, address: int) -> int:
        """
        Get the byte at `address`, failing if the `address` is not in the memory view.
        """
        return self._memory[address]

    def __setitem__(self, address: int, value: int):
        """
        Set the byte at `address` to `value`.
        The `address` must be containable in a 4 GiB address space,
        and `value` must be representable as an unsigned 8 bit integer.
        """
        assert 0 <= address < 2**32, ValueError(
            f"{Elli.__name__} only supports 4 GiB memory spaces;"
            f" address `{address:x}` lies outside of this."
        )

        assert 0 <= value < 2**8, ValueError(
            f"Value `{value} ({value:x})` does not fit within a byte."
            " Perhaps you wanted to use `.set_word` instead?"
        )

        self._memory[address] = value

    @property
    def start_address(self) -> int:
        """
        Retrieve the start address of the memory slice represented by Elli.
        """
        return self._min()

    @start_address.setter
    def start_address(self, new_start: int):
        """
        Set the start address of the memory slice to `new_start`,
        while simultaneously shifting all bytes to account for the new start.
        """
        shift = new_start - self._min()

        assert new_start >= 0 and self._max() + shift < 2**32, ValueError(
            f"Setting a start address of `{new_start:x}` will shift the"
            " contained memory out of its 4 GiB address space."
        )

        self._memory = {address + shift: byte for address, byte in self._memory.items()}

    @property
    def span(self) -> Tuple[int, int]:
        """
        Retrieve the lower and upper bounds of the memory spanned by Elli,
        returned as a tuple of the lowest and highest address in the memory slice.
        """
        return self._min(), self._max()

    @property
    def hex_start_segment_address(self) -> Optional[Tuple[int, int]]:
        """
        Get the intel hex `Start segment address` CS and IP values, if any.
        These are the two `code segment` (CS) and `instruction pointer` (IP)
        values contained in intel hex records of type `0x03`.

        If the values are set, they are returned as a tuple of `(CS, IP)`.
        Otherwise, `None` is returned.

        The `Start segment address` is typically only relevant for 80x86
        processors, and can be safely ignored if you are not operating on
        an intel hex file for this architecture.
        """
        if self._start_segment_cs is None:
            return None
        return self._start_segment_cs, self._start_segment_ip

    @hex_start_segment_address.setter
    def hex_start_segment_address(self, cs_ip: Optional[Tuple[int, int]]):
        """
        Set the intel hex `Start segment address` CS and IP values.
        These are the two `code segment` (CS) and `instruction pointer` (IP)
        values contained in intel hex records of type `0x03`.

        The values are set with a tuple on the form `(CS, IP)`.
        Alternatively, a single `None` may be submitted to purge these
        values from the memory slice.

        The `Start segment address` is typically only relevant for 80x86
        processors, and can be safely ignored if you are not operating on
        an intel hex file for this architecture.
        """
        if cs_ip is None:
            self._start_segment_cs = None
            self._start_segment_ip = None
            return

        try:
            cs, ip = cs_ip

            assert isinstance(cs, int)
            assert isinstance(ip, int)
        except (ValueError, AssertionError):
            raise TypeError(
                f"Cannot set `start segment address` with `{cs_ip}`."
                " Provide a tuple of the CS and IP as integers."
            )

        for v, name in [(cs, "CS"), (ip, "IP")]:
            assert 0 <= v < 2**16, ValueError(
                f"Cannot set `Start segment address` {name} to `0x{v:x}`."
                f" {name} must be representable as a 16 bit integer."
            )

        self._start_segment_cs = cs
        self._start_segment_ip = ip

    @property
    def hex_start_linear_address(self) -> Optional[int]:
        """
        Get the `Start linear address` of the memory, if any.
        For processors that support it, this sets the `start execution address`
        encoded in intel hex records of type `0x05`.

        The `Start linear address` is typically only relevant for files compiled
        with Arm Keil-MDK, and can be safely ignored if you are not operating on
        such files.
        """
        return self._exec_start_address

    @hex_start_linear_address.setter
    def hex_start_linear_address(self, address: Optional[int]):
        """
        Set the `Start linear address` of the memory.
        For processors that support it, this sets the `start execution address`
        encoded in intel hex records of type `0x05`.

        Alternatively, a `None` may be supplied to this setter to purge this
        value from the memory slice.

        The `Start linear address` is typically only relevant for files compiled
        with Arm Keil-MDK, and can be safely ignored if you are not operating on
        such files.
        """
        if address is not None:
            assert isinstance(address, int), TypeError(
                f"Cannot set `start linear address` with `{type(address).__name__}`."
                " Address must be an integer or `None`."
            )

            assert 0 <= address < 2**32, ValueError(
                f"Cannot set `start linear address` to `0x{address:x}`."
                " Address must be representable by a 32 bit integer."
            )

        self._exec_start_address = address

    def get_word(self, address: int, fill: int = 0xFF) -> int:
        """
        Get a 4-byte word from `address`, assuming a fill value of `fill`
        for bytes that are not set in the range of `(address, address + 4)`.

        The underlying memory is always treated as big endian, as per
        the intel hex specification.

        This function enforces no alignment requirements.
        Any such restrictions are left up to the caller.
        """
        return int.from_bytes(
            [
                self._memory.get(byte_address, fill)
                for byte_address in range(address, address + 4)
            ],
            byteorder="big",
        )

    def set_word(self, address: int, value: int):
        """
        Set a 4-byte word at `address` to `value`.

        The underlying memory and `value` is always treated as big endian, as per
        the intel hex specification.

        This function enforces no alignment requirements.
        Any such restrictions are left up to the caller.
        """
        for offset, byte in enumerate(int.to_bytes(value, length=4, byteorder="big")):
            self._memory[address + offset] = byte

    def merge(self, other: Elli, allow_overwrites: bool = False) -> Elli:
        """
        Merge an Elli `other` with the current Elli, producing a new Elli with
        merged memory content from both instances. Neither of the original Ellis
        are modified by this.

        If either of the Ellis set the same memory content, or have different
        `Start segment address` or `Start linear address` values set, a `ValueError`
        is raised to signal the collision.

        Alternatively, `allow_overwrites` may be set true, in which case values
        from `other` will override any conflicts with the current Elli. Still,
        neither of the two input instances are modified by this.
        """
        merged = self._memory

        for address, byte in other._memory.items():
            if address in merged and not allow_overwrites:
                raise ValueError(
                    f"Byte at address `0x{address:08x}` is already set in memory,"
                    " and would be overwritten by merging. To allow this,"
                    f" call `{self.merge.__name__}` with `allow_overwrites = True`."
                )
            merged[address] = byte

        if allow_overwrites:
            exec_start = other._exec_start_address or self._exec_start_address
            cs = other._start_segment_cs or self._start_segment_cs
            ip = other._start_segment_ip or self._start_segment_ip
        else:

            def pick_address_or_raise(
                one: Optional[int], two: Optional[int], description: str
            ) -> Optional[int]:
                if one is not None and two is not None and one != two:
                    raise ValueError(
                        f"{description} would be overwritten by merging."
                        f" To allow this, call `{self.merge.__name__}` with"
                        " `allow_overwrites = True`."
                    )

                return one or two

            exec_start = pick_address_or_raise(
                self._exec_start_address,
                other._exec_start_address,
                "Start linear address (execution start address)",
            )

            cs = pick_address_or_raise(
                self._start_segment_cs,
                other._start_segment_cs,
                "Start segment address (CS)",
            )

            ip = pick_address_or_raise(
                self._start_segment_ip,
                other._start_segment_ip,
                "Start segment address (IP)",
            )

        new = Elli()

        new._exec_start_address = exec_start
        new._start_segment_cs = cs
        new._start_segment_ip = ip
        new._memory = merged

        return new

    def range(self, start: int, end: int) -> Elli:
        """
        Retrieve a sub-Elli, having the same memory as the current Elli,
        but only ranging between `start` and `end`, inclusively.

        Potential `Start segment address` and `Start linear address` values
        are not transferred into the new Elli, and must be manually copied
        if these are of relevance.
        """
        region = Elli()

        region._memory = {
            address: byte
            for address, byte in self._memory.items()
            if address in range(start, end + 1)
        }

        return region

    def to_dict(self) -> Dict[int, int]:
        """
        Return the underlying memory view of the Elli as a dictionary,
        mapping addresses to bytes.
        """
        return self._memory

    def to_hex(self) -> str:
        """
        Encode the Elli in intel hex format, returning this as a string.
        """
        return "\n".join(str(record) for record in self._hex_records()) + "\n"

    def to_bin(self, fill: int = 0xFF) -> bytes:
        """
        Get the raw byte representation of the Elli, using `fill` as the default
        value for any empty addresses inside the span of the Elli.
        """
        start = self._min()
        end = self._max()
        size = end - start + 1

        binary = [fill] * size

        for address, byte in self._memory.items():
            binary[address - start] = byte

        return bytes(binary)

    def write(
        self, path: Union[str, Path], file_type: Literal["hex", "bin"], fill: int = 0xFF
    ):
        """
        Convenience method for directly writing the Elli to a file given by `path`.
        The file type is determined by `file_type`, and can be either `"hex"` or
        `"bin"`, for intel hex files or raw binary files, respectively.

        For binary files, `fill` is used as the default byte value for empty addresses
        in the span of the Elli. For intel hex files, `fill` is not used.
        """
        if isinstance(path, str):
            path = Path(path).expanduser().absolute()

        if file_type == "hex":
            path.write_text(self.to_hex())
        elif file_type == "bin":
            path.write_bytes(self.to_bin(fill))
