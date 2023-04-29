import requests
import login
import datetime
import InfiniteCampusExceptions

class InfiniteCampus():
    def __init__(self) -> None:
        self.session = requests.session()
        self.district_data = None
        self.logged_in = False
        self.Student = InfiniteCampus.Student(infinite_campus_self=self)
        self.Grades = InfiniteCampus.Grades(infinite_campus_self=self)
        self.Calendar = InfiniteCampus.Calendar(infinite_campus_self=self)
    
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

        def fetch_self(self):
            if not self.infinite_campus_self.logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
            district_site = self.infinite_campus_self.district_data["district_baseurl"]
            student_response = self.infinite_campus_self.session.get(f"{district_site}api/portal/students")
            student_response_json = student_response.json()

            student = student_response_json[0]

            return student


        def fetch_user_account(self):
            if not self.infinite_campus_self.logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
            district_site = self.infinite_campus_self.district_data["district_baseurl"]
            account_response = self.infinite_campus_self.session.get(f"{district_site}resources/my/userAccount")
            account_response_json = account_response.json()
            return account_response_json
            
        def fetch_email(self):
            if not self.infinite_campus_self.logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
        
        def fetch_today(self):
            if not self.infinite_campus_self.logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
        
    class Grades():
        def __init__(self, infinite_campus_self) -> None:
            self.infinite_campus_self: InfiniteCampus = infinite_campus_self

        def fetch_grades(self):
            if not self.infinite_campus_self.logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
            district_site = self.infinite_campus_self.district_data["district_baseurl"]
            grades_json_response = self.infinite_campus_self.session.get(f"{district_site}resources/portal/grades").json()

            
            return grades_json_response
        
        def fetch_grade_book_updates(self):
            if not self.infinite_campus_self.logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
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

    class Calendar():
        def __init__(self, infinite_campus_self) -> None:
            self.infinite_campus_self: InfiniteCampus = infinite_campus_self

        def fetch_calendar(self):
            if not self.infinite_campus_self.logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError

            calendar_json = self.infinite_campus_self.session.get("https://siouxfallssd.infinitecampus.org/campus/resources/calendar/instructionalDay?calendarID=2137").json()

            return calendar_json
        

        