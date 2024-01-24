# =============================================================================
# Casanova Enricher
# =============================================================================
#
# A CSV reader/writer combo that can be used to read an input CSV file and
# easily ouput a similar CSV file while editing, adding and filtering cell_count.
#
from typing import Optional, Iterable, Union
from casanova.types import AnyWritableCSVRowPart, AnyCSVDialect

from ebbe import with_is_last

from casanova.resumers import (
    LastCellComparisonResumer,
    Resumer,
    RowCountResumer,
    IndexedResumer,
    BatchResumer,
)
from casanova.headers import Headers
from casanova.reader import Reader
from casanova.writer import Writer, InferringWriter
from casanova.record import coerce_row, coerce_fieldnames, AnyFieldnames
from casanova.defaults import DEFAULTS
from casanova.serialization import CustomTypes


class Enricher(Reader):
    __supported_resumers__ = (RowCountResumer, LastCellComparisonResumer)

    def __init__(
        self,
        input_file,
        output_file,
        no_headers: bool = False,
        select: Optional[Union[str, Iterable[str]]] = None,
        add: Optional[AnyFieldnames] = None,
        strip_null_bytes_on_write: Optional[bool] = None,
        writer_dialect: Optional[AnyCSVDialect] = None,
        writer_delimiter: Optional[str] = None,
        writer_quotechar: Optional[str] = None,
        writer_escapechar: Optional[str] = None,
        writer_quoting: Optional[int] = None,
        writer_lineterminator: Optional[str] = None,
        write_header: bool = True,
        **kwargs
    ):
        # Inheritance
        super().__init__(input_file, no_headers=no_headers, **kwargs)

        if strip_null_bytes_on_write is None:
            strip_null_bytes_on_write = DEFAULTS.strip_null_bytes_on_write

        if not isinstance(strip_null_bytes_on_write, bool):
            raise TypeError('expecting a boolean as "strip_null_bytes_on_write" kwarg')

        self.strip_null_bytes_on_write = strip_null_bytes_on_write

        self.selected_indices = None
        self.output_fieldnames = (
            list(self.fieldnames) if self.fieldnames is not None else None
        )
        self.added_count = 0

        if select is not None:
            if no_headers:
                self.selected_indices = Headers.select_no_headers(self.row_len, select)
            else:
                self.selected_indices = self.headers.select(select)
                self.output_fieldnames = self.__filterrow(self.output_fieldnames)

        add = coerce_fieldnames(add)

        if add is not None:
            if no_headers:
                if not isinstance(add, int):
                    raise TypeError(
                        "cannot add named columns with no_headers=True. Use a number of columns instead."
                    )

                self.added_count = add
            else:
                self.output_fieldnames += add
                self.added_count = len(add)

        self.output_headers = None

        # NOTE: not forwarding writer headers to avoid resumer issues (ref. #123)
        if self.output_fieldnames is not None:
            self.output_headers = Headers(self.output_fieldnames)

        self.padding = [""] * self.added_count

        # Resuming?
        self.resumer = None
        self.resuming = False

        if isinstance(output_file, Resumer):
            if not isinstance(output_file, self.__class__.__supported_resumers__):
                raise TypeError(
                    "%s: does not support %s!"
                    % (self.__class__.__name__, output_file.__class__.__name__)
                )

            self.resumer = output_file

            self.resuming = self.resumer.can_resume()

            if self.resuming:
                # NOTE: how about null bytes
                self.resumer.get_insights_from_output(
                    self,
                    no_headers=no_headers,
                    dialect=writer_dialect,
                    quotechar=writer_quotechar,
                    delimiter=writer_delimiter,
                )

                if hasattr(self.resumer, "resume"):
                    self.resumer.resume(self)

            output_file = self.resumer.open_output_file()

            if hasattr(self.resumer, "filter"):
                self.row_filter = self.resumer.filter_row

        # Instantiating writer
        self.writer = Writer(
            output_file,
            fieldnames=self.output_fieldnames,
            strip_null_bytes_on_write=strip_null_bytes_on_write,
            dialect=writer_dialect,
            delimiter=writer_delimiter,
            quotechar=writer_quotechar,
            escapechar=writer_escapechar,
            quoting=writer_quoting,
            lineterminator=writer_lineterminator,
            write_header=not self.resuming and write_header,
            strict=False,  # NOTE: not strict because we already check row length
        )

    def __repr__(self):
        return "<%s>" % self.__class__.__name__

    @property
    def should_write_header(self):
        return self.writer.should_write_header

    def __filterrow(self, row):
        row = coerce_row(row)

        if self.selected_indices is not None:
            row = [row[i] for i in self.selected_indices]

        return row

    def __formatrow(self, row, add=None, *addenda):
        # We expect additions
        if self.added_count > 0:
            if add is None:
                add = self.padding
            else:
                add = coerce_row(add, consume=True)

                for addition in addenda:
                    addition = coerce_row(addition)
                    add.extend(addition)

                if len(add) != self.added_count:
                    raise TypeError(
                        "casanova.enricher.writerow: expected %i additional cells but got %i."
                        % (self.added_count, len(add))
                    )

            formatted_row = self.__filterrow(row) + add

        # We don't expect additions
        else:
            if add is not None:
                raise TypeError("casanova.enricher.writerow: expected no additions.")

            formatted_row = self.__filterrow(row)

        return formatted_row

    def writeheader(self) -> None:
        self.writer.writeheader()

    def writerow(
        self,
        row: AnyWritableCSVRowPart,
        add: Optional[AnyWritableCSVRowPart] = None,
        *addenda: AnyWritableCSVRowPart
    ) -> None:
        self.writer._writerow(self.__formatrow(row, add, *addenda))

    def writebatch(
        self, row: AnyWritableCSVRowPart, addenda: Iterable[AnyWritableCSVRowPart]
    ):
        row = self.__filterrow(row)

        for addendum in addenda:
            addendum = coerce_row(addendum)

            if len(addendum) != self.added_count:
                raise TypeError(
                    "casanova.enricher.writebatch: expected %i additional cells but got %i."
                    % (self.added_count, len(addendum))
                )

            self.writer._writerow(row + addendum)


class IndexedEnricher(Enricher):
    __supported_resumers__ = (IndexedResumer,)

    def __init__(
        self, input_file, output_file, add=None, index_column="index", **kwargs
    ):
        self.index_column = index_column

        # Prepending index column to output
        add = [index_column] + list(coerce_fieldnames(add or []))

        # Inheritance
        super().__init__(input_file, output_file, add=add, **kwargs)

    def __iter__(self):
        return self.enumerate()

    def cells(self, column, with_rows=False):
        return self.enumerate_cells(column, with_rows=with_rows)

    def records(self, *shape, with_rows=False):
        return self.enumerate_records(*shape, with_rows=with_rows)

    def writerow(
        self,
        index: int,
        row: AnyWritableCSVRowPart,
        add: Optional[AnyWritableCSVRowPart] = None,
        *addenda: AnyWritableCSVRowPart
    ):
        if add is None:
            super().writerow(row, [index] + self.padding[:-1])
        else:
            super().writerow(row, [index], add, *addenda)


class BatchEnricher(Enricher):
    __supported_resumers__ = (BatchResumer,)

    def __init__(
        self,
        input_file,
        output_file,
        add=None,
        cursor_column="cursor",
        end_symbol="end",
        **kwargs
    ):
        self.cursor_column = cursor_column
        self.end_symbol = end_symbol

        # Prepending cursor column to output
        add = [cursor_column] + list(coerce_fieldnames(add or []))

        # Inheritance
        super().__init__(input_file, output_file, add=add, **kwargs)

    def writebatch(
        self,
        row: AnyWritableCSVRowPart,
        addenda: Iterable[AnyWritableCSVRowPart],
        cursor: Optional[str] = None,
    ):
        if cursor is None:
            cursor = self.end_symbol

        for is_last, addendum in with_is_last(addenda):
            self.writerow(row, [cursor if is_last else None], addendum)


class InferringEnricher(Reader):
    __supported_resumers__ = (RowCountResumer, LastCellComparisonResumer)

    def __init__(
        self,
        input_file,
        output_file,
        select: Optional[Union[str, Iterable[str]]] = None,
        strip_null_bytes_on_write: Optional[bool] = None,
        writer_dialect: Optional[AnyCSVDialect] = None,
        writer_delimiter: Optional[str] = None,
        writer_quotechar: Optional[str] = None,
        writer_escapechar: Optional[str] = None,
        writer_quoting: Optional[int] = None,
        writer_lineterminator: Optional[str] = None,
        plural_separator: Optional[str] = None,
        none_value: Optional[str] = None,
        true_value: Optional[str] = None,
        false_value: Optional[str] = None,
        stringify_everything: Optional[bool] = None,
        custom_types: Optional[CustomTypes] = None,
        buffer_optionals: bool = False,
        mapping_sample_size: Optional[int] = None,
        **kwargs
    ):
        # Inheritance
        super().__init__(input_file, **kwargs)

        if strip_null_bytes_on_write is None:
            strip_null_bytes_on_write = DEFAULTS.strip_null_bytes_on_write

        if not isinstance(strip_null_bytes_on_write, bool):
            raise TypeError('expecting a boolean as "strip_null_bytes_on_write" kwarg')

        self.strip_null_bytes_on_write = strip_null_bytes_on_write

        assert self.fieldnames is not None
        assert self.headers is not None

        self.selected_indices = None

        if select is not None:
            self.selected_indices = self.headers.select(select)
            prepend = [self.fieldnames[i] for i in self.selected_indices]
        else:
            prepend = list(self.fieldnames)

        # Resuming?
        self.resumer = None
        self.resuming = False

        if isinstance(output_file, Resumer):
            if not isinstance(output_file, self.__class__.__supported_resumers__):
                raise TypeError(
                    "%s: does not support %s!"
                    % (self.__class__.__name__, output_file.__class__.__name__)
                )

            self.resumer = output_file

            self.resuming = self.resumer.can_resume()

            if self.resuming:
                # NOTE: how about null bytes
                self.resumer.get_insights_from_output(
                    self,
                    dialect=writer_dialect,
                    quotechar=writer_quotechar,
                    delimiter=writer_delimiter,
                )

                if hasattr(self.resumer, "resume"):
                    self.resumer.resume(self)

            output_file = self.resumer.open_output_file()

            if hasattr(self.resumer, "filter"):
                self.row_filter = self.resumer.filter_row

        # Instantiating writer
        self.writer = InferringWriter(
            output_file,
            prepend=prepend,
            strip_null_bytes_on_write=strip_null_bytes_on_write,
            dialect=writer_dialect,
            delimiter=writer_delimiter,
            quotechar=writer_quotechar,
            escapechar=writer_escapechar,
            quoting=writer_quoting,
            lineterminator=writer_lineterminator,
            plural_separator=plural_separator,
            none_value=none_value,
            true_value=true_value,
            false_value=false_value,
            stringify_everything=stringify_everything,
            custom_types=custom_types,
            buffer_optionals=buffer_optionals,
            mapping_sample_size=mapping_sample_size,
        )

    def writerow(self, row: AnyWritableCSVRowPart, data) -> None:
        row = coerce_row(row)

        if self.selected_indices is not None:
            row = [row[i] for i in self.selected_indices]

        self.writer.writerow(row, data)
