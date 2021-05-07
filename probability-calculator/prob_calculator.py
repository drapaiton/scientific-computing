"""you can use a mathematical formula to calculate event dependent probability,
here we using brute-force approach"""
import copy
import random

# Consider using the modules imported above.
from typing import List


class Hat:
    _contents: List[str]

    def __init__(self, **kwargs):
        if len(kwargs) == 0:
            raise ValueError("hat Can't be empty")
        self._contents = []
        for item, quantity in kwargs.items():
            self._contents.extend([item] * quantity)

    def draw(self, quantity: int):
        if quantity >= len(self._contents):
            return self._contents

        random_items = [self.pick_from_hat(True) for _ in range(quantity)]

        return random_items

    def pick_from_hat(self, remove_from_hat: bool = False) -> str:
        random_number = random.randint(0, len(self._contents) - 1)
        if remove_from_hat:
            return self._contents.pop(random_number)
        else:
            return self._contents[random_number]

    @property
    def contents(self) -> List[str]:
        return self._contents

    @contents.setter
    def contents(self, value):
        self._contents = value


def experiment(
    hat: Hat, expected_balls: dict, num_balls_drawn: int, num_experiments: int
):
    assert all([i in hat.contents for i in expected_balls])

    asserted_experiment_count = 0
    for _ in range(num_experiments):
        a = copy.deepcopy(hat)

        picked = a.draw(num_balls_drawn)

        if all([picked.count(item) >= expected_balls[item] for item in expected_balls]):
            asserted_experiment_count += 1

    return asserted_experiment_count / num_experiments
