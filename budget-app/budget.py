from __future__ import annotations

from itertools import zip_longest
from math import floor
from typing import List, Tuple, Union


class Category:
    STR_SIZE = 30

    ledger: List[dict]
    balance: int

    def __init__(self, name: str):
        self.name = name
        self.ledger = []

    def deposit(self, amount: Union[float, int], description: str = ""):
        self.ledger += [{"amount": float(amount), "description": description}]
        return self

    def withdraw(self, amount: Union[float, int], description: str = "") -> bool:
        if not self.check_funds(amount):
            return False

        self.deposit(-amount, description)
        return True

    def get_balance(self) -> Union[float, int]:

        return sum([i["amount"] for i in self.ledger])

    def transfer(self, amount: Union[float, int], destination: Category):
        is_ok = self.withdraw(amount, f"Transfer to {destination.name}")
        if not is_ok:
            return False

        destination.deposit(amount, f"Transfer from {self.name}")
        return True

    def check_funds(self, amount: Union[float, int]) -> bool:
        could_be_processed = self.get_balance() >= amount
        return could_be_processed

    def __str__(self):
        title = self.name.center(self.STR_SIZE, "*")

        # modifying for more than 2 decimals won't work
        def format_item(amount: Union[int, float], description: str) -> str:
            amount_lon = len(str(float(amount)))
            if int(amount) == float(amount):
                # add extra space to 1.00 instead of 1.0 py default
                amount_lon += 1

            description_cut = description[: self.STR_SIZE - amount_lon - 1]
            description_size = self.STR_SIZE - amount_lon - 1
            ITEM_TEMPLATE = f"{{:{description_size}}} {{:>{amount_lon}.2f}}"
            return ITEM_TEMPLATE.format(description_cut, amount)

        items = "\n".join([format_item(**i) for i in self.ledger])
        total = f"Total: {self.get_balance():.2f}"

        return "\n".join([title, items, total])


def create_spend_chart(categories: List[Category]):
    """we use categories index order"""
    TITLE = "Percentage spent by category"

    def get_total_withdraws(cat: Category) -> int:
        """transfer counts as a withdraw, return absolute spend money"""
        amounts = [i["amount"] for i in cat.ledger]
        return abs(sum(filter(lambda x: x < 1, amounts)))

    total_spent: Union[float, int] = sum(map(get_total_withdraws, categories))
    # cat stands for category
    cat_spent: Tuple = tuple(get_total_withdraws(c) for c in categories)
    cat_percentages = tuple((spent / total_spent) * 100 for spent in cat_spent)

    ABSTRACT_PERCENTAGE_LINE = "{percentage:>3}| "
    # add spaces for each category
    ABSTRACT_PERCENTAGE_LINE += "  ".join(["{}"] * len(categories))

    def get_repr(to_check: Union[float, int], value_expected: Union[float, int]) -> str:
        is_major = floor(to_check) >= value_expected
        return "o" if is_major else " "

    percentage_chart: List[str] = []
    for actual_percentage in range(100, -1, -10):
        representations = [get_repr(p, actual_percentage) for p in cat_percentages]

        percentage_chart += [
            ABSTRACT_PERCENTAGE_LINE.format(
                percentage=actual_percentage,
                *representations,
            ),
        ]
    # specific modification to pass tests
    percentage_chart = [line + "  " for line in percentage_chart]

    # separator_line
    chart_max_len = max(map(len, percentage_chart))
    separator_line = f'{"":<4}{"":->{chart_max_len-4}}'

    cat_names = [c.name for c in categories]
    # iterates trough every char every index of every cat name
    # shortest names are filled with blank spaces
    name_lines = zip_longest(*cat_names, fillvalue=" ")

    # minor adjustment
    ABSTRACT_NAME_LINE = f'{"":>5}'
    ABSTRACT_NAME_LINE += "  ".join(["{}"] * len(categories))
    # specific modification to pass tests
    ABSTRACT_NAME_LINE += "  "
    name_lines = [ABSTRACT_NAME_LINE.format(*chars) for chars in name_lines]
    return "\n".join([TITLE, *percentage_chart, separator_line, *name_lines])
