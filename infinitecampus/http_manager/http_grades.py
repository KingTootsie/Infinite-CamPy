from typing import TYPE_CHECKING
from infinitecampus import InfiniteCampusExceptions
import datetime

if TYPE_CHECKING:
    from infinitecampus.http_manager import Http

class Grades():
    def __init__(self, http):
        self.http: Http = http

    def fetch_course_details(self, sectionID: int) -> dict:
        """Fetches categories, subcategories, and assignments from IC."""
        #https://siouxfallssd.infinitecampus.org/campus/resources/portal/grades/detail/2152106
        district_site = self.http.district_data["district_baseurl"]
        details = self.http.session.get(f"{district_site}resources/portal/grades/detail/{sectionID}").json()

        #Add checks

        return details
    
    def fetch_grades(self) -> dict:
        district_site = self.http.district_data["district_baseurl"]
        grades = self.http.session.get(f"{district_site}resources/portal/grades").json()

        return grades
    
    def fetch_grade_book_updates(self):
            district_site = self.http.district_data["district_baseurl"]

            date_today = str(datetime.datetime.today().date())

            day_current = date_today[8:9]
            day_current = int(day_current)

            month = date_today[5:7]

            if month[0] == "0":
                month = month[1]
            month = int(month)

            day_past = day_current - 14

            if day_past <= 0:
                month -= 1
                day_past = 30 - abs(day_past)

            str_day = str(day_past)
            if len(str_day) == 1:
                str_day = "0" + str_day
                
            str_month = str(month)
            if len(str_month) == 1:
                str_month = "0" + str_month

            date_string = date_today[:4] + "-" + str_month + "-" + str_day
            
            recent_grades = self.http.session.get(f"{district_site}api/portal/assignment/recentlyGraded?modifiedDate={date_string}T00:00:00").json()

            return recent_grades