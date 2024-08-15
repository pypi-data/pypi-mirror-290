from functools import lru_cache
from typing import (
    Callable,
    ClassVar,
    Hashable,
    Sequence,
    Union,
    final,
    overload,
)

from bs4 import BeautifulSoup, NavigableString, ResultSet, Tag


class CellBase[L: str, Value]:
    def __init__(self, cell_tag: Tag, label: str) -> None:
        self.tag = cell_tag
        self.label = self.parse_label(label)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.value)})"

    def parse_label(self, label: str) -> L:
        return label  # type: ignore

    @property
    def value(self) -> Value:
        # return repr(self.tag)
        raise NotImplementedError


class ColumnLabel:
    name: str

    def __init__(self, td: Tag) -> None:
        self.name = "".join(
            map(str, filter(lambda x: isinstance(x, NavigableString), td.contents))
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.name)})"

    def __eq__(self, value: object) -> bool:
        match value:
            case str():
                return self.name == value
            case ColumnLabel():
                return self.name == value.name
            case _:
                return False


class RowBase[ExtraIndex: Hashable, C: CellBase, Value]:
    type Index = Union[ExtraIndex, int]

    cell_cls: ClassVar[type[CellBase]] = CellBase

    @final
    def __init__(
        self,
        row_tag: Tag,
        raw_labels: list[ColumnLabel],
    ) -> None:
        # ? drop '本學期我預計要選的課程'
        self.column_tags = row_tag.select("td")[:-1]
        self.raw_labels = raw_labels
        self.label_idx = {label.name: idx for idx, label in enumerate(raw_labels)}

    # @overload
    # def __getitem__(self, index: Index) -> Value: ...

    # @overload
    # def __getitem__(self, index: slice | Sequence[Index]) -> list[C]: ...

    # def __getitem__(self, index: Index | slice | Sequence[Index]):

    def __getitem__(self, index: Index) -> Value:
        match index:
            case int():
                return self.cell_cls(
                    self.column_tags[index], self.raw_labels[index].name
                ).value
            # case slice() as cell_slice:
            #     return [
            #         self[i] for i in range(*cell_slice.indices(len(self.column_tags)))
            #     ]
            case _:
                # if isinstance(index, Sequence) and not isinstance(index, str):
                #     return [self[i] for i in index]
                return self.from_extra(index)  # type: ignore

        raise TypeError

    def from_extra(self, extra: ExtraIndex) -> C:
        raise NotImplementedError


# todo: paginated
class RowList[T: RowBase](Sequence):
    def __init__(self, soup: BeautifulSoup, row_cls: type[T]):
        table = soup.select("table")[6]
        self.row_tags: ResultSet[Tag] = table.select("tr")
        self.column_fields = [
            ColumnLabel(td) for td in self.row_tags.pop(0).select("td")
        ]
        self.row_cls = row_cls

    @lru_cache
    def __getitem__(self, index: int):
        return self.row_cls(self.row_tags[index], self.column_fields)

    def __len__(self) -> int:
        return len(self.row_tags)


class PaginatedRowList[R: RowBase, ExtraIndex: Hashable, C: CellBase, Value](Sequence):
    type Index = int | ExtraIndex

    def __init__(
        self,
        total: int,
        page_count: int,
        num_pages: int,
        get_page: Callable[[int], Tag],
        row_cls: type[RowBase[ExtraIndex, C, Value]] | None = None,
    ) -> None:
        self.total = total
        self.page_count = page_count
        self.num_pages = num_pages
        self.get_page = get_page
        self.row_cls = row_cls or RowBase

    @lru_cache
    def get_page_row(self, page_idx: int) -> RowList[RowBase[ExtraIndex, C, Value]]:
        soup = self.get_page(page_idx)
        return RowList(soup, self.row_cls)  # type: ignore

    @overload
    def __getitem__(self, index: int) -> R: ...

    @overload
    def __getitem__(
        self, index: slice | Sequence[int]
    ) -> list[RowBase[ExtraIndex, C, Value]]: ...

    @overload
    def __getitem__(self, index: tuple[int, ExtraIndex | int]) -> C: ...

    @overload
    def __getitem__(
        self, index: tuple[int, slice | Sequence[ExtraIndex | int]]
    ) -> Sequence[C]: ...

    @overload
    def __getitem__(
        self, index: tuple[slice | Sequence[int], ExtraIndex | int]
    ) -> Sequence[C]: ...

    @overload
    def __getitem__(
        self, index: tuple[slice | Sequence[int], slice | Sequence[Index]]
    ) -> Sequence[list[C]]: ...

    def __getitem__(self, index: object) -> object:
        match index:
            case int():
                if index >= self.total:
                    raise IndexError

                page_idx = index // self.page_count
                row_idx = index % self.page_count

                return self.get_page_row(page_idx)[row_idx]
            case slice():
                return [self[i] for i in range(*index.indices(self.total))]
            case (int() as row_idx, col_idx):
                return self[row_idx][col_idx]
            case (slice() as row_slice, col_idx):
                return [row[col_idx] for row in self[row_slice]]
            case _:
                if isinstance(index, Sequence):
                    return [self[int(i)] for i in index]
                raise TypeError

    def __len__(self) -> int:
        return self.total
