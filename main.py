from typing import Any


class Program:
    def __init__(self, raw_program: list[str]) -> None:
        self.current_index: int = 0

        self.jumps: list[int] = []
        self.vars: list[float | None] = []

        # 0: flow_stop, 1: flow_jump, 2: DDD_set,
        # 3: IO_load, 4: IO_write_text, 5: IO_write_calculation,
        # 6: IO_write_expression,7: IO_write_newl, 8: IF
        self.operations: list[tuple[int, Any]] = []

        for line in raw_program:
            split_line: list[str] = line.split(" ")
            match split_line[0]:
                case "FLOW":
                    match split_line[1]:
                        case "END":
                            self.operations.append((0, None))
                        case "jump":
                            self.operations.append((1, int(split_line[2])))
                        case "def":
                            self.jumps.append(len(self.operations) + 1)
                case "DDD":
                    match split_line[1]:
                        case "def":
                            self.vars.append(None)
                        case "set":
                            self.operations.append(
                                (2, (int(split_line[2]), split_line[3:]))
                            )
                case "IO":
                    match split_line[1]:
                        case "load":
                            text: str = ""
                            for word in " ".join(split_line[3:]):
                                if word != "æ":  # this symbol symbolizes space char
                                    text += word
                                else:
                                    text += ""  # this adds space, python is strange
                            self.operations.append((3, (int(split_line[2]), text)))
                        case "write":
                            match split_line[2]:
                                case "text":
                                    self.operations.append(
                                        (4, " ".join(split_line[3:]))
                                    )
                                case "calc":
                                    self.operations.append((5, split_line[3:]))
                                case "exp":
                                    self.operations.append((6, split_line[3:]))
                                case "newl":
                                    self.operations.append((7, None))
                case "IF":
                    self.operations.append(
                        (8, (split_line[3:], split_line[1], split_line[2]))
                    )

    def _load_var(self, idx: int) -> float:
        value = self.vars[idx]
        if value is None:
            raise ValueError(f"variable {idx} is None")
        return value

    def _prefix_postfix(self, token: str) -> float:
        """Return value_to_use"""
        if "$" not in token:
            return float(token)

        if "+" not in token and "-" not in token:
            return self._load_var(int(token[1:]))

        var_index: int = 0
        last_char: str = token[-1]
        if last_char == "+":
            var_index = int(token[1:-2])
            value = self._load_var(var_index)
            self.vars[var_index] = value + 1
            return value
        elif last_char == "-":
            var_index = int(token[1:-2])
            value = self._load_var(var_index)
            self.vars[var_index] = value - 1
            return value

        first_char: str = token[0]
        if first_char == "+":
            var_index = int(token[3:])
            value = self._load_var(var_index)
            value += 1
            self.vars[var_index] = value
            return value
        elif first_char == "-":
            var_index = int(token[3:])
            value = self._load_var(var_index)
            value -= 1
            self.vars[var_index] = value
            return value
        raise ValueError(f"error in token '{token}'")

    def process_calculation(self, tokens: list[str]) -> float:
        if not tokens:
            raise ValueError("empty expression")

        value = self._prefix_postfix(tokens[0])

        i = 1
        while i < len(tokens):
            op = tokens[i]
            rhs_token = tokens[i + 1]
            rhs = self._prefix_postfix(rhs_token)

            if op == "+":
                value = value + rhs
            elif op == "-":
                value = value - rhs
            elif op == "*":
                value = value * rhs
            elif op == "/":
                value = value / rhs
            elif op == "**":
                value = value**rhs
            elif op == "%":
                value = value % rhs
            else:
                raise ValueError(f"unknown operator {op}")

            i += 2

        return value

    def evaluate_expression(self, calculation: list[str]) -> bool:
        return True

    def run_program(self) -> None:
        for line in self.operations:
            # # DEBUG THINGS ==========
            # debug_dict: dict[int, str] = {
            #     0: "flow_stop",
            #     1: "flow_jump",
            #     2: "DDD_set",
            #     3: "IO_load",
            #     4: "IO_write_text",
            #     5: "IO_write_calculation",
            #     6: "IO_write_expression",
            #     7: "IO_write_newl",
            #     8: "IF",
            # }
            # print(f"CURRENT_INDEX: {self.current_index}", end="\n\n")
            # print("LINE:")
            # print(debug_dict[line[0]], line[1], end="\n\n")
            # print("VARS:")
            # print(self.vars, end="\n=================================\n\n")
            # =======================

            match line[0]:
                case 0:  # flow_stop
                    return
                case 1:  # flow_jump int: number_line
                    self.current_index = line[1]
                case 2:  # DDD_set tuple[int: var_index, list[str]: calculation]
                    print(line[1][1])
                    print(self.vars)
                    self.vars[line[1][0]] = self.process_calculation(line[1][1])
                    print(self.vars)
                case 3:  # IO_load tuple[int: var_index, str: prompt]
                    self.vars[line[1][0]] = float(input(line[1][1]))
                case 4:  # IO_write_text str: text
                    print(line[1], end="")
                    self.current_index += 1
                case 5:  # IO_write_calculation list[str]: calculation
                    print(self.process_calculation(line[1]))
                    self.current_index += 1
                case 6:  # IO_write_expression list[str]: expression
                    print(self.evaluate_expression(line[1]))
                    self.current_index += 1
                case 7:  # IO_write_newl None
                    print()
                    self.current_index += 1
                case 8:  # IF tuple[list[str]: expression, int: line_index, int: else_line_index]
                    if self.evaluate_expression(line[1][0]):
                        self.current_index = line[1][1]
                    else:
                        self.current_index = line[1][2]


