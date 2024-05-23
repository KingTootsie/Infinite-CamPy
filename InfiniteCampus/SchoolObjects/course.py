from typing import (List, TYPE_CHECKING)

if TYPE_CHECKING:
    from enrollment import Enrollment
    from term import Term
    from task import Task

class Course(object):
    def __init__(
        self, 

        enrollment: Enrollment,
        term: Term,

        course_name: str, 
        course_id: int,
        section_id: int, 
        teacher: str, 
        room: str, 
        school_name: str, 
        dropped: bool,

        tasks: List[Task],
    ) -> None:
        self.enrollment: Enrollment = enrollment
        self.term: Term = term #An attribute that refers to the parent Term object.

        self.name: str = course_name
        self.course_id: int = course_id
        self.section_id: int = section_id #Represented as sectionID from IC.
        self.teacher: str = teacher
        self.room: str = room
        self.school_name: str = school_name
        self.dropped: bool = dropped
        
        self.tasks: List[Task] = tasks

    def __repr__(self) -> str:
        return self.name


