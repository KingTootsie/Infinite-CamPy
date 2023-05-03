import requests
import datetime
import time
from . import InfiniteCampusExceptions

#NOTE: Sessions expire after 1 hour of inactivity
class InfiniteCampus(object):
    def __init__(self) -> None:
        self.session = requests.session()
        self.district_data = None
        self.logged_in = False
        self.last_interaction_timestamp = None
        self.Student = InfiniteCampus.Student(infinite_campus_self=self)
        self.Grades = InfiniteCampus.Grades(infinite_campus_self=self)
        self.Calendar = InfiniteCampus.Calendar(infinite_campus_self=self)

    def _authentication_check(self):
        """
        Called in all functions to make sure the session hasn't expired.
        Do not invoke this on your own.
        """
        current_time = time.time()

        if self.last_interaction_timestamp is None:
            self.last_interaction_timestamp = current_time
            return
        
        if current_time >= (self.last_interaction_timestamp + 3600):
            self.session.cookies.clear()
            self.logged_in = False
            self.district_data = None
            raise InfiniteCampusExceptions.AuthorizationExceptions.SessionHasExpired
        else:
            self.last_interaction_timestamp = current_time
    
    """
    Logs into a student campus portal.

    Inputs:
    - username (string): The username for the student.
    - password (string): The password for the student.
    - district_name (string): This is the name of the school district. Ex: "Central Vermont Career Center School District"
    - state_abbreviation (string): The abbreviation for the school district's state. Ex: Vermont --> VT

    Output:
    - Boolean: True if logging in was successful.

    Operations:
    - Inputs district_name and state_addreviation are used to request district information. 
    - This district info is then stored and used for all future wrapper and api operations.
    - A request is then made to log in. All cookies are stored in the session being used.
    - Then it checks if the log in was successful, and if it is, returns True.
    """
    def login(self, username: str, password: str, district_name: str, state_abbreviation: str) -> bool:
        if self.logged_in == True:
            raise InfiniteCampusExceptions.LoginExceptions.UserAlreadyLoggedInError
        
        get_district = self.session.get(url=f"https://mobile.infinitecampus.com/api/district/searchDistrict?query={district_name}&state={state_abbreviation}").json()
        
        if len(get_district["data"]) == 0:
            raise InfiniteCampusExceptions.LoginExceptions.NoDistrictFound
        
        district = get_district["data"][0]

        district_site = district["district_baseurl"]

        data = {
            "username": username,
            "password": password,
            "appName": district["district_app_name"],
            "url": "nav-wrapper",
            "lang": "en",
            "portalLoginPage": "students"
        }

        verify_response = self.session.post(url=f"{district_site}verify.jsp", data=data)
        
        cookie_names = []
        for cookie in self.session.cookies:
            cookie_names.append(cookie.name)

        #This probably is flawed
        if "XSRF-TOKEN" not in cookie_names:
            raise InfiniteCampusExceptions.LoginExceptions.InvalidUsernameOrPassword
        else:
            self.district_data = district
            self.logged_in = True
            self.last_interaction_timestamp = time.time()
            print("Successfully logged in.")
            return True
    
    def logout(self):
        if not self.logged_in:
            raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError(message="You must log in before trying to log out.")
        
        district_site = self.district_data["district_baseurl"]

        self.session.get(f"{district_site}logoff.jsp?")
        self.session.cookies.clear()
        self.logged_in = False
        self.district_data = None

        print("Successfully logged out.")
        return True

    class Student():
        def __init__(self, infinite_campus_self) -> None:
            self.infinite_campus_self: InfiniteCampus = infinite_campus_self

        def fetch_student(self):
            """
            Raises:
                InfiniteCampusExceptions.LoginExceptions.NotLoggedInError: Session has not been logged into.

            Returns:
                dictionary: Returns json information on student account.
            """
            if not self.infinite_campus_self.logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
            self.infinite_campus_self._authentication_check()
            
            district_site = self.infinite_campus_self.district_data["district_baseurl"]
            student_response = self.infinite_campus_self.session.get(f"{district_site}api/portal/students")
            student_response_json = student_response.json()

            student = student_response_json[0]

            return student

        def fetch_user_account(self):
            if not self.infinite_campus_self.logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
            self.infinite_campus_self._authentication_check()
            
            district_site = self.infinite_campus_self.district_data["district_baseurl"]
            account_response = self.infinite_campus_self.session.get(f"{district_site}resources/my/userAccount")
            account_response_json = account_response.json()

            return account_response_json
            
        def fetch_attendance(self):
            if not self.infinite_campus_self.logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
            self.infinite_campus_self._authentication_check()
            
            district_site = self.infinite_campus_self.district_data["district_baseurl"]
            user_account_json = self.session.get(f"{district_site}api/portal/students").json()
            user_account = user_account_json[0]

            #I've only ever seen one enrollment. If anyone is able to experiment with more,
            #Please, let me know or make a pull request.
            enrollmentID = user_account["enrollments"][0]["enrollmentID"]

            attendance_json = self.session.get(f"{district_site}resources/portal/attendance/{enrollmentID}?courseSummary=true").json()

            return attendance_json
        
    class Grades():
        def __init__(self, infinite_campus_self) -> None:
            self.infinite_campus_self: InfiniteCampus = infinite_campus_self

        def fetch_grades(self):
            if not self.infinite_campus_self.logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
            self.infinite_campus_self._authentication_check()
            
            district_site = self.infinite_campus_self.district_data["district_baseurl"]
            grades_json_response = self.infinite_campus_self.session.get(f"{district_site}resources/portal/grades").json()

            return grades_json_response
        
        def fetch_grade_book_updates(self):
            if not self.infinite_campus_self.logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
            self.infinite_campus_self._authentication_check()
            
            district_site = self.infinite_campus_self.district_data["district_baseurl"]

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
            
            recent_grades = self.infinite_campus_self.session.get(f"{district_site}api/portal/assignment/recentlyGraded?modifiedDate={date_string}T00:00:00").json()

            return recent_grades
        
        def fetch_class(self, class_name: str, term:int):
            if not self.infinite_campus_self.logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
            self.infinite_campus_self._authentication_check()

            district_site = self.infinite_campus_self.district_data["district_baseurl"]
            grades_json_response = self.infinite_campus_self.session.get(f"{district_site}resources/portal/grades").json()
            
            classes = grades_json_response[0]["terms"][term - 1]["courses"]

            for class_json in classes:
                name = class_json["courseName"]
                if class_name in name:
                    return class_json

    class Calendar():
        def __init__(self, infinite_campus_self) -> None:
            self.infinite_campus_self: InfiniteCampus = infinite_campus_self

        def fetch_calendar(self):
            if not self.infinite_campus_self.logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
            self.infinite_campus_self._authentication_check()

            district_site = self.infinite_campus_self.district_data["district_baseurl"]

            student_info_json = self.infinite_campus_self.session.get(f"{district_site}api/portal/students").json()

            calendar_id = student_info_json[0]["enrollments"][0]["calendarID"]

            calendar_json = self.infinite_campus_self.session.get(f"{district_site}resources/calendar/instructionalDay?calendarID={calendar_id}").json()

            is_error = "errors" in calendar_json

            if is_error is True:
                error_message = calendar_json["errors"][0]["message"]

                raise InfiniteCampusExceptions.CalendarExceptions.APIException(f"The following error message was given by the Infinite Campus API:\n {error_message}")
            
            return calendar_json
        
        def fetch_day(self, date: str):
            """date is in (YYYY-MM-DD) format"""

            if not self.infinite_campus_self.logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
            self.infinite_campus_self._authentication_check()

            district_site = self.infinite_campus_self.district_data["district_baseurl"]

            student_info_json = self.infinite_campus_self.session.get(f"{district_site}api/portal/students").json()

            calendar_id = student_info_json[0]["enrollments"][0]["calendarID"]

            calendar_json = self.infinite_campus_self.session.get(f"{district_site}resources/calendar/instructionalDay?calendarID={calendar_id}&date={date}").json()

            is_error = "errors" in calendar_json

            if is_error is True:
                error_message = calendar_json["errors"][0]["message"]

                raise InfiniteCampusExceptions.CalendarExceptions.APIException(f"The following error message was given by the Infinite Campus API:\n {error_message}")

            return calendar_json