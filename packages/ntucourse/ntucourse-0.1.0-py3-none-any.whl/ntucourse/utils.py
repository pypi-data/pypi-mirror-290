import json
import pathlib
from functools import lru_cache
from typing import Callable



def catch_json(filename: str):
    path = pathlib.Path(__file__).parent / filename

    def decorator[T, **P](func: Callable[P, T]) -> Callable[P, T]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except FileNotFoundError:
                res = func(*args, **kwargs)
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(res, f, ensure_ascii=False, indent=4)
                return res

        return lru_cache(wrapper)  # type: ignore

    return decorator
