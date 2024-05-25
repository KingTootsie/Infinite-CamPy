from typing import TYPE_CHECKING
from infinitecampus import InfiniteCampusExceptions
from infinitecampus.schoolObjects.calendarObjects.day import Day

if TYPE_CHECKING:
    from .client import Client

class Calendar():
    def __init__(self, client) -> None:
        self.client: Client = client
    
    def get_calendar(self) -> list[Day]:
        if not self.client._logged_in:
            raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
        
        self.client.check_session_validity()

        #Might need to move the exception checks to here.
        calendar_json = self.client.http.fetch_calendar()

        day_list = []
        for day_json in calendar_json:
            day_list.append(
                Day(
                    date=day_json["date"],
                    is_school_day=day_json["isSchoolDay"],
                    requires_attendance=day_json["requiresAttendance"],
                    day_id=day_json["dayID"],
                    calendar_id=day_json["calendarID"],
                    structure_id=day_json["structureID"],
                    comment=day_json.get("comments")
                )
            )

        return day_list
        
    
    def fetch_day(self, date: str):
        """date is in (YYYY-MM-DD) format"""

        if not self.client._logged_in:
            raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
        
        self.client.check_session_validity()

        district_site = self.client.district_data["district_baseurl"]

        student_info_json = self.client.session.get(f"{district_site}api/portal/students").json()

        calendar_id = student_info_json[0]["enrollments"][0]["calendarID"]

        calendar_json = self.client.session.get(f"{district_site}resources/calendar/instructionalDay?calendarID={calendar_id}&date={date}").json()

        is_error = "errors" in calendar_json

        if is_error is True:
            error_message = calendar_json["errors"][0]["message"]

            raise InfiniteCampusExceptions.CalendarExceptions.APIException(f"The following error message was given by the Infinite Campus API:\n {error_message}")

        return calendar_json