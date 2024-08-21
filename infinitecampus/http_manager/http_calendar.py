from typing import TYPE_CHECKING
from infinitecampus import InfiniteCampusExceptions

if TYPE_CHECKING:
    from infinitecampus.http_manager import Http

class Calendar():
    def __init__(self, http):
        self.http: Http = http

    def fetch_calendar(self) -> dict:
        district_site = self.http.district_data["district_baseurl"]

        student_info_json = self.http.session.get(f"{district_site}api/portal/students").json()

        calendar_id = student_info_json[0]["enrollments"][0]["calendarID"]

        calendar_json = self.http.session.get(f"{district_site}resources/calendar/instructionalDay?calendarID={calendar_id}").json()

        is_error = "errors" in calendar_json

        if is_error is True:
            error_message = calendar_json["errors"][0]["message"]

            raise InfiniteCampusExceptions.CalendarExceptions.APIException(f"The following error message was given by the Infinite Campus API:\n{error_message}\nPlease report this on the issues tab at https://github.com/KingTootsie/Infinite-CamPy/issues")
        
        return calendar_json
    
    def fetch_day(self, day: int, month: int, year: int):
        district_site = self.http.district_data["district_baseurl"]

        student_info_json = self.http.session.get(f"{district_site}api/portal/students").json()

        calendar_id = student_info_json[0]["enrollments"][0]["calendarID"]

        calendar_json = self.http.session.get(f"{district_site}resources/calendar/instructionalDay?calendarID={calendar_id}&date={year}-{month}-{day}").json()
        print(f"{district_site}resources/calendar/instructionalDay?calendarID={calendar_id}&date={year}-{month}-{day}")

        is_error = "errors" in calendar_json

        if is_error is True:
            error_message = calendar_json["errors"][0]["message"]

            raise InfiniteCampusExceptions.CalendarExceptions.APIException(f"The following error message was given by the Infinite Campus API:\n {error_message}")

        try:
            return calendar_json[0]
        except IndexError:
            return None
    
        