import asyncio
from enum import Enum
from functools import lru_cache
from typing import (
    Mapping,
    TypedDict,
)

import httpx
from base import CellBase, PaginatedRowList, RowBase
from bs4 import BeautifulSoup, Tag
from label import (
    LABEL_MAP,
    RAW_LABEL_MAP,
    Category,
    Department,
    Duration,
    EnrollmentRule,
    Label,
    Schedule,
    parse_tag,
)


def ceil_div(a: int, b: int) -> int:
    return (a + b - 1) // b


def _to_str_dict(d: Mapping[str, object]) -> dict[str, str]:
    return {k: str(v) for k, v in d.items()}


type CellValue = (
    str | float | Department | Duration | EnrollmentRule | Category | Schedule
)


class Cell(CellBase[Label, CellValue]):
    @property
    def value(self) -> CellValue:
        return parse_tag(self.tag, self.label)

    def parse_label(self, label: str) -> Label:
        return LABEL_MAP[label]


class Row(RowBase[Label, Cell, CellValue]):
    cell_cls = Cell

    def from_extra(self, extra: Label) -> Cell:
        return self[self.raw_labels.index(RAW_LABEL_MAP[extra])]  # type: ignore


MAX_PAGE_COUNT = 150


class QueryType(Enum):
    TITLE = 1
    INSTRUCTOR = 2
    CODE = 3
    IDENTIFIER = 4
    SERIAL = 5


class Params(TypedDict):
    current_sem: str
    cstype: int
    csname: str
    alltime: str
    allproced: str
    allsel: str
    page_cnt: int
    start_rec: int


def build_params(
    query_type: QueryType,
    query_value: str | int,
    semester: str,
    page_count: int,
    offset: int = 0,
) -> Params:
    if page_count > MAX_PAGE_COUNT:
        raise ValueError(f"page_count must be less than {MAX_PAGE_COUNT}")

    return {
        "current_sem": semester,
        "cstype": query_type.value,
        "csname": str(query_value),
        "alltime": "yes",
        "allproced": "yes",
        "allsel": "yes",
        "page_cnt": page_count,
        "start_rec": offset,
    }


class Search:
    def __init__(
        self,
        query_type: QueryType,
        query_value: str | int,
        semester: str,
        page_count=15,
        page_batch_size=5,
    ):
        self.page_count = page_count
        self.page_batch_size = page_batch_size
        self.page_cache: dict[int, BeautifulSoup] = {}

        self.params = build_params(
            query_type,
            query_value,
            semester,
            page_count=page_count,
        )

        soup0 = self.get_page(0, batch=False)
        self.total = self.get_total(soup0)

        # print(self.total, self.num_pages)

        # self.html = response.text

    @property
    def num_pages(self):
        return ceil_div(self.total, self.page_count)

    @staticmethod
    def get_total(soup: Tag):
        return int(soup.select("table")[5].select("td b")[0].text)

    def get_page(self, page_idx: int, batch=True):
        if page_idx in self.page_cache:
            return self.page_cache[page_idx]

        st = page_idx
        end = st + self.page_batch_size if batch else page_idx + 1

        async def fetch_pages():
            return await asyncio.gather(
                *[self._get_single_page(i) for i in range(st, end)]
            )

        asyncio.run(fetch_pages())
        return self.page_cache[page_idx]

    async def _get_single_page(self, page_idx: int):
        if page_idx in self.page_cache:
            return self.page_cache[page_idx]

        offset = page_idx * self.page_count
        params: Params = {**self.params, "start_rec": offset}

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://nol.ntu.edu.tw/nol/coursesearch/search_result.php",
                params=_to_str_dict(params),
            )
            return self.page_cache.setdefault(
                page_idx, BeautifulSoup(response.text, "html.parser")
            )

    @property
    @lru_cache
    def rows(self) -> PaginatedRowList[Row, Label, Cell, CellValue]:
        return PaginatedRowList(
            total=self.total,
            page_count=self.page_count,
            num_pages=self.num_pages,
            get_page=self.get_page,
            row_cls=Row,
        )