def load_file(path: str = "./example.loi") -> list[str]:
    with open(path, "r") as file:
        return [line.rstrip("\n") for line in file]


def tests() -> bool:
    prog: Program = Program([])
    for i in range(100):
        prog.vars.append(None)

    test_list: list[tuple[int, list[str], list[tuple[int, float]]]] = [
        (0, ["0"], []),
        (20, ["20"], []),
        (0, ["$0"], [(0, 0.0)]),
        (4, ["2", "+", "2"], []),
        (4, ["2", "*", "2"], []),
        (1, ["2", "/", "2"], []),
        (6, ["$0", "+", "$1"], [(0, 2.0), (1, 4.0)]),
        (4, ["4", "*", "$0", "/", "$0"], [(0, 256.0)]),
        (3, ["++$0"], [(0, 2.0)]),
        (6, ["$0++", "+", "3"], [(0, 3.0)]),
        (-10, ["3", "+", "2", "-", "10", "*", "3", "/", "2"], []),
        (2, ["$0++", "+", "++$1", "+", "--$2"], [(0, 2), (1, 3), (2, -3)]),
        (2, ["$0++"], [(0, 2.0)]),
        (3, ["++$0"], [(0, 2.0)]),
    ]
    tests_passed: bool = True
    passed: int = 0
    for i, test in enumerate(test_list):
        prog.vars = [None for _ in range(10)]
        for var in test[2]:
            prog.vars[var[0]] = var[1]
        try:
            answer: float = prog.process_calculation(test[1])
        except ValueError as error:
            print("\033[1;31m" + f"TEST {i + 1}/{len(test_list)} FAILED")
            print(error, "\033[0m")
            continue

        test_passed: bool = answer == test[0]
        if test_passed:
            print("\033[1;32m" + f"TEST {i + 1}/{len(test_list)} PASSED" + "\033[0m")
            passed += 1
        else:
            tests_passed = False
            print("\033[1;31m" + f"TEST {i + 1}/{len(test_list)} FAILED")
            print(f"EXPECTED VALUE: {test[0]}, PROVIDED VALUE: {answer}")
            print("COMPUTATION:", test[1])
            print("VARS:", prog.vars, "\033[0m\n")
    print(f"TESTS PASSED {passed}/{len(test_list)}")

    return tests_passed


def run():
    program: Program = Program(load_file())
    program.run_program()


if __name__ == "__main__":
    tests()
