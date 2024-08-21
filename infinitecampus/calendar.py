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
        calendar_json = self.client.http.calendar.fetch_calendar()

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
        
    
    def get_day(self, day: int, month: int, year: int) -> Day | None:
        """Gets a day from the calendar.
        
        Inputs:
        - day (int): A specified day.
        - month (int): A specified month.
        - year (int): A specified year.
        
        Outputs:
        - Day: Returned if specified date is a school day.
        - None: Returned if specified date is invalid or not a school day."""
        
        if not self.client._logged_in:
            raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
        
        self.client.check_session_validity()

        day_json = self.client.http.calendar.fetch_day(day=day, month=month, year=year)
        
        if day_json is None:
            return None
        
        day = Day(
            date=day_json["date"],
            is_school_day=day_json["isSchoolDay"],
            requires_attendance=day_json["requiresAttendance"],
            day_id=day_json["dayID"],
            calendar_id=day_json["calendarID"],
            structure_id=day_json["structureID"],
            comment=day_json.get("comments")
        )

        return day

        