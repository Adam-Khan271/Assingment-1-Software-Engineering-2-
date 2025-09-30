from App.database import db
from datetime import datetime
import uuid

class Staff(db.Model):
    __tablename__ = 'staff'

    staff_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String, nullable=False)

    # Relationship: 1 Staff → 0..* Shortlist
    shortlists = db.relationship('Shortlist', backref='staff', lazy=True)

    def add_student_to_shortlist(self, student, shortlist):
        if student not in shortlist.students:
            shortlist.students.append(student)
            db.session.commit()
        return shortlist

    def remove_student_from_shortlist(self, student, shortlist):
        if student in shortlist.students:
            shortlist.students.remove(student)
            db.session.commit()
        return shortlist

    def view_student_applications(self, student):
        return student.applications

    def update_student_profile(self, student, **kwargs):
        for key, value in kwargs.items():
            if hasattr(student, key):
                setattr(student, key, value)
        db.session.commit()
        return student

    @classmethod
    def create(cls, staff_id, name, email, role):
        staff = cls(
            staff_id=staff_id,
            name=name,
            email=email,
            role=role
        )
        db.session.add(staff)
        db.session.commit()
        return staff

    def create_shortlist(self, notes):
        from App.models.shortlist import Shortlist
        shortlist = Shortlist(
            shortlist_id=str(uuid.uuid4()),
            date_added=datetime.utcnow(),
            notes=notes,
            staff_id=self.staff_id
        )
        db.session.add(shortlist)
        db.session.commit()
        return shortlist