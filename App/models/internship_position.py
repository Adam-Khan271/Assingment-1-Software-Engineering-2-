

from App.database import db

class InternshipPosition(db.Model):
    __tablename__ = 'internship_position'

    position_id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, nullable=False, default='Open')

    employer_id = db.Column(db.String, db.ForeignKey('employer.employer_id'), nullable=False)

    # Relationship: 1 InternshipPosition → 0..* Application
    applications = db.relationship('Application', backref='position', lazy=True)

    def update_status(self, status):
        self.status = status
        db.session.commit()