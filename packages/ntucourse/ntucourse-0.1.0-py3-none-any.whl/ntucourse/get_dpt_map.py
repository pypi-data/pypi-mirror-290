import asyncio
import json
import pathlib
from functools import lru_cache
from typing import Callable

import httpx
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from utils import catch_json



def get_departments():
    res = requests.get("https://nol.ntu.edu.tw/nol/coursesearch/search_for_02_dpt.php")
    soup = BeautifulSoup(res.text, "html.parser")

    departments = soup.select("#dptname option")[1:]
    return departments


def split_dpt(text: str):
    text = text.strip()
    idx = text.find(" ")
    return text[:idx], text[idx + 1 :]


@catch_json("dpt_name_map.json")
def get_dpt_name_map():
    return {
        dpt_code: dpt_name
        for dpt_code, dpt_name in (split_dpt(dpt.text) for dpt in get_departments())
    }


@catch_json("dpt_code_map.json")
def get_dpt_code_map():
    return {
        dpt_name: dpt_code
        for dpt_code, dpt_name in (split_dpt(dpt.text) for dpt in get_departments())
    }


async def get_dpt_results():
    dpt_codes = list(get_dpt_code_map().values())
    pbar = tqdm(total=len(dpt_codes))
    limits = httpx.Limits(max_keepalive_connections=20, max_connections=150)
    timeout = httpx.Timeout(60.0, connect=60.0)
    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:

        async def get_dpt(dpt_code: str):
            # print(dpt_code,1)
            res = await client.get(
                "https://nol.ntu.edu.tw/nol/coursesearch/search_for_02_dpt.php",
                params={
                    "current_sem": "113-1",
                    # "dpt_sel": "4000",
                    "dptname": dpt_code,
                    "yearcode": 0,
                    "selcode": -1,
                    "alltime": "yes",
                    "allproced": "yes",
                    "allsel": "yes",
                    "page_cnt": 1,
                },
            )
            # print(dpt_code,2)
            pbar.update(1)
            return res.text

        results1 = await asyncio.gather(
            *(get_dpt(dpt_code) for dpt_code in dpt_codes[: len(dpt_codes) // 2])
        )
        results2 = await asyncio.gather(
            *(get_dpt(dpt_code) for dpt_code in dpt_codes[len(dpt_codes) // 2 :])
        )
    return [*results1, *results2]


@catch_json("dpt_short_name_map.json")
def get_short_name_map():
    short_name_map = {dpt_name: dpt_name for dpt_name in get_dpt_code_map().keys()}

    dpt_results = asyncio.run(get_dpt_results())
    for (dpt_name, dpt_code), text in zip(get_dpt_code_map().items(), dpt_results):
        soup = BeautifulSoup(text, "html.parser")
        try:
            short_name = (
                soup.find_all("table")[-2].find_all("tr")[1].find_all("td")[1].text
            )
            short_name_map[dpt_name] = short_name
        except IndexError:
            pass
    return short_name_map


def get_full_name_map():
    return {v: k for k, v in get_short_name_map().items()}


if __name__ == "__main__":
    from rich import print

    print(get_short_name_map())
