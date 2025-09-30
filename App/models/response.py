from App.database import db
from datetime import datetime

class Response(db.Model):
    __tablename__ = 'response'

    response_id = db.Column(db.String, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, nullable=False)  # Accepted/Rejected
    date_sent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    application_id = db.Column(db.String, db.ForeignKey('application.application_id'), nullable=False)

    def view_response(self):
        return self.message