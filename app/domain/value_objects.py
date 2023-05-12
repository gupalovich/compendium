from dataclasses import dataclass
from datetime import date, timedelta


class BusinessRuleValidationException(Exception):
    """A base class for all business rule validation exceptions"""


class ValueObject:
    """A base class for all value objects"""


@dataclass(frozen=True)
class DateRange(ValueObject):
    """Our first value object"""

    start_date: date
    end_date: date

    def __post_init__(self):
        """Here we check if a value object has a valid state."""
        if self.start_date >= self.end_date:
            raise BusinessRuleValidationException(
                "end date date should be greater than start date"
            )

    def days(self):
        """Returns the number of days between the start date and the end date"""
        delta = self.end_date - self.start_date + timedelta(days=1)
        return delta.days

    def extend(self, days):
        """Extend the end date by a specified number of days"""
        new_end_date = self.end_date + timedelta(days=days)
        return DateRange(self.start_date, new_end_date)


@dataclass(frozen=True)
class Location2D(ValueObject):
    """A 2D location"""

    x: float
    y: float

    def as_tuple(self):
        """Return the location as a tuple (x, y)"""
        return (self.x, self.y)


@dataclass(frozen=True)
class Rect2D(ValueObject):
    """A 2D rectangle"""

    top_left: Location2D
    bottom_right: Location2D

    def contains(self, location: Location2D):
        """Returns true if the location is contained in the rectangle"""
        return (
            location.x >= self.top_left.x
            and location.x <= self.bottom_right.x
            and location.y >= self.top_left.y
            and location.y <= self.bottom_right.y
        )
