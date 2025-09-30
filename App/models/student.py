from App.database import db
from datetime import datetime
import uuid

class Student(db.Model):
    __tablename__ = 'student'

    student_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    profile_info = db.Column(db.Text)

    # Relationships
    applications = db.relationship('Application', backref='student', lazy=True)
    shortlists = db.relationship('Shortlist', secondary='shortlist_student', back_populates='students')

    def apply_for_internship(self, position):
        from App.models.application import Application
        application = Application(
            application_id=str(uuid.uuid4()),
            status='Pending',
            date_applied=datetime.utcnow(),
            position_id=position.position_id,
            student_id=self.student_id
        )
        db.session.add(application)
        db.session.commit()
        return application

    @classmethod
    def create(cls, student_id, name, email, profile_info):
        student = cls(
            student_id=student_id,
            name=name,
            email=email,
            profile_info=profile_info
        )
        db.session.add(student)
        db.session.commit()
        return student

    def view_shortlisted_positions(self):
        return self.shortlists

    def view_employer_response(self):
        return [app.responses for app in self.applications]