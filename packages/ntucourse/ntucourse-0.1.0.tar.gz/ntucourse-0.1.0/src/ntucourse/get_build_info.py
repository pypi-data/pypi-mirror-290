import asyncio
import json

import bs4
import httpx
import requests
from utils import catch_json

name_map = {
    "共同": "共同",
    "普通": "普通",
    "新生": "新生",
    "綜合": "綜合",
    "博雅": "博雅",
    "1": "文學院",
    "2": "理學院",
    "3": "社科院",
    "4": "醫學院",
    "5": "工學院",
    "6": "生農學院",
    "7": "管理院",
    "8": "公衛院",
    "9": "電資院",
    "A": "法律院",
    "B": "生科院",
}


async def main():
    async with httpx.AsyncClient() as client:

        async def get_building(name: str):
            res = await client.get(
                "https://gra206.aca.ntu.edu.tw/classrm/acarm/get-classroom-by-building",
                params={"building": name},
            )
            return list(map(lambda x: x["cr_no"], res.json()["room_ls"]))

        tasks = [(get_building(name)) for name in name_map.keys()]
        results: list[list[str]] = await asyncio.gather(*tasks)

    building_map = {k: v for k, v in zip(name_map.keys(), results)}
    return building_map


@catch_json("building_map.json")
def get_building_map():
    return asyncio.run(main())


@catch_json("building_map_rev.json")
def get_building_map_rev():
    return {v: k for k, rooms in get_building_map().items() for v in rooms}
