from typing import Literal, TypedDict


class Operation(TypedDict):
    # 0: flow_start, 1: flow_stop
    code: int
    operands: str


class Program(TypedDict):
    jumps: list[int]
    vars: list[int]
    operations: list[Operation]


def load_file(path: str = "./example.loi") -> list[str]:
    with open(path, "r") as file:
        return file.readlines()


if __name__ == "__main__":
    print(load_file())
