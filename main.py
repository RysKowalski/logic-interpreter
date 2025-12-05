class Operation:
    def __init__(self, code: int, operands: str) -> None:
        """0: flow_start, 1: flow_stop"""
        self.code: int = code
        self.operands: str = operands


class Program:
    def __init__(self, raw_program: list[str]) -> None:
        self.current_index: int = 0

        self.jumps: list[int] = []
        self.vars: list[int] = []
        self.operations: list[Operation] = []

        for line in raw_program:
            split_line: list[str] = line.split(" ")
            match split_line[0]:
                case "FLOW":
                    match split_line[1]:
                        case "START":
                            self.operations.append(Operation(0, ""))
                        case "END":
                            self.operations.append(Operation(1, ""))


def load_file(path: str = "./example.loi") -> list[str]:
    with open(path, "r") as file:
        return [line.rstrip("\n") for line in file]


if __name__ == "__main__":
    file = load_file()
    prog = Program(file)
    print(
        prog.current_index,
        [op.code for op in prog.operations] + [op.operands for op in prog.operations],
        prog.jumps,
        prog.vars,
        sep="\n",
    )
