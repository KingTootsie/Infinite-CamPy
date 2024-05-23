from typing import TYPE_CHECKING
import datetime, time
from infinitecampus import InfiniteCampusExceptions
#from infinitecampus import (NAME_SEARCH, COURSE_ID_SEARCH)
from infinitecampus.SchoolObjects import *

if TYPE_CHECKING:
    from .client import Client

#
class Grades():
        def __init__(self, client) -> None:
            self.client: Client = client
            #Gets called before logging in
            #Saves the most recent get_terms() call

        def get_terms(self):
            if not self.client._logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
            self.client.check_session_validity()

            grades_json = self.client.http.fetch_grades()

            terms: list[Term] = []
            #print(grades_json)
            #Terms
            for term in grades_json[0]["terms"]:
                current_term = Term(
                    term_name=term["termName"], 
                    term_id=term["termID"], 
                    start_date=term["startDate"], 
                    end_date=term["endDate"], 
                    courses=[]
                    )

                terms.append(current_term)
                #Courses
                course_list = []
                for course in term["courses"]:
                    current_course: Course = Course(
                        course_name=course["courseName"], 
                        term=current_term,
                        course_id=course["courseID"],
                        section_id=course["sectionID"],
                        teacher=course["teacherDisplay"],
                        school_name=course["schoolName"],
                        dropped=course["dropped"],
                        tasks=[],
                        room=course["roomName"]
                        )
                    course_list.append(current_course)

                    task_list = []
                    #Gets assignment info
                    tasks_json = self.client.http.fetch_course_details(sectionID=current_course.section_id)
                    #print(tasks_json)
                    for task in tasks_json["details"]:
                        percent = task.get("task").get("progressPercent")

                        current_task = Task(
                            term=current_term, 
                            course=current_course, 
                            task_name=task["task"]["taskName"], 
                            task_percent=percent,
                            points_earned=task["task"].get("progressPointsEarned"),
                            total_points=task["task"].get("progressTotalPoints"),
                            categories=[] if len(task["categories"]) > 0 else None
                            )
                        task_list.append(current_task)
                        
                        category_list = []
                        #if len(task["categories"]) > 0:
                        for category in task["categories"]:
                            current_category = Category(
                                term=current_term,
                                course=current_course,
                                task=current_task,
                                category_name=category["name"],
                                assignments=[] if len(category["assignments"]) > 0 else None,
                            )

                            category_list.append(current_category)
                            assignment_list = []
                            #TODO: IMPLEMENT THIS.
                            for assignment in category["assignments"]:
                                current_assignment = Assignment(
                                    term=current_term,
                                    course=current_course,
                                    category=current_category,
                                    assignment_name=assignment["assignmentName"],
                                    points_earned=float(assignment["score"]) if assignment["score"] is not None else None,
                                    max_points=assignment["totalPoints"],
                                    not_graded=assignment["notGraded"],
                                    late=assignment["late"],
                                    missing=assignment["missing"],
                                    cheated=assignment["cheated"],
                                    dropped=assignment["dropped"]
                                )

                                assignment_list.append(current_assignment)
                            current_category.assignments = assignment_list
                        current_task.categories = category_list
                    current_course.tasks = task_list
                current_term.courses = course_list
            return terms
        
        def get_course(self, query: str, search_type):
            terms = self.get_terms()

            #NAME_SEARCH
            if search_type == "name":
                for term in terms:
                    course = term.fetch_course(query=query, search_type="name")
                    if course is not None:
                        return course
                    else:
                        return None
            if search_type == "course_id":
                for term in terms:
                    course = term.fetch_course(query=query, search_type="course_id")
                    if course is not None:
                        return course
                    else:
                        return None
        

        def fetch_grades(self):
            if not self.client._logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
            self.client.check_session_validity()
            
            district_site = self.client.http.district_data["district_baseurl"]
            grades_json_response = self.client.http.session.get(f"{district_site}resources/portal/grades").json()

            return grades_json_response
        
        def fetch_grade_book_updates(self):
            if not self.client._logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
            self.client.check_session_validity()
            
            district_site = self.client.http.district_data["district_baseurl"]

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
            
            recent_grades = self.client.http.session.get(f"{district_site}api/portal/assignment/recentlyGraded?modifiedDate={date_string}T00:00:00").json()

            return recent_grades
        
        
        def fetch_class(self, class_name: str, term:int):
            if not self.client._logged_in:
                raise InfiniteCampusExceptions.LoginExceptions.NotLoggedInError
            
            self.client.check_session_validity()

            district_site = self.client.district_data["district_baseurl"]
            grades_json_response = self.client.session.get(f"{district_site}resources/portal/grades").json()
            
            classes = grades_json_response[0]["terms"][term - 1]["courses"]

            for class_json in classes:
                name = class_json["courseName"]
                if class_name in name:
                    return class_json