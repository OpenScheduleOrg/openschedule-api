from faker import Faker
from dateutil.parser import isoparse

from db import populate_patients
from factory import PatientBuilder
from app.models import Patient, session, select

fake = Faker(["pt_BR"])


def assert_patient(result, expected, complete=True):
    """
    Assert patient
    """
    assert result["name"] == expected["name"]
    assert result["cpf"] == expected["cpf"]
    assert result["phone"] == expected["phone"]

    if complete:
        assert result["address"] == expected["address"]
        assert result["birthdate"] == expected["birthdate"]


#  POST  #


def test_should_return_201_and_the_patient_whether_request_valid_only_required(
        app, client):
    """
    Should return status 201 and patient whether the request is valid with only required fields
    """
    new_patient = PatientBuilder().build()

    res = client.post("/api/patients", json=new_patient)

    with app.app_context():
        persited_patient = session.execute(
            select(Patient).where(
                (Patient.cpf == new_patient["cpf"])
                & (Patient.phone == new_patient["phone"])
                & (Patient.name == new_patient["name"]))).scalar()
    assert persited_patient

    assert res.status_code == 201

    assert_patient(res.get_json(), new_patient, False)


def test_should_return_201_and_the_patient_whether_request_valid(app, client):
    """
    Should return status 201 and patient whether the request is valid
    """
    new_patient = PatientBuilder().complete().build()

    rs = client.post("/api/patients", json=new_patient)

    assert rs.status_code == 201

    res_json = rs.get_json()

    with app.app_context():
        persited_patient = session.execute(
            select(Patient).where(
                (Patient.cpf == new_patient["cpf"])
                & (Patient.phone == new_patient["phone"])
                & (Patient.name == new_patient["name"])
                & (Patient.address == new_patient["address"])
                & (Patient.birthdate == new_patient["birthdate"]))).scalar()
    assert persited_patient

    assert_patient(res_json, new_patient)


def test_should_return_422_whether_request_payload_is_invalid(client):
    """
    Should return status 422 whether request payload is invalid
    """
    new_patient = {}

    res = client.post("/api/patients", json=new_patient)

    assert res.status_code == 422
    res_json = res.get_json()

    assert len(res_json) == 3
    assert "name" in res_json
    assert "cpf" in res_json
    assert "phone" in res_json

    new_patient = PatientBuilder().with_name(
        fake.pystr(min_chars=1, max_chars=1)).with_cpf("not a cpf").with_phone(
            "not a phone").with_birthdate("not a date").build()

    res = client.post("/api/patients", json=new_patient)

    assert res.status_code == 422
    res_json = res.get_json()

    assert len(res_json) == 4
    assert "name" in res_json
    assert "cpf" in res_json
    assert "phone" in res_json
    assert "birthdate" in res_json

    new_patient = PatientBuilder().complete().with_name(
        fake.pystr(min_chars=256, max_chars=300)).build()

    res = client.post("/api/patients", json=new_patient)

    assert res.status_code == 422
    res_json = res.get_json()

    assert len(res_json) == 1
    assert "name" in res_json


def test_should_return_422_whether_payload_have_cpf_that_is_already_in_use(
        app, client):
    """
    Should return 422 if payload have cpf that is already in use
    """
    with app.app_context():
        patients = populate_patients()

    new_patient = PatientBuilder().with_cpf(patients[0]["cpf"]).build()

    res = client.post("/api/patients", json=new_patient)

    assert res.status_code == 422
    res_json = res.get_json()
    assert "cpf" in res_json
    assert "registered" in res_json["cpf"]


def test_should_return_422_whether_payload_have_phone_that_is_already_in_use(
        app, client):
    """
    Should return 422 if payload have phone that is already in use
    """
    with app.app_context():
        patients = populate_patients()

    new_patient = PatientBuilder().with_phone(patients[0]["phone"]).build()

    res = client.post("/api/patients", json=new_patient)

    assert res.status_code == 422
    res_json = res.get_json()
    assert "phone" in res_json
    assert "registered" in res_json["phone"]


#  POST  #

#  GET  #


def test_should_return_last_20_patients_inserted_ordered_descending_created_at(
        app, client):
    """
    Should return status 200 and the last 20 patients inserteds ordered descending created_at
    """
    with app.app_context():
        patients = populate_patients(100)
    patients = sorted(patients, key=lambda d: d["created_at"], reverse=True)

    res = client.get("/api/patients")

    assert res.status_code == 200

    res_patients = res.get_json()
    assert len(res_patients) == 20
    assert patients[0]["id"] == res_patients[0]["id"]

    for i in range(1, len(res_patients)):
        assert isoparse(res_patients[i - 1]["created_at"]) > isoparse(
            res_patients[i]["created_at"])


def test_should_return_n_patients_ordered_by_created_at_desceding(app, client):
    """
    Should return status 200 and n patients ordered by created at descending
    """
    with app.app_context():
        patients = populate_patients(100)
    patients = sorted(patients, key=lambda d: d["created_at"], reverse=True)

    limit = 5
    res = client.get(f"/api/patients?limit={limit}")

    assert res.status_code == 200

    res_patients = res.get_json()
    assert len(res_patients) == limit
    assert patients[0]["id"] == res_patients[0]["id"]


def test_should_return_diferent_patients_with_page_change_ordered_by_create_at_descending(
        app, client):
    """
    Should return status 200 diferente patients with page change ordered by created at desceding
    """
    with app.app_context():
        patients = populate_patients(100)
    patients = sorted(patients, key=lambda d: d["created_at"], reverse=True)

    page = 1
    res = client.get(f"/api/patients?page={page}")
    page1_patients = res.get_json()

    page = 2
    res = client.get(f"/api/patients?page={page}")
    page2_patients = res.get_json()

    assert len(page2_patients) == 20
    assert patients[20]["id"] == page2_patients[0]["id"]

    for i in range(1, len(page2_patients)):
        assert isoparse(page2_patients[i - 1]["created_at"]) > isoparse(
            page2_patients[i]["created_at"])
        for p in page1_patients:
            assert page2_patients[i]["id"] != p["id"]


def test_should_return_should_return_first_n_patients_match_filter_name_ordered_by_created_at(
        app, client):
    """
    Should return status 200 and first n patietns that match with filter name ordered by created at
    """
    filter_name = "foo"
    with app.app_context():
        created_patients = []
        for i in range(30):
            patient = PatientBuilder().complete().with_name(
                f"{fake.first_name()} {filter_name} {fake.last_name()}"
            ).build_object()
            created_patients.append(patient)

        patients = populate_patients(100, created_patients)

    patients = sorted(patients, key=lambda d: d["created_at"], reverse=True)

    res = client.get(f"/api/patients?name={filter_name}")

    assert res.status_code == 200

    res_patients = res.get_json()
    assert len(res_patients) == 20

    for i in range(1, len(res_patients)):
        assert isoparse(res_patients[i - 1]["created_at"]) > isoparse(
            res_patients[i]["created_at"])
        assert filter_name in res_patients[i]["name"]

    res = client.get(f"/api/patients?name={filter_name}&page=2")

    res_patients = res.get_json()

    assert 10 == len(res_patients)
    for p in res_patients:
        assert filter_name in p["name"]


def test_should_return_200_and_patient_get_patient_by_id(app, client):
    """
    Should return status 200 and patient get patient by id
    """
    with app.app_context():
        patients = populate_patients()

    patient = patients[0]
    patient_id = patient["id"]

    res = client.get(f"/api/patients/{patient_id}")

    assert res.status_code == 200

    assert_patient(res.get_json(), patient)


def test_should_return_200_and_patient_get_patient_by_cpf(app, client):
    """
    Should return status 200 and patient get patient by cpf
    """
    with app.app_context():
        patients = populate_patients()

    patient = patients[0]
    patient_cpf = patient["cpf"]

    res = client.get(f"/api/patients/{patient_cpf}/cpf")

    assert res.status_code == 200

    assert_patient(res.get_json(), patient)


def test_should_return_200_and_patient_get_patient_by_phone(app, client):
    """
    Should return status 200 and patient get patient by phone
    """
    with app.app_context():
        patients = populate_patients()

    patient = patients[0]
    patient_phone = patient["phone"]

    res = client.get(f"/api/patients/{patient_phone}/phone")

    assert res.status_code == 200

    assert_patient(res.get_json(), patient)


def test_should_return_404_if_patient_not_exists_on_get_patient(client):
    """
    Should return status 404 if patient not exists on get patient
    """
    endpoints = [
        "/api/patients/0", "/api/patients/11111111111/cpf",
        "/api/patients/9999999999/phone"
    ]
    for ept in endpoints:
        res = client.get(ept)

        assert res.status_code == 404
        res_json = res.get_json()
        assert "message" in res_json


#  GET  #

#  PUT  #


def test_should_return_200_when_patient_is_updated_with_valid_data(
        app, client):
    """
    Should return status 200 when patient is udpated with valid data
    """
    with app.app_context():
        patients = populate_patients()
    patient_id = patients[0]["id"]
    update_patient = PatientBuilder().complete().build()

    res = client.put(f"/api/patients/{patient_id}", json=update_patient)

    with app.app_context():
        persited_patient = session.execute(
            select(Patient).where(
                (Patient.id == patient_id)
                & (Patient.cpf == update_patient["cpf"])
                & (Patient.phone == update_patient["phone"])
                & (Patient.name == update_patient["name"])
                & (Patient.address == update_patient["address"])
                &
                (Patient.birthdate == update_patient["birthdate"]))).scalar()
    assert persited_patient

    assert res.status_code == 200

    assert_patient(res.get_json(), update_patient)


def test_should_return_404_if_patient_to_update_not_exists(app, client):
    """
    Should return status 404 if patient to update not exists
    """
    with app.app_context():
        populate_patients()

    update_patient = PatientBuilder().complete().build()

    res = client.put(f"/api/patients/{0}", json=update_patient)

    assert res.status_code == 404
    res_json = res.get_json()
    assert "message" in res_json


def test_should_return_422_whether_request_payload_is_invalid_on_update_patient(
        client):
    """
    Should return status 422 whether request payload is invalid on update patient
    """
    new_patient = {}

    res = client.put("/api/patients/0", json=new_patient)

    assert res.status_code == 422
    res_json = res.get_json()

    assert len(res_json) == 3
    assert "name" in res_json
    assert "cpf" in res_json
    assert "phone" in res_json

    new_patient = PatientBuilder().with_name(
        fake.pystr(min_chars=1, max_chars=1)).with_cpf("not a cpf").with_phone(
            "not a phone").with_birthdate("not a date").build()

    res = client.put("/api/patients/0", json=new_patient)

    assert res.status_code == 422
    res_json = res.get_json()

    assert len(res_json) == 4
    assert "name" in res_json
    assert "cpf" in res_json
    assert "phone" in res_json
    assert "birthdate" in res_json

    new_patient = PatientBuilder().complete().with_name(
        fake.pystr(min_chars=256, max_chars=300)).build()

    res = client.put("/api/patients/0", json=new_patient)

    assert res.status_code == 422
    res_json = res.get_json()

    assert len(res_json) == 1
    assert "name" in res_json


def test_should_return_422_whether_payload_have_cpf_that_is_already_in_use_on_update_patient(
        app, client):
    """
    Should return 422 if payload have cpf that is already in use on update patient
    """
    with app.app_context():
        patients = populate_patients()

    patient_id = patients[0]["id"]
    new_patient = PatientBuilder().with_cpf(patients[1]["cpf"]).build()

    res = client.put(f"/api/patients/{patient_id}", json=new_patient)

    assert res.status_code == 422
    res_json = res.get_json()
    assert "cpf" in res_json
    assert "registered" in res_json["cpf"]


def test_should_return_422_whether_payload_have_phone_that_is_already_in_use_on_update_patient(
        app, client):
    """
    Should return 422 if payload have phone that is already in use
    """
    with app.app_context():
        patients = populate_patients()

    patient_id = patients[0]["id"]
    new_patient = PatientBuilder().with_phone(patients[1]["phone"]).build()

    res = client.put(f"/api/patients/{patient_id}", json=new_patient)

    assert res.status_code == 422
    res_json = res.get_json()
    assert "phone" in res_json
    assert "registered" in res_json["phone"]


#  PUT  #

#  DELETE  #


def test_should_return_204_when_delete_patient_if_exists_or_not(client, app):
    """
    Should return 204 when delete patient with him existing or not
    """
    with app.app_context():
        patients = populate_patients()

    patient = patients[0]
    res = client.delete("/api/patients/" + str(patient["id"]))
    assert res.status_code == 204

    with app.app_context():
        persited_patient = session.get(Patient, patient["id"])
    assert not persited_patient

    res = client.delete("/api/patients/9999")
    assert res.status_code == 204


#  DELETE  #


def test_should_return_422_when_request_have_useless_parameters(client):
    """
    Should return 422 when request have useless parameters
    """
    useless_atribute = "useless_atribute"
    useless_data = "useless data"
    useless_payload = {useless_atribute: useless_data}

    def assert_useless(res):
        """
        Reussable assert
        """
        res_json = res.get_json()
        assert res.status_code == 422
        assert "detail" in res_json
        assert useless_atribute in res_json["detail"]
        assert res_json["detail"][useless_atribute] == "useless"

    res = client.post("/api/patients", json=useless_payload)
    assert_useless(res)

    res = client.put("/api/patients/123", json=useless_payload)
    assert_useless(res)

    res = client.get("/api/patients", query_string=useless_payload)
    assert_useless(res)
