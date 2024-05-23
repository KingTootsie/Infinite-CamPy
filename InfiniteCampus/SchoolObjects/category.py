#These are the categories within a course category.
#For example, these would look like tabs saying "Labs", "Tests", and "Homework".
#You'll notice this differs from categories who have tabs saying things like "Midterm", "Semester", "Semester Test" and "Final".

from typing import (List, Optional, TYPE_CHECKING)

if TYPE_CHECKING:
    from enrollment import Enrollment
    from term import Term
    from course import Course
    from task import Task
    from assignment import Assignment

class Category(object):
    """Represents a subcategory in IC.
    \nUsually only seen in the semester category.
    """
    def __init__(
        self,

        enrollment: Enrollment,
        term: Term,
        course: Course,
        task: Task, 

        category_name: str, 

        assignments: List[Assignment]
    ) -> None:
        self.enrollment: Enrollment = enrollment
        self.term: Term = term
        self.course: Course = course
        self.task: Task = task

        self.name: str = category_name
        
        self.assignments: List[Assignment] = assignments

    def __repr__(self) -> str:
        return self.name