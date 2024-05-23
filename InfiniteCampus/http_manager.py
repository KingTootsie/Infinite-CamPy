import requests
from infinitecampus import InfiniteCampusExceptions

class Http():
    """Responsible for performing the raw http requests to the Infinite Campus servers."""
    def __init__(self):
        self.session = requests.session()
        self.district_data = None
        self._logged_in = False
        self.last_interaction_timestamp = None

    def fetch_course_details(self, sectionID: int) -> dict:
        """Fetches categories, subcategories, and assignments from IC."""
        #https://siouxfallssd.infinitecampus.org/campus/resources/portal/grades/detail/2152106
        district_site = self.district_data["district_baseurl"]
        details = self.session.get(f"{district_site}resources/portal/grades/detail/{sectionID}").json()

        #Add checks

        return details
    
    def fetch_grades(self) -> dict:
        district_site = self.district_data["district_baseurl"]
        grades = self.session.get(f"{district_site}resources/portal/grades").json()

        return grades
    
    def fetch_calendar(self) -> dict:
        district_site = self.district_data["district_baseurl"]

        student_info_json = self.session.get(f"{district_site}api/portal/students").json()

        calendar_id = student_info_json[0]["enrollments"][0]["calendarID"]

        calendar_json = self.session.get(f"{district_site}resources/calendar/instructionalDay?calendarID={calendar_id}").json()

        is_error = "errors" in calendar_json

        if is_error is True:
            error_message = calendar_json["errors"][0]["message"]

            raise InfiniteCampusExceptions.CalendarExceptions.APIException(f"The following error message was given by the Infinite Campus API:\n {error_message}")
        
        return calendar_json