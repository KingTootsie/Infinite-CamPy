from typing import TYPE_CHECKING
from infinitecampus import InfiniteCampusExceptions

if TYPE_CHECKING:
    from infinitecampus.http_manager import Http

class Student():
    def __init__(self, http):
        self.http: Http = http