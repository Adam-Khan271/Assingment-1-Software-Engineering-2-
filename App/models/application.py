

from App.database import db

class Application(db.Model):
    __tablename__ = 'application'

    application_id = db.Column(db.String, primary_key=True)
    status = db.Column(db.String, nullable=False)
    date_applied = db.Column(db.Date, nullable=False)

    position_id = db.Column(db.String, db.ForeignKey('internship_position.position_id'), nullable=False)
    student_id = db.Column(db.String, db.ForeignKey('student.student_id'), nullable=False)

    # Relationship: 0..* Application → 1 Response
    responses = db.relationship('Response', backref='application', lazy=True)

    def update_status(self, status):
        self.status = status
        db.session.commit()