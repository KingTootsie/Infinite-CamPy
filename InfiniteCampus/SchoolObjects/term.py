from datetime import datetime
from typing import (List, Union, TYPE_CHECKING)
from infinitecampus import InfiniteCampusExceptions

if TYPE_CHECKING:
    from enrollment import Enrollment
    from course import Course



class Term(object):
    """Represents a part of the school year.\n
    Most schools use a semester system (2 terms) but this'll change depending on school.
    """
    def __init__(
        self, 

        enrollment: Enrollment,

        term_name: str, 
        term_id: int, 
        start_date: str, 
        end_date: str, 
        
        courses: Union[List[Course], None],
    ) -> None:
        self.enrollment: Enrollment = enrollment

        self.name: str = term_name
        self.id: int = term_id
        self.start_date: datetime = datetime.fromisoformat(start_date)
        self.end_date: datetime = datetime.fromisoformat(end_date)

        self.courses: Union[List[Course], None] = courses

    def fetch_course(self, query: str, search_type):
        if search_type == "name":
            for course in self.courses:
                if course.name == query:
                    return course
            else:
                return None
        elif search_type == "course_id":
            try:
                query = int(query)
            except ValueError:
                raise InfiniteCampusExceptions.SearchExceptions.CourseIDMustBeInteger
            for course in self.courses:
                if course.id == int(query):
                    return course
            else:
                return None

    def __repr__(self) -> str:
        return self.name