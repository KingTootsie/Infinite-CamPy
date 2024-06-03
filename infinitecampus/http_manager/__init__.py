import requests
from infinitecampus import InfiniteCampusExceptions

from infinitecampus.http_manager.http_grades import Grades
from infinitecampus.http_manager.http_calendar import Calendar
from infinitecampus.http_manager.http_student import Student

class Http():
    """Responsible for holding and performing the raw http requests to the Infinite Campus servers."""
    def __init__(self):
        self.session = requests.session()
        self.district_data = None
        self._logged_in = False
        self.last_interaction_timestamp = None

        self.grades: Grades = Grades(http=self)
        self.calendar: Calendar = Calendar(http=self)
        self.student: Student = Student(http=self)

        