class Program:
    def __init__(self, raw_program: list[str]) -> None:
        self.current_index: int = 0

        self.jumps: list[int] = []
        self.vars: list[float | None] = []

        # 0: flow_start, 1: flow_stop, 2: flow_jump, 3: flow_def_jump
        # 4: DDD_set
        self.operations: list[tuple[int, str | int | list[str | int]]] = []

        for line in raw_program:
            split_line: list[str] = line.split(" ")
            match split_line[0]:
                case "FLOW":
                    match split_line[1]:
                        case "START":
                            self.operations.append((0, ""))
                        case "END":
                            self.operations.append((1, ""))
                        case "jump":
                            self.operations.append((2, int(split_line[2])))
                        case "def":
                            self.jumps.append(len(self.operations) + 1)
                        case _:
                            raise NameError("not found", split_line)
                case "DDD":
                    match split_line[1]:
                        case "def":
                            self.vars.append(None)
                        case "set":
                            self.operations.append((4, " ".join(split_line[3:])))
                        case 

    def process_expression(self, expression: str) -> float:
        return 1.0


def load_file(path: str = "./example.loi") -> list[str]:
    with open(path, "r") as file:
        return [line.rstrip("\n") for line in file]


if __name__ == "__main__":
    file = load_file()
    prog = Program(file)
    print(
        prog.current_index,
        [op[0] for op in prog.operations] + [op[1] for op in prog.operations],
        prog.jumps,
        prog.vars,
        sep="\n",
    )
