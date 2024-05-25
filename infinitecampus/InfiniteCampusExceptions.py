import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class LoginExceptions:
    class NotLoggedInError(Exception):
        def __init__(self, message = "User has not logged in.", *args: object) -> None:
            super().__init__(message, *args)
            self.message = message

    class UserAlreadyLoggedInError(Exception):
        def __init__(self, message = "A user has already been logged into on this instance.", *args: object) -> None:
            super().__init__(message, *args)
            self.message = message
            
    class InvalidUsernameOrPassword(Exception):
        def __init__(self, message = "Incorrect username or password provided.", *args: object) -> None:
            super().__init__(message, *args)
            self.message = message

    class NoDistrictFound(Exception):
        def __init__(self, message = "No district was found with queries provided.", *args: object) -> None:
            super().__init__(message, *args)
            self.message = message

    class InvalidState(Exception):
        def __init__(self, message = "Provided state is invalid.", *args: object) -> None:
            super().__init__(message, *args)
            self.message = message

class AuthorizationExceptions:
    class SessionHasExpired(Exception):
        def __init__(self, message = "This session has expired because it has gone 1 hour without activity.", *args: object) -> None:
            super().__init__(message, *args)
            self.message = message

class CalendarExceptions:
    class APIException(Exception):
        def __init__(self, message, *args: object) -> None:
            super().__init__(message, *args)
            self.message = message

class SearchExceptions:
    class CourseIDMustBeInteger(Exception):
        def __init__(self, message = "Non-numerical characters included in query string.", *args: object) -> None:
            super().__init__(message, *args)
            self.message = message