from typing import Callable, Iterable, TypeVar, Generic, Any, Optional

T = TypeVar("T")


def input_for(filename: str, sample: bool = False) -> str:
    suffix = ".py"
    if filename.endswith(suffix):
        filename = filename[: -len(suffix)]
    if sample:
        filename += "_sample"
    return filename + ".txt"


def identity(x: T) -> T:
    return x


def read_lines(filename: str, func: Callable[[str], T]) -> list[T]:  # type: ignore
    print(f"Reading from {filename}... ", end="")
    with open(filename, "r", encoding="utf8") as file:
        lines = file.readlines()
        stripped = [func(line.strip()) for line in lines]
        print("Done.")
        return stripped


def read_first_line(filename: str, sep: str, func: Callable[[str], T]) -> list[T]:  # type: ignore
    line = read_lines(filename, str)[0]
    return [func(part) for part in line.split(sep)]


def join(items: Iterable[T], sep: str = "", to_str: Callable[[T], str] = str) -> str:
    return sep.join(map(to_str, items))


def count_where(pred: Callable[[T], bool], items: Iterable[T]) -> int:
    n = 0
    for item in items:
        if pred(item):
            n += 1
    return n


def find_where(pred: Callable[[T], bool], items: Iterable[T]) -> T:
    for e in items:
        if pred(e):
            return e
    raise ValueError("No element found")


def find_all_where(pred: Callable[[T], bool], items: Iterable[T]) -> list[T]:
    return [e for e in items if pred(e)]


def first(items: Iterable[T]) -> T:
    for e in items:
        return e
    raise ValueError("No element found")


def flatten(items: list[list[T]]) -> list[T]:
    return [item for sublist in items for item in sublist]


def index_where(pred: Callable[[T], bool], items: Iterable[T]) -> int:
    for i, e in enumerate(items):
        if pred(e):
            return i
    return -1


def all_indices_where(pred: Callable[[T], bool], items: Iterable[T]) -> list[int]:
    return [i for i, e in enumerate(items) if pred(e)]


def transposed(matrix: list[list[T]]) -> list[list[T]]:
    return list(map(list, zip(*matrix)))


def sign(a: int) -> int:
    return 1 if a > 0 else -1 if a < 0 else 0
