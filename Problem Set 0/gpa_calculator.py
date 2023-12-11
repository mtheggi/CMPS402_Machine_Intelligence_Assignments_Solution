from typing import List
from college import Student, Course
import utils


def calculate_gpa(student: Student, courses: List[Course]) -> float:
    '''
    This function takes a student and a list of course
    It should compute the GPA for the student
    The GPA is the sum(hours of course * grade in course) / sum(hours of course)
    The grades come in the form: 'A+', 'A' and so on.
    But you can convert the grades to points using a static method in the course class
    To know how to use the Student and Course classes, see the file "college.py"  
    '''
    # TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()
    totalhours = 0
    sGpa = 0
    for crs in courses:
        if student.id in crs.grades:
            print(crs.hours)
            totalhours += crs.hours
            sGpa += crs.hours * \
                crs.convert_grade_to_points(crs.grades[student.id])

    return (sGpa/totalhours) if totalhours else 0.0
