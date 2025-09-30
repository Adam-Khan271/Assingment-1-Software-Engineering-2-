from App.database import db
import uuid


class Employer(db.Model):
    __tablename__ = 'employer'

    employer_id = db.Column(db.String, primary_key=True)
    company_name = db.Column(db.String, nullable=False)
    contact_info = db.Column(db.String, nullable=False)

    positions = db.relationship('InternshipPosition', backref='employer', lazy=True)

    def create_internship_position(self, title, desc):
        from App.models.internship_position import InternshipPosition
        position = InternshipPosition(title=title, description=desc, employer_id=self.employer_id)
        db.session.add(position)
        db.session.commit()
        return position

    def edit_internship_position(self, position, new_title=None, new_desc=None):
        if new_title:
            position.title = new_title
        if new_desc:
            position.description = new_desc
        db.session.commit()

    def close_internship_position(self, position):
        position.status = 'Closed'
        db.session.commit()

    def review_application(self, application):
        # Logic to review application
        pass

    def send_response(self, application, message):
        from App.models.response import Response
        response = Response(
            message=message,
            status="Sent",
            date_sent=db.func.current_date(),
            application_id=application.application_id
        )
        db.session.add(response)
        db.session.commit()
        return response

    @classmethod
    def create(cls, employer_id, company_name, contact_info):
        employer = cls(
            employer_id=employer_id,
            company_name=company_name,
            contact_info=contact_info
        )
        db.session.add(employer)
        db.session.commit()
        return employer

    def accept_student(self, application, message):
        application.status = 'Accepted'
        return self.send_response(application, message)

    def reject_student(self, application, message):
        application.status = 'Rejected'
        return self.send_response(application, message)