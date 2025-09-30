import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Student, Employer, Staff, InternshipPosition, Application, Shortlist
from App.main import create_app
from App.controllers import (
    create_user, get_all_users_json, get_all_users, initialize,
    create_internship_position, accept_student, reject_student,
    add_student_to_shortlist, create_shortlist,
    view_shortlisted_positions, view_employer_responses
)

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database initialized')

'''
User Commands
'''
user_cli = AppGroup('user', help='User object commands') 

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)

'''
Student Commands
'''
student_cli = AppGroup('student', help='Student object commands')

@student_cli.command("create_student", help="Creates a student")
@click.argument("student_id")
@click.argument("name")
@click.argument("email")
@click.argument("profile_info", default="")
def create_student_command(student_id, name, email, profile_info):
    student = Student.create(
        student_id=student_id,
        name=name,
        email=email,
        profile_info=profile_info
    )
    if student:
        print(f'Student {name} (ID: {student_id}) created!')
    else:
        print('Failed to create student')

@student_cli.command("view_shortlists", help="View shortlisted positions for a student")
@click.argument("student_id")
def view_shortlists_command(student_id):
    shortlists = view_shortlisted_positions(student_id)
    if not shortlists:
        print(f'No shortlists found for student {student_id}')
    else:
        print(f'Shortlists for student {student_id}:')
        for shortlist in shortlists:
            print(f'  - Shortlist ID: {shortlist.shortlist_id}, Notes: {shortlist.notes}, Date: {shortlist.date_added}')

@student_cli.command("view_responses", help="View employer responses for a student")
@click.argument("student_id")
def view_responses_command(student_id):
    responses = view_employer_responses(student_id)
    if not responses or all(not r for r in responses):
        print(f'No responses found for student {student_id}')
    else:
        print(f'Responses for student {student_id}:')
        for app_responses in responses:
            for response in app_responses:
                print(f'  - Response ID: {response.response_id}')
                print(f'    Status: {response.status}')
                print(f'    Message: {response.message}')
                print(f'    Date: {response.date_sent}')

@student_cli.command("list", help="List all students")
def list_students_command():
    students = Student.query.all()
    if not students:
        print('No students found')
    else:
        print('All students:')
        for student in students:
            print(f'  - ID: {student.student_id}, Name: {student.name}, Email: {student.email}')

app.cli.add_command(student_cli)

'''
Employer Commands
'''
employer_cli = AppGroup('employer', help='Employer object commands')

@employer_cli.command("create_employer", help="Creates an employer")
@click.argument("employer_id")
@click.argument("company_name")
@click.argument("contact_info")
def create_employer_command(employer_id, company_name, contact_info):
    employer = Employer.create(
        employer_id=employer_id,
        company_name=company_name,
        contact_info=contact_info
    )
    if employer:
        print(f'Employer {company_name} (ID: {employer_id}) created!')
    else:
        print('Failed to create employer')

@employer_cli.command("create_position", help="Create an internship position")
@click.argument("employer_id")
@click.argument("title")
@click.argument("description")
def create_position_command(employer_id, title, description):
    position = create_internship_position(employer_id, title, description)
    if position:
        print(f'Position "{title}" created with ID: {position.position_id}')
    else:
        print('Failed to create position. Employer not found.')

@employer_cli.command("accept_student", help="Accept a student application")
@click.argument("application_id")
@click.argument("message")
def accept_student_command(application_id, message):
    response = accept_student(application_id, message)
    if response:
        print(f'Student accepted! Response ID: {response.response_id}')
    else:
        print('Failed to accept student. Application not found.')

@employer_cli.command("reject_student", help="Reject a student application")
@click.argument("application_id")
@click.argument("message")
def reject_student_command(application_id, message):
    response = reject_student(application_id, message)
    if response:
        print(f'Student rejected. Response ID: {response.response_id}')
    else:
        print('Failed to reject student. Application not found.')

@employer_cli.command("list", help="List all employers")
def list_employers_command():
    employers = Employer.query.all()
    if not employers:
        print('No employers found')
    else:
        print('All employers:')
        for employer in employers:
            print(f'  - ID: {employer.employer_id}, Company: {employer.company_name}, Contact: {employer.contact_info}')

@employer_cli.command("list_positions", help="List positions for an employer")
@click.argument("employer_id")
def list_positions_command(employer_id):
    employer = Employer.query.get(employer_id)
    if not employer:
        print(f'Employer {employer_id} not found')
    elif not employer.positions:
        print(f'No positions found for employer {employer_id}')
    else:
        print(f'Positions for {employer.company_name}:')
        for position in employer.positions:
            print(f'  - ID: {position.position_id}, Title: {position.title}, Status: {position.status}')

app.cli.add_command(employer_cli)

