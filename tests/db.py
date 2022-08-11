from faker import Faker

from app.models import db, session, Patient

fake = Faker(["pt_BR"])

NUMBERS_PATIENTS = 5


def _fk_pragma_on_connect(dbapi_con, _):
    """
    Enable FK constraint in sqllite
    """
    dbapi_con.execute("PRAGMA foreign_keys = ON")


def set_up_db():
    """
    Create test database and populate
    """
    from sqlalchemy import event
    event.listen(db.engine, 'connect', _fk_pragma_on_connect)
    db.create_all()


def populate_patients(num_rows=NUMBERS_PATIENTS, created_patients=None):
    """
    Populate table patients
    """
    patients = []
    with db.session():
        for _ in range(num_rows):
            patient = Patient(**create_patient())
            db.session.add(patient)
            session.flush()
            patients.append(patient.as_json())

        if created_patients:
            for p in created_patients:
                patient = Patient(**p)
                db.session.add(patient)
                session.flush()
                patients.append(patient.as_json())

        session.commit()
    return patients


def create_patient(date_iso=False):
    """
    create a fake patient
    """
    return {
        "name":
        fake.name(),
        "cpf":
        fake.ssn(),
        "phone":
        fake.msisdn()[-10:],
        "address":
        fake.address(),
        "birthdate":
        fake.date_between().isoformat() if date_iso else fake.date_between()
    }
