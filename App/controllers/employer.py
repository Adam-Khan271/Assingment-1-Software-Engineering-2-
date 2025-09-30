from App.models import db, Employer, InternshipPosition, Application, Response

def create_internship_position(employer_id, title, description):
    employer = Employer.query.get(employer_id)
    if not employer:
        return None
    return employer.create_internship_position(title, description)

def accept_student(application_id, message):
    application = Application.query.get(application_id)
    if not application:
        return None
    application.update_status('Accepted')
    response = Response(
        message=message,
        status='Accepted',
        date_sent=db.func.current_date(),
        application_id=application_id
    )
    db.session.add(response)
    db.session.commit()
    return response

def reject_student(application_id, message):
    application = Application.query.get(application_id)
    if not application:
        return None
    application.update_status('Rejected')
    response = Response(
        message=message,
        status='Rejected',
        date_sent=db.func.current_date(),
        application_id=application_id
    )
    db.session.add(response)
    db.session.commit()
    return response