'''
Staff Commands
'''
staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("create_staff", help="Creates a staff member")
@click.argument("staff_id")
@click.argument("name")
@click.argument("email")
@click.argument("role")
def create_staff_command(staff_id, name, email, role):
    staff = Staff.create(
        staff_id=staff_id,
        name=name,
        email=email,
        role=role
    )
    if staff:
        print(f'Staff {name} (ID: {staff_id}) created!')
    else:
        print('Failed to create staff')

@staff_cli.command("create_shortlist", help="Create a shortlist")
@click.argument("staff_id")
@click.argument("notes", default="")
def create_shortlist_command(staff_id, notes):
    shortlist = create_shortlist(staff_id, notes)
    if shortlist:
        print(f'Shortlist created with ID: {shortlist.shortlist_id}')
    else:
        print('Failed to create shortlist')

@staff_cli.command("add_to_shortlist", help="Add a student to a shortlist")
@click.argument("staff_id")
@click.argument("student_id")
@click.argument("shortlist_id")
def add_to_shortlist_command(staff_id, student_id, shortlist_id):
    shortlist = add_student_to_shortlist(staff_id, student_id, shortlist_id)
    if shortlist:
        print(f'Student {student_id} added to shortlist {shortlist_id}')
    else:
        print('Failed to add student to shortlist. Check IDs.')

@staff_cli.command("remove_from_shortlist", help="Remove a student from a shortlist")
@click.argument("staff_id")
@click.argument("student_id")
@click.argument("shortlist_id")
def remove_from_shortlist_command(staff_id, student_id, shortlist_id):
    staff = Staff.query.get(staff_id)
    student = Student.query.get(student_id)
    shortlist = Shortlist.query.get(shortlist_id)
    
    if not (staff and student and shortlist):
        print('Failed to remove student. Check IDs.')
        return
    
    result = staff.remove_student_from_shortlist(student, shortlist)
    if result:
        print(f'Student {student_id} removed from shortlist {shortlist_id}')
    else:
        print('Failed to remove student from shortlist')

@staff_cli.command("update_student_profile", help="Update a student profile")
@click.argument("staff_id")
@click.argument("student_id")
@click.argument("field")
@click.argument("value")
def update_student_profile_command(staff_id, student_id, field, value):
    staff = Staff.query.get(staff_id)
    student = Student.query.get(student_id)
    
    if not staff or not student:
        print('Staff or student not found')
        return
    
    kwargs = {field: value}
    updated_student = staff.update_student_profile(student, **kwargs)
    if updated_student:
        print(f'Student {student_id} profile updated: {field} = {value}')
    else:
        print('Failed to update student profile')

@staff_cli.command("list", help="List all staff members")
def list_staff_command():
    staff_members = Staff.query.all()
    if not staff_members:
        print('No staff members found')
    else:
        print('All staff members:')
        for staff in staff_members:
            print(f'  - ID: {staff.staff_id}, Name: {staff.name}, Email: {staff.email}, Role: {staff.role}')

app.cli.add_command(staff_cli)

'''
Application Commands
'''
application_cli = AppGroup('application', help='Application object commands')

@application_cli.command("apply", help="Student applies for a position")
@click.argument("student_id")
@click.argument("position_id")
def apply_command(student_id, position_id):
    student = Student.query.get(student_id)
    position = InternshipPosition.query.get(position_id)
    
    if not student:
        print(f'Student {student_id} not found')
        return
    if not position:
        print(f'Position {position_id} not found')
        return
    
    application = student.apply_for_internship(position)
    if application:
        print(f'Application submitted! Application ID: {application.application_id}')
    else:
        print('Failed to submit application')

@application_cli.command("list", help="List all applications")
@click.argument("student_id", required=False)
def list_applications_command(student_id):
    if student_id:
        student = Student.query.get(student_id)
        if not student:
            print(f'Student {student_id} not found')
            return
        applications = student.applications
        print(f'Applications for student {student_id}:')
    else:
        applications = Application.query.all()
        print('All applications:')
    
    if not applications:
        print('No applications found')
    else:
        for app in applications:
            print(f'  - Application ID: {app.application_id}')
            print(f'    Student: {app.student_id}')
            print(f'    Position: {app.position_id}')
            print(f'    Status: {app.status}')
            print(f'    Date Applied: {app.date_applied}')
            print()

app.cli.add_command(application_cli)

'''
Position Commands
'''
position_cli = AppGroup('position', help='Position object commands')

@position_cli.command("list", help="List all positions")
def list_positions_command():
    positions = InternshipPosition.query.all()
    if not positions:
        print('No positions found')
    else:
        print('All positions:')
        for position in positions:
            print(f'  - ID: {position.position_id}')
            print(f'    Title: {position.title}')
            print(f'    Employer: {position.employer_id}')
            print(f'    Status: {position.status}')
            print(f'    Description: {position.description[:50]}...')
            print()

app.cli.add_command(position_cli)

'''
Test Commands
'''
test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)