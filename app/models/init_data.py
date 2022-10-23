from flask import Flask
from passlib.hash import pbkdf2_sha256

from . import User, Clinic


def set_up_data(db, app: Flask):
    """
    Set up data with necessary initial data
    """
    with app.app_context():
        clinic_id = db.session.query(Clinic.id).scalar()

        if clinic_id is None:
            clinic = Clinic(name="Clinic Name",
                            cnpj="99999999999999",
                            phone="9999999999",
                            address="Rua, NU, Bairro\nCEP\nCidade - UF")
            db.session.add(clinic)
            db.session.commit()
            db.session.refresh(clinic)
            clinic_id = clinic.id

        user_id = db.session.query(User.id).scalar()
        if user_id is None:
            user = User(name="Admin",
                        username="admin",
                        email="admin@consuchat.com",
                        password=pbkdf2_sha256.hash("admin"),
                        clinic_id=clinic_id)
            db.session.add(user)
            db.session.commit()
