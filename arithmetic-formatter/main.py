"""found problems (I did not think about scalability)
I just thought of making it as fast as possible and readable"""

from functools import partial
from typing import Iterable, List, Tuple, Union


def validate_input(problem: str):
    params = problem.split()
    assert len(params) == 3

    operand_one, operator, operand_two = [str(i) for i in params]
    assert min(len(operand_one), len(operand_two)) > 0

    if len(operand_one) > 4 or len(operand_two) > 4:
        raise SyntaxError("Error: Numbers cannot be more than four digits.")
    if not (operand_one.isdigit() and operand_two.isdigit()):
        raise SyntaxError("Error: Numbers must only contain digits.")
    if operator not in "+-":
        raise SyntaxError("Error: Operator must be '+' or '-'.")


def problem_formatter(problem: str) -> Tuple[str, str, str]:
    params = problem.split()
    operand_one, operator, operand_two = [str(i) for i in params]

    MAX_DIGITS = max(len(operand_one), len(operand_two)) + 2
    FORMAT_OPERATOR = f"{{:={operator}{MAX_DIGITS}d}}"
    FORMAT_SIMPLE = f"{{:{MAX_DIGITS}d}}"

    if operator == "-":
        operand_two = -int(operand_two)

    line1 = FORMAT_SIMPLE.format(int(operand_one))
    line2 = FORMAT_OPERATOR.format(int(operand_two))
    line3 = "-" * MAX_DIGITS

    return line1, line2, line3


def compute_formatted_result(problem: str):
    params = problem.split()
    operand_one, operator, operand_two = [str(i) for i in params]

    MAX_DIGITS = max(len(operand_one), len(operand_two)) + 2
    FORMAT_SIMPLE = f"{{:{MAX_DIGITS}d}}"

    if operator == "-":
        operand_two = -int(operand_two)

    result = int(operand_one) + int(operand_two)
    return FORMAT_SIMPLE.format(result)


def join_problems_lines(
    problems: Iterable,
    lines_to_group: int = 3,
):
    output = []
    for line in range(lines_to_group):
        output += [(" " * 4).join([problem[line] for problem in problems])]
    return "\n".join(output)


def arithmetic_arranger(problems: List[str], show_result: bool = False) -> str:
    if len(problems) > 5:
        return "Error: Too many problems."
    try:
        for _ in map(validate_input, problems):
            pass
    except SyntaxError as e:
        return str(e)

    vertical_problem_lines = [problem_formatter(problem) for problem in problems]

    output = ""
    if not show_result:
        output = join_problems_lines(vertical_problem_lines, lines_to_group=3)
    else:
        vertical_problem_lines = join_with_results(problems, vertical_problem_lines)
        output = join_problems_lines(vertical_problem_lines, lines_to_group=4)

    return output


def join_with_results(problems, vertical_problem_lines):
    result_per_problem = map(compute_formatted_result, problems)
    new_vertical_problem_lines = []
    for lines, result in zip(vertical_problem_lines, result_per_problem):
        line1, line2, line3 = lines
        new_vertical_problem_lines.append(
            (
                line1,
                line2,
                line3,
                result,
            )
        )

    return new_vertical_problem_lines
