# Infinite-CamPy
A simple python wrapper for the student end of Infinite Campus.

Example usage:

```
import infinitecampus

#Initialize a new client instance\n
ic = client.client()

#Log into a IC portal
ic.login("username", "password", "District_NAME", "STATE_ABEREVIATION")

#Get all enrolled classes.
enrollments = ic.grades.fetch_enrollments()

#Get the first enrolled school.
enrollment = enrollments[0]

#Print the school's name
print(enrollment.name)

#Print the name of the first term in the school
print(f"Course name: {enrollment.terms[0].name}")

#Go through each course in the term and print it's name and what each task has as a percent.
courses = enrollment.terms[0].courses
for course in courses:
    for task in course.tasks:
        print(f"{course.name} - {task.name} percent: {task.percent}%")
exit(0)
```
