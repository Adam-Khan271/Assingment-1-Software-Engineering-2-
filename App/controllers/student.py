from App.models import db, Student, Application

def view_shortlisted_positions(student_id):
    student = Student.query.get(student_id)
    if not student:
        return []
    return student.view_shortlisted_positions()

def view_employer_responses(student_id):
    student = Student.query.get(student_id)
    if not student:
        return []
    return student.view_employer_response()
