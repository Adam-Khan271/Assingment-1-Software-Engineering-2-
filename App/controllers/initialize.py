import os
import csv
from App.database import db
from App.models.student import Student
from App.models.employer import Employer
from App.models.staff import Staff
from App.models.application import Application


def load_from_csv(csv_path=None):
    if not csv_path:
        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'instance', 'dummy_data.csv')

    if not os.path.exists(csv_path):
        return False

    records = {'students': [], 'employers': [], 'staff': [], 'applications': []}

    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['type'].startswith('#'):
                continue

            if row['type'] == 'student':
                student = Student.create(
                    student_id=row['id'],
                    name=row['name'],
                    email=row['email'],
                    profile_info=row['extra']
                )
                records['students'].append(student)

            elif row['type'] == 'employer':
                employer = Employer.create(
                    employer_id=row['id'],
                    company_name=row['name'],
                    contact_info=row['email']
                )
                records['employers'].append(employer)

            elif row['type'] == 'staff':
                staff = Staff.create(
                    staff_id=row['id'],
                    name=row['name'],
                    email=row['email'],
                    role=row['extra']
                )
                records['staff'].append(staff)

            elif row['type'] == 'applicant':
                # Parse position ID from extra field
                position_id = row['extra'].split(':')[1]
                student = Student.query.get(row['id'])
                if student:
                    application = student.apply_for_internship(position_id)
                    records['applications'].append(application)

    return records


def initialize(csv_path=None):
    db.drop_all()
    db.create_all()
    return load_from_csv(csv_path)
