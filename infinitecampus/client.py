import requests
import datetime
import time
from infinitecampus import InfiniteCampusExceptions
from infinitecampus.grades import Grades
from infinitecampus.calendar import Calendar
from infinitecampus.student import Student
from infinitecampus.http_manager import Http

#NOTE: Sessions expire after 1 hour of inactivity
class Client(object):
    def __init__(self) -> None:
        self.http: Http = Http()
        self._logged_in = False
        self.student = Student(client=self)
        self.grades = Grades(client=self)
        self.calendar = Calendar(client=self)

    def check_session_validity(self):
        """
        Called in all functions to make sure the session hasn't expired.
        """
        current_time = time.time()

        if self.http.last_interaction_timestamp is None:
            self.http.last_interaction_timestamp = current_time
            return
        
        if current_time > (self.http.last_interaction_timestamp + 3600):
            self.http.session.cookies.clear()
            self._logged_in = False
            self.http.district_data = None
            raise InfiniteCampusExceptions.AuthorizationExceptions.SessionHasExpired
        else:
            self.http.last_interaction_timestamp = current_time
    
    
    def log_in(self, username: str, password: str, district_name: str, state_abbreviation: str) -> bool:
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
        if self._logged_in == True:
            raise InfiniteCampusExceptions.LoginExceptions.UserAlreadyLoggedInError
        
        get_district = self.http.session.get(url=f"https://mobile.infinitecampus.com/api/district/searchDistrict?query={district_name}&state={state_abbreviation}").json()
        
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
        
        #Check status code?
        verify_response = self.http.session.post(url=f"{district_site}verify.jsp", headers={"User-Agent": "Infinite-Campy - v.1"}, data=data)
        
        cookie_names = []
        for cookie in self.http.session.cookies:
            cookie_names.append(cookie.name)

        #This is probably flawed, but it works.
        if "XSRF-TOKEN" not in cookie_names:
            raise InfiniteCampusExceptions.LoginExceptions.InvalidUsernameOrPassword
        else:
            self.http.district_data = district
            self._logged_in = True
            self.http.last_interaction_timestamp = time.time()
            #print("Successfully logged in.")
            return True
    
    def log_out(self) -> bool:
        if not self._logged_in:
            raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError(message="You must log in before trying to log out.")
        
        district_site = self.http.district_data["district_baseurl"]

        self.http.session.get(f"{district_site}logoff.jsp?")
        self.http.session.cookies.clear()
        self._logged_in = False
        self.http.district_data = None

        print("Successfully logged out.")
        return True

    
        
    

    