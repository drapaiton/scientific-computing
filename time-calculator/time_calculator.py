"""Do not import any Python libraries. Assume that the start times are valid times.
The minutes in the duration time will be a whole number less than 60,
but the hour can be any whole number."""
from dataclasses import dataclass
from enum import IntEnum, auto, unique
from typing import Tuple, Union


@unique
class WeekDays(IntEnum):
    """using index property as position order"""

    Sunday = auto()
    Monday = auto()
    Tuesday = auto()
    Wednesday = auto()
    Thursday = auto()
    Friday = auto()
    Saturday = auto()


@unique
class AmPm(IntEnum):
    """using value property as hour quantity"""

    AM = 0
    PM = 12


@dataclass
class BaseClock:
    _hours: int = 0
    _minutes: int = 0
    _am_pm: AmPm = AmPm.AM

    @property
    def hours(self) -> int:
        hours_from_minutes = self._minutes // 60
        last_day_hour = (self._hours + hours_from_minutes + self._am_pm.value) % 24

        if last_day_hour == 0 or last_day_hour == 12:
            output_hour = 12
        else:
            output_hour = last_day_hour % 12

        return output_hour

    @property
    def minutes(self) -> int:
        return self._minutes % 60

    @property
    def am_pm(self) -> AmPm:
        hours_from_minutes = self._minutes // 60
        last_day_hour = (self._hours + hours_from_minutes + self._am_pm.value) % 24

        index = last_day_hour // 12
        # minimize to 0 or 1, to cap am or pm
        index %= 2
        return list(AmPm)[index]

    @hours.setter
    def hours(self, to_set: int):
        self._hours = to_set

    @minutes.setter
    def minutes(self, to_set: int):
        self._minutes = to_set

    @am_pm.setter
    def am_pm(self, to_set: AmPm):
        self._am_pm = to_set


@dataclass
class BaseDate(BaseClock):
    """TODO add handlers for month, leap days, etc..."""

    _day = 0
    _week_day: WeekDays = WeekDays.Sunday

    @property
    def day(self) -> int:
        hours_from_minutes = self._minutes // 60
        total_hours = self._hours + hours_from_minutes + self._am_pm.value

        accumulated_days = total_hours // 24
        return self._day + accumulated_days

    @property
    def week_day(self):
        actual_weekday_idx = self.day % 7
        actual_idx = self._week_day.value - 1

        new_idx = (actual_idx + actual_weekday_idx) % len(WeekDays)
        return list(WeekDays)[new_idx]

    @week_day.setter
    def week_day(self, to_set: WeekDays):
        total_week_day_index: int = self._week_day.value - 1 + to_set.value - 1
        valid_weekday_index: int = total_week_day_index % len(WeekDays)

        final_weekday: WeekDays = list(WeekDays)[valid_weekday_index]
        self._week_day = final_weekday

    @staticmethod
    def _parse_weekday(starting_weekday: Union[str, WeekDays]) -> WeekDays:
        if not starting_weekday:
            return list(WeekDays).pop(0)
        else:
            if type(starting_weekday) is WeekDays:
                return starting_weekday
            else:
                return WeekDays[starting_weekday.capitalize()]


class FullDate(BaseDate):
    REPRESENTATION_FORMAT = "{}:{:0>2d} {}"
    show_weekday = False

    def __init__(
        self, start: str, duration: str, starting_weekday: Union[str, WeekDays] = None
    ):
        """TODO add REGEX check for start,duration and starting_weekday"""
        try:
            # parsing and checking
            assert len(start.split()) == 2
            assert len(duration.split(":")) == 2

            start_time, am_pm = start.split()
            assert len(start_time.split(":")) == 2

            # assign to variables
            self.week_day = self._parse_weekday(starting_weekday)

            # getting numerical values and assign to variables
            self.hours, self.minutes = map(int, start_time.split(":"))
            self.am_pm = AmPm[am_pm]

            duration_hours, duration_minutes = map(int, duration.split(":"))
            self.hours += duration_hours
            self.minutes += duration_minutes

            if starting_weekday:
                self.show_weekday = True
        except AssertionError as e:
            assert ValueError(f"invalid arguments when building FullDate [{e}]")
        except SyntaxError as e:
            raise SyntaxError(f"error handling hours for [{start}]\n [{e}]")

    def get_elapsed_days_repr(self) -> str:
        if self.day == 0:
            return ""
        elif self.day == 1:
            return "(next day)"
        else:
            return f"({self.day} days later)"

    def __str__(self):
        positioned_values: Tuple = (
            str(self.hours),
            int(self.minutes),
            str(self.am_pm.name),
        )
        output = self.REPRESENTATION_FORMAT.format(*positioned_values)

        if self.show_weekday:
            output = ", ".join([output, self.week_day.name])

        if elapsed_days_output := self.get_elapsed_days_repr():
            return " ".join([output, elapsed_days_output])
        else:
            return output

    def __repr__(self):
        return self.__str__()


def add_time(*args, **kwargs):
    return FullDate(*args, **kwargs).__str__()


if __name__ == "__main__":
    print(add_time("11:40 AM", "0:25"))
