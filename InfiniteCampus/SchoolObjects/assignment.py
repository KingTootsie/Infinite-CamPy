#https://siouxfallssd.infinitecampus.org/campus/resources/portal/section/2053248?_expand=course&_expand=terms&_expand=periods-periodSchedule&_expand=teacherPreference&_expand=room&_expand=teachers
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from term import Term
    from course import Course
    from category import Category
    from category import Category

class Assignment(object):
    """Represents an assignment in an IC course."""
    def __init__(
        self, 
        term, 
        course, 
        category, 
        assignment_name: str, 
        points_earned: float, 
        max_points: float, 
        not_graded: bool, 
        late: bool, 
        missing: bool, 
        cheated: bool, 
        dropped: bool
    ) -> None:
        self.term: Term = term
        self.course: Course = course
        self.category: Category = category
        self.name = assignment_name
        self.points_earned = points_earned
        self.max_points = max_points
        self.not_graded = not_graded
        self.late = late
        self.missing = missing
        self.cheated = cheated
        self.dropped = dropped
        
    def __repr__(self) -> str:
        return self.name