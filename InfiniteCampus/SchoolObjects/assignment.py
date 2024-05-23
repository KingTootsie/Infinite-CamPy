#https://siouxfallssd.infinitecampus.org/campus/resources/portal/section/2053248?_expand=course&_expand=terms&_expand=periods-periodSchedule&_expand=teacherPreference&_expand=room&_expand=teachers
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enrollment import Enrollment
    from term import Term
    from course import Course
    from category import Task
    from category import Category

class Assignment(object):
    """Represents an assignment in an IC course."""
    def __init__(
        self, 

        enrollment: Enrollment,
        term: Term, 
        course: Course, 
        task: Task,
        category: Category, 
        
        assignment_name: str, 
        points_earned: float, 
        max_points: float, 
        not_graded: bool, 
        late: bool, 
        missing: bool, 
        cheated: bool, 
        dropped: bool
    ) -> None:
        self.enrollment: Enrollment = enrollment
        self.term: Term = term
        self.course: Course = course
        self.task: Task = task
        self.category: Category = category
        
        self.name = assignment_name
        self.points_earned = points_earned
        self.max_points = max_points
        self.percent = round((self.points_earned / self.max_points) * 100, 2) if self.points_earned is not None and self.max_points is not None and self.max_points != 0 else None
        self.not_graded = not_graded
        self.late = late
        self.missing = missing
        self.cheated = cheated
        self.dropped = dropped
        
    def __repr__(self) -> str:
        return self.name