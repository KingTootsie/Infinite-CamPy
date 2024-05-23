from typing import (List, Union, TYPE_CHECKING)
from datetime import datetime, date

if TYPE_CHECKING:
    from term import Term

class Enrollment(object):
    """Represents a currently enrolled school."""

    def __init__(
        self,

        enrollment_name: str,
        enrollment_id: int,
        calendar_id: int,
        school_id: int,
        structure_id: int,
        end_date: Union[date, None],
        grades_enabled: bool, #Honestly not sure what this means.
        assignments_enabled: bool,
        grading_key_enabled: bool, #This either.

        terms: List[Term],
    ) -> None:
        self.name: str = enrollment_name
        self.id: int = enrollment_id
        self.calendar_id: int = calendar_id
        self.school_id: int = school_id
        self.structure_id: int = structure_id
        self.end_date: Union[date, None] = end_date
        self.grades_enabled: bool = grades_enabled
        self.assignments_enabled: bool = assignments_enabled
        self.grading_key_enabled: bool = grading_key_enabled

        self.terms: List[Term] = terms

    def __repr__(self) -> str:
        return self.name