# =============================================================================
# Casanova Utils
# =============================================================================
#
# Miscellaneous utility functions.
#
from typing import Iterator, Iterable, Mapping, TypeVar, Generic, Optional, cast

import re
import csv
import gzip
import importlib
import os
import sys
from os import PathLike, SEEK_END
from os.path import splitext, abspath, relpath, dirname
from io import StringIO, DEFAULT_BUFFER_SIZE
from platform import python_version_tuple

from casanova.exceptions import Py310NullByteWriteError, LtPy311ByteReadError

PY_310 = python_version_tuple()[:2] == ("3", "10")
LT_PY311 = python_version_tuple()[:2] <= ("3", "10")


def py310_wrap_csv_writerow(writer):
    if not PY_310:
        return writer.writerow

    def wrapped(*args, **kwargs):
        try:
            writer.writerow(*args, **kwargs)
        except csv.Error as e:
            if str(e).lower() == "need to escape, but no escapechar set":
                raise Py310NullByteWriteError(
                    "Cannot write row containing null byte. This error only happens on python 3.10 (see https://github.com/python/cpython/issues/56387). Consider using the strip_null_bytes_on_write=True kwarg or change python version."
                )

            raise

    return wrapped


def ltpy311_csv_reader(input_file, **kwargs):
    reader = csv.reader(input_file, **kwargs)

    if not LT_PY311:
        return reader

    def wrapped():
        try:
            for item in reader:
                yield item
        except csv.Error as e:
            if "line contains nul" in str(e).lower():
                raise LtPy311ByteReadError(
                    "python < 3.11 cannot read CSV files containing null bytes. Consider using the strip_null_bytes_on_read=True kwarg or upgrade your python version."
                )

            raise

    return wrapped()


def ensure_open(p, mode="r", encoding="utf-8", newline=None):
    if not isinstance(p, (str, PathLike)):
        return p

    p = str(p)

    if p.endswith(".gz"):
        if "b" in mode:
            return gzip.open(p, mode=mode, newline=newline)

        mode += "t"
        return gzip.open(p, encoding=encoding, mode=mode, newline=newline)

    if "b" in mode:
        return open(p, mode=mode, newline=newline)

    return open(p, encoding=encoding, mode=mode, newline=newline)


def parse_module_and_target(path, default: str = "main"):
    if ":" in path:
        s = path.rsplit(":", 1)
        return s[0], s[1]

    return path, default


def import_target(path: str, default: str = "main"):
    module_path_or_name, function_name = parse_module_and_target(path, default=default)

    # NOTE: we normalize to a path, so we can add dir to sys.path
    if not module_path_or_name.endswith(".py"):
        module_path_or_name = module_path_or_name.replace(".", os.sep) + ".py"

    module_path = abspath(module_path_or_name)
    module_directory = dirname(module_path)

    if module_directory not in sys.path:
        sys.path.append(module_directory)

    # NOTE: we renormalize to a module
    module = relpath(module_path)[:-3].replace(os.sep, ".")

    m = importlib.import_module(module)

    sys.path.remove(module_directory)

    try:
        return getattr(m, function_name)
    except AttributeError:
        raise ImportError


def infer_delimiter_or_type(file_or_path):
    if isinstance(file_or_path, PathLike):
        file_or_path = str(file_or_path)

    if hasattr(file_or_path, "name"):
        file_or_path = file_or_path.name

    if isinstance(file_or_path, str):
        rest, ext = splitext(file_or_path)

        if ext == ".gz":
            _, ext = splitext(rest)

        if ext == ".tsv" or ext == ".tab":
            return ("csv", "\t")

        if ext == ".ndjson" or ext == ".jsonl":
            return ("ndjson", None)

    return ("csv", None)


BOM_RE = re.compile(r"^\ufeff")


def suppress_BOM(string):
    return re.sub(BOM_RE, "", string)


def has_null_byte(string):
    return "\0" in string


def strip_null_bytes(string):
    return string.replace("\0", "")


def lines_without_null_bytes(iterable):
    for line in iterable:
        yield strip_null_bytes(line)


def first_cell_index_with_null_byte(row):
    for i, cell in enumerate(row):
        if has_null_byte(cell):
            return i

    return None


def strip_null_bytes_from_row(row):
    if any(has_null_byte(cell) for cell in row if isinstance(cell, str)):
        return [
            strip_null_bytes(cell) if isinstance(cell, str) else cell for cell in row
        ]

    return row


