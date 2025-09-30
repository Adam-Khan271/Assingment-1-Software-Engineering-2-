

from App.database import db

# Association table for Shortlist <-> Student many-to-many
shortlist_student = db.Table('shortlist_student',
    db.Column('shortlist_id', db.String, db.ForeignKey('shortlist.shortlist_id'), primary_key=True),
    db.Column('student_id', db.String, db.ForeignKey('student.student_id'), primary_key=True)
)

class Shortlist(db.Model):
    __tablename__ = 'shortlist'

    shortlist_id = db.Column(db.String, primary_key=True)
    date_added = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)

    staff_id = db.Column(db.String, db.ForeignKey('staff.staff_id'), nullable=False)
    students = db.relationship('Student', secondary=shortlist_student, back_populates='shortlists')

    def remove_student(self, student):
        if student in self.students:
            self.students.remove(student)
            db.session.commit()