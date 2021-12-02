from typing import Callable, Iterable, TypeVar, Generic, Any, Optional

T = TypeVar('T')

def input_for(filename: str) -> str:
    suffix = ".py"
    if filename.endswith(suffix):
        filename = filename[:-len(suffix)]
    return filename + ".txt"


def identity(x: T) -> T:
    return x


def read_lines(filename: str, func: Callable[[str], T] = lambda line: line) -> list[T]: # type: ignore
    print(f"Reading from {filename}... ", end="")
    with open(filename, 'r', encoding="utf8") as file:
        lines = file.readlines()
        stripped = [func(line.strip()) for line in lines]
        print("Done.")
        return stripped


def join(items: Iterable[T], sep: str = "", to_str: Callable[[T], str] = str) -> str:
    return sep.join(map(to_str, items))


def count_where(func: Callable[[T], bool], items: Iterable[T]) -> int:
    n = 0
    for item in items:
        if func(item):
            n += 1
    return n

