# Infinite-CamPy
A simple python wrapper for the student end of Infinite Campus.

How to use:

`
#Initialize a new client instance
ic = client.client()

#Log into a IC portal
ic.login("username", "password", "Vermont", "VT")

grades = ic.Grades.fetch_grades()

print(grades)
`