def rows_without_null_bytes(iterable):
    for row in iterable:
        yield strip_null_bytes_from_row(row)


def looks_like_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def size_of_row_in_memory(row):
    """
    Returns the approximate amount of bytes needed to represent the given row into
    the python's program memory.

    The magic numbers are based on `sys.getsizeof`.
    """
    a = 64 + 8 * len(row)  # Size of the array
    a += sum(49 + len(cell) for cell in row)  # Size of the contained strings

    return a


def size_of_row_in_file(row):
    """
    Returns the approximate amount of bytes originally used to represent the
    given row in its CSV file. It assumes the delimiter uses only one byte.

    I also ignores quotes (-2 bytes) around escaped cells if they were
    originally present.

    I also don't think that it counts 16 bit chars correctly.
    """
    a = max(0, len(row) - 1)
    a += sum(len(cell) for cell in row)

    return a


def flatmap(item):
    if not isinstance(item, Iterable) or isinstance(item, (str, bytes)):
        yield item
    else:
        for sub_item in item:
            yield from flatmap(sub_item)


class CsvIOBase(StringIO):
    def __init__(self):
        super().__init__()
        self.writer = csv.writer(
            self, dialect=csv.unix_dialect, quoting=csv.QUOTE_MINIMAL
        )


class CsvCellIO(CsvIOBase):
    def __init__(self, value, column=None):
        super().__init__()

        if column is not None:
            self.fieldnames = [column]
            self.writer.writerow(self.fieldnames)

        self.writer.writerow([value])

        self.seek(0)


class CsvRowIO(CsvIOBase):
    def __init__(self, row, fieldnames=None):
        super().__init__()

        self.fieldnames = fieldnames

        if isinstance(row, Mapping):
            if self.fieldnames is None:
                self.fieldnames = list(row.keys())

            row = [row.get(f) for f in self.fieldnames]

        if self.fieldnames is not None:
            self.writer.writerow(self.fieldnames)

        self.writer.writerow(row)

        self.seek(0)


class CsvIO(CsvIOBase):
    def __init__(self, rows, fieldnames=None):
        super().__init__()

        self.fieldnames = fieldnames

        if fieldnames is not None:
            self.writer.writerow(fieldnames)

        for row in rows:
            self.writer.writerow(row)

        self.seek(0)


class ReversedFile:
    def __init__(self, f, offset: int = 0, buffer_size: int = DEFAULT_BUFFER_SIZE):
        self.f = f

        self.f.seek(0, SEEK_END)
        size = self.f.tell()

        self.cursor = size
        self.offset = offset
        self.buffer_size = buffer_size

    def read(self, size=-1):
        if size < 0:
            raise NotImplementedError

        assert self.cursor >= self.offset

        # Already finished
        if self.cursor == self.offset:
            return ""

        if self.cursor - size < self.offset:
            size = self.cursor - self.offset

        self.cursor -= size
        self.f.seek(self.cursor)
        data = self.f.read(size)

        return data[::-1]

    def __iter__(self):
        buffer = ""
        first = True

        while True:
            try:
                # NOTE: we could start searching from last buffer size
                # for better performance but who has time for that?
                i = buffer.index("\n")
            except ValueError:
                data = self.read(self.buffer_size)

                if not data:
                    break

                buffer += data

                continue

            part = buffer[: i + 1]
            buffer = buffer[i + 1 :]

            if first and part == "\n":
                first = False
                continue

            yield part

        if buffer:
            yield buffer


T = TypeVar("T")


# TODO: transfer this to `ebbe`
class PeekableIterator(Generic[T]):
    iterator: Iterator[T]
    finished: bool
    consumed: bool
    current: Optional[T]

    def __init__(self, iterable: Iterable[T]):
        self.iterator = iter(iterable)
        self.finished = False
        self.consumed = False
        self.current = None

        try:
            self.current = next(self.iterator)
        except StopIteration:
            self.consumed = True
            self.finished = True

    def peek(self) -> Optional[T]:
        return self.current

    def __next__(self) -> T:
        if self.consumed:
            raise StopIteration

        # NOTE:
        current = cast(T, self.current)

        if self.finished:
            self.consumed = True
            return current

        try:
            self.current = next(self.iterator)
        except StopIteration:
            self.finished = True
            self.current = None

        return current
