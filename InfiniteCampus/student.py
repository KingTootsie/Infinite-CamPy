from typing import TYPE_CHECKING
from infinitecampus import InfiniteCampusExceptions

if TYPE_CHECKING:
     from infinitecampus.client import Client

class Student():
    def __init__(self, client) -> None:
        self.client: Client = client

        #Fetch student info json with API calls
        #Fetch user account info

        self.first_name = None #Student First Name
        self.middle_name = None
        self.last_name = None
        self.suffix = None
        self.full_name = (self.first_name if self.first_name is not None else "") + (" " + self.middle_name if self.middle_name is not None else "") + (" " + self.last_name if self.last_name is not None else "") + (" " + self.suffix if self.suffix is not None else "")
        self.alias = None
        self.student_id = None #Student ID
        self.person_id = None
        self.email = None
        self.current_enrollments = None
        self.future_enrollments = None

    def fetch_student(self):
        """
        Raises:
            InfiniteCampusExceptions.LoginExceptions.NotLoggedInError: Session has not been logged into.

        Returns:
            dictionary: Returns json information on student account.
        """
        if not self.client._logged_in:
            raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
        
        self.client.check_session_validity()
        
        district_site = self.client.district_data["district_baseurl"]
        student_response = self.client.http.session.get(f"{district_site}api/portal/students")
        student_response_json = student_response.json()

        student = student_response_json[0]

        return student

    def fetch_user_account(self):
        if not self.client._logged_in:
            raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
        
        self.client.check_session_validity()
        
        district_site = self.client.district_data["district_baseurl"]
        account_response = self.client.http.session.get(f"{district_site}resources/my/userAccount")
        account_response_json = account_response.json()

        return account_response_json
        
    def fetch_attendance(self):
        if not self.client._logged_in:
            raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
        
        self.client.check_session_validity()
        
        district_site = self.client.district_data["district_baseurl"]
        user_account_json = self.client.http.session.get(f"{district_site}api/portal/students").json()
        user_account = user_account_json[0]

        #I've only ever seen one enrollment. If anyone is able to experiment with more,
        #Please, let me know or make a pull request.
        enrollmentID = user_account["enrollments"][0]["enrollmentID"]

        attendance_json = self.client.http.session.get(f"{district_site}resources/portal/attendance/{enrollmentID}?courseSummary=true").json()

        return attendance_json