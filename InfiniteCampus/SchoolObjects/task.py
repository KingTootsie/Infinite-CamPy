from typing import (List, TYPE_CHECKING, Union)

if TYPE_CHECKING:
    from term import Term
    from course import Course
    from category import Category
#https://siouxfallssd.infinitecampus.org/campus/api/instruction/categories?sectionID=2054177
#https://siouxfallssd.infinitecampus.org/campus/resources/portal/grades/detail/2054177?showAllTerms=false&selectedTermID=8025
class Task(object):
    """Represents a task in IC. 
    \nTypically you'll see only 4 tasks in a course, but there could be more or less.
    """
    def __init__(self, 
        term,
        course,
        task_name: str, 
        task_percent: Union[float, None], 
        points_earned: Union[float, None],
        total_points: Union[float, None], 
        categories = None
    ) -> None:
        term: Term = term
        self.course: Course = course
        self.name = task_name
        self.percent = task_percent
        self.points_earned = points_earned
        self.total_points = total_points
        self.categories: list[Category] = categories
        
    def __repr__(self) -> str:
        return self.name