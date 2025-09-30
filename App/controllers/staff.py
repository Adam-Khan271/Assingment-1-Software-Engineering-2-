
from App.models import db, Staff, Shortlist, Student
from datetime import date
import uuid

def add_student_to_shortlist(staff_id, student_id, shortlist_id):
    """
    Add a student to a shortlist by staff.
    Returns the shortlist if successful, None otherwise.
    """
    staff = Staff.query.get(staff_id)
    student = Student.query.get(student_id)
    shortlist = Shortlist.query.get(shortlist_id)
    if not (staff and student and shortlist):
        return None
    return staff.add_student_to_shortlist(student, shortlist)

def create_shortlist(staff_id, notes=None):
    """
    Create a new shortlist for a staff member.
    Returns the created shortlist.
    """
    shortlist = Shortlist(
        shortlist_id=str(uuid.uuid4()),
        date_added=date.today(),
        notes=notes,
        staff_id=staff_id
    )
    db.session.add(shortlist)
    db.session.commit()
    return shortlist
