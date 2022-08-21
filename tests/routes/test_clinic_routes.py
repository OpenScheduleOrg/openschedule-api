from faker import Faker
from dateutil.parser import isoparse

from db import populate_clinics
from factory import ClinicBuilder
from app.models import Clinic, session, select, ClinicType

fake = Faker(["pt_BR"])


def assert_clinic(result, expected, complete=True):
    """
    Assert clinic
    """
    assert result["name"] == expected["name"]
    assert result["cnpj"] == expected["cnpj"]
    assert result["phone"] == expected["phone"]
    assert result["type"] == expected["type"].value
    assert result["address"] == expected["address"]

    if complete:
        assert result["latitude"] == expected["latitude"]
        assert result["longitude"] == expected["longitude"]


#  POST  #


def test_should_return_201_and_the_clinic_whether_request_valid_only_required(
        app, client):
    """
    Should return status 201 and clinic whether the request is valid with only required fields
    """
    new_clinic = ClinicBuilder().build()

    res = client.post("/api/clinics", json=new_clinic)

    assert res.status_code == 201

    with app.app_context():
        persited_clinic = session.execute(
            select(Clinic).where(
                (Clinic.cnpj == new_clinic["cnpj"])
                & (Clinic.phone == new_clinic["phone"])
                & (Clinic.name == new_clinic["name"]))).scalar()
    assert persited_clinic

    res_json = res.get_json()
    assert "clinic" in res_json
    res_clinic = res_json["clinic"]

    assert_clinic(res_clinic, new_clinic, False)


def test_should_return_201_and_the_clinic_whether_request_valid(app, client):
    """
    Should return status 201 and clinic whether the request is valid
    """
    new_clinic = ClinicBuilder().complete().build()

    rs = client.post("/api/clinics", json=new_clinic)

    assert rs.status_code == 201

    res_json = rs.get_json()

    with app.app_context():
        persited_clinic = session.execute(
            select(Clinic).where(
                (Clinic.cnpj == new_clinic["cnpj"])
                & (Clinic.phone == new_clinic["phone"])
                & (Clinic.name == new_clinic["name"])
                & (Clinic.type == new_clinic["type"])
                & (Clinic.address == new_clinic["address"])
                & (Clinic.latitude == new_clinic["latitude"])
                & (Clinic.longitude == new_clinic["longitude"]))).scalar()
    assert persited_clinic

    assert "clinic" in res_json
    res_clinic = res_json["clinic"]

    assert_clinic(res_clinic, new_clinic)


def test_should_return_400_whether_request_payload_is_invalid(client):
    """
    Should return status 400 whether request payload is invalid
    """
    new_clinic = {}

    res = client.post("/api/clinics", json=new_clinic)

    assert res.status_code == 400
    res_json = res.get_json()

    assert len(res_json) == 5
    assert "name" in res_json
    assert "cnpj" in res_json
    assert "phone" in res_json
    assert "type" in res_json

    new_clinic = ClinicBuilder().with_name(fake.pystr(
        min_chars=1, max_chars=1)).with_cnpj("not a cnpj").with_phone(
            "not a phone number").with_latitude(-91).with_longitude(
                181).with_type(0).build()

    res = client.post("/api/clinics", json=new_clinic)

    assert res.status_code == 400
    res_json = res.get_json()

    assert len(res_json) == 6
    assert "name" in res_json
    assert "cnpj" in res_json
    assert "phone" in res_json
    assert "type" in res_json
    assert "latitude" in res_json
    assert "longitude" in res_json

    new_clinic = ClinicBuilder().complete().with_name(
        fake.pystr(min_chars=256, max_chars=300)).with_latitude(
            "not a number").with_longitude("not a number").build()

    res = client.post("/api/clinics", json=new_clinic)

    assert res.status_code == 400
    res_json = res.get_json()

    assert len(res_json) == 3
    assert "name" in res_json
    assert "latitude" in res_json
    assert "longitude" in res_json


def test_should_return_400_whether_payload_have_cnpj_that_is_already_in_use(
        app, client):
    """
    Should return 400 if payload have cnpj that is already in use
    """
    with app.app_context():
        clinics = populate_clinics()

    new_clinic = ClinicBuilder().with_cnpj(clinics[0]["cnpj"]).build()

    res = client.post("/api/clinics", json=new_clinic)

    assert res.status_code == 400
    res_json = res.get_json()
    assert "cnpj" in res_json
    assert "registered" in res_json["cnpj"]


def test_should_return_400_whether_payload_have_phone_that_is_already_in_use(
        app, client):
    """
    Should return 400 if payload have phone that is already in use
    """
    with app.app_context():
        clinics = populate_clinics()

    new_clinic = ClinicBuilder().with_phone(clinics[0]["phone"]).build()

    res = client.post("/api/clinics", json=new_clinic)

    assert res.status_code == 400
    res_json = res.get_json()
    assert "phone" in res_json
    assert "registered" in res_json["phone"]


#  POST  #

#  GET  #


def test_should_return_last_20_clinics_inserted_ordered_descending_created_at(
        app, client):
    """
    Should return status 200 and the last 20 clinics inserteds ordered descending created_at
    """
    with app.app_context():
        clinics = populate_clinics(100)
    clinics = sorted(clinics, key=lambda d: d["created_at"], reverse=True)

    res = client.get("/api/clinics")

    assert res.status_code == 200

    res_clinics = res.get_json()
    assert len(res_clinics) == 20
    assert clinics[0]["id"] == res_clinics[0]["id"]

    for i in range(1, len(res_clinics)):
        assert isoparse(res_clinics[i - 1]["created_at"]) > isoparse(
            res_clinics[i]["created_at"])


def test_should_return_n_clinics_ordered_by_created_at_desceding(app, client):
    """
    Should return status 200 and n clinics ordered by created at descending
    """
    with app.app_context():
        clinics = populate_clinics(100)
    clinics = sorted(clinics, key=lambda d: d["created_at"], reverse=True)

    limit = 5
    res = client.get(f"/api/clinics?limit={limit}")

    assert res.status_code == 200

    res_clinics = res.get_json()
    assert len(res_clinics) == limit
    assert clinics[0]["id"] == res_clinics[0]["id"]


def test_should_return_diferent_clinics_with_page_change_ordered_by_create_at_descending(
        app, client):
    """
    Should return status 200 and different clinics with page change ordered by created at desceding
    """
    with app.app_context():
        clinics = populate_clinics(100)
    clinics = sorted(clinics, key=lambda d: d["created_at"], reverse=True)

    page = 1
    res = client.get(f"/api/clinics?page={page}")
    page1_clinics = res.get_json()

    page = 2
    res = client.get(f"/api/clinics?page={page}")
    page2_clinics = res.get_json()

    assert len(page2_clinics) == 20
    assert clinics[20]["id"] == page2_clinics[0]["id"]

    for i in range(1, len(page2_clinics)):
        assert isoparse(page2_clinics[i - 1]["created_at"]) > isoparse(
            page2_clinics[i]["created_at"])
        for p in page1_clinics:
            assert page2_clinics[i]["id"] != p["id"]


def test_should_return_should_return_first_n_clinics_match_filter_name_ordered_by_created_at(
        app, client):
    """
    Should return status 200 and first n patietns that match with filter name ordered by created at
    """
    filter_name = fake.word()
    with app.app_context():
        created_clinics = []
        for i in range(30):
            clinic = ClinicBuilder().complete().with_name(
                f"{fake.word()} {filter_name} {fake.word()}").build_object()
            created_clinics.append(clinic)

        clinics = populate_clinics(100, created_clinics)

    clinics = sorted(clinics, key=lambda d: d["created_at"], reverse=True)

    res = client.get(f"/api/clinics?name={filter_name}")

    assert res.status_code == 200

    res_clinics = res.get_json()
    assert len(res_clinics) == 20

    for i in range(1, len(res_clinics)):
        assert isoparse(res_clinics[i - 1]["created_at"]) > isoparse(
            res_clinics[i]["created_at"])
        assert filter_name in res_clinics[i]["name"]

    res = client.get(f"/api/clinics?name={filter_name}&page=2")

    res_clinics = res.get_json()

    assert 10 == len(res_clinics)
    for p in res_clinics:
        assert filter_name in p["name"]


def test_should_return_should_return_first_n_clinics_filter_type(app, client):
    """
    Should return status 200 and first 10 patients that match with filter type
    """
    filter_type = ClinicType.PEDIATRIC
    with app.app_context():
        created_clinics = []
        for _ in range(20):
            clinic = ClinicBuilder().complete().with_type(
                filter_type).build_object()
            created_clinics.append(clinic)
            clinic = ClinicBuilder().complete().with_type(
                ClinicType.DENTISTRY).build_object()
            created_clinics.append(clinic)

        populate_clinics(0, created_clinics)

    res = client.get(f"/api/clinics?type={filter_type.value}")

    assert res.status_code == 200

    res_clinics = res.get_json()

    for clinic in res_clinics:
        assert clinic["type"] == filter_type.value


def test_should_return_200_and_clinic_get_clinic_by_id(app, client):
    """
    Should return status 200 and clinic get clinic by id
    """
    with app.app_context():
        clinics = populate_clinics()

    clinic = clinics[0]
    clinic_id = clinic["id"]

    res = client.get(f"/api/clinics/{clinic_id}")

    assert res.status_code == 200

    res_json = res.get_json()
    assert "clinic" in res_json
    res_clinic = res_json["clinic"]

    assert_clinic(res_clinic, clinic)


def test_should_return_200_and_clinic_get_clinic_by_cnpj(app, client):
    """
    Should return status 200 and clinic get clinic by cnpj
    """
    with app.app_context():
        clinics = populate_clinics()

    clinic = clinics[0]
    clinic_cnpj = clinic["cnpj"]

    res = client.get(f"/api/clinics/{clinic_cnpj}/cnpj")

    assert res.status_code == 200

    res_json = res.get_json()
    assert "clinic" in res_json
    res_clinic = res_json["clinic"]

    assert_clinic(res_clinic, clinic)


def test_should_return_200_and_clinic_get_clinic_by_phone(app, client):
    """
    Should return status 200 and clinic get clinic by phone
    """
    with app.app_context():
        clinics = populate_clinics()

    clinic = clinics[0]
    clinic_phone = clinic["phone"]

    res = client.get(f"/api/clinics/{clinic_phone}/phone")

    assert res.status_code == 200

    res_json = res.get_json()
    assert "clinic" in res_json
    res_clinic = res_json["clinic"]

    assert_clinic(res_clinic, clinic)


def test_should_return_404_if_clinic_not_exists_on_get_clinic(client):
    """
    Should return status 404 if clinic not exists on get clinic
    """
    res = client.get(f"/api/clinics/{0}")

    assert res.status_code == 404
    res_json = res.get_json()
    assert "message" in res_json

    res = client.get("/api/clinics/11111111111/cnpj")

    assert res.status_code == 404
    res_json = res.get_json()
    assert "message" in res_json

    res = client.get("/api/clinics/9999999999/phone")

    assert res.status_code == 404
    res_json = res.get_json()
    assert "message" in res_json


#  GET  #

#  PUT  #


def test_should_return_200_when_clinic_is_updated_with_valid_data(app, client):
    """
    Should return status 200 when clinic is udpated with valid data
    """
    with app.app_context():
        clinics = populate_clinics()
    clinic_id = clinics[0]["id"]
    update_clinic = ClinicBuilder().complete().build()

    res = client.put(f"/api/clinics/{clinic_id}", json=update_clinic)

    assert res.status_code == 200

    with app.app_context():
        persited_clinic = session.execute(
            select(Clinic).where(
                (Clinic.id == clinic_id)
                & (Clinic.cnpj == update_clinic["cnpj"])
                & (Clinic.phone == update_clinic["phone"])
                & (Clinic.name == update_clinic["name"])
                & (Clinic.type == update_clinic["type"])
                & (Clinic.address == update_clinic["address"])
                & (Clinic.latitude == update_clinic["latitude"])
                & (Clinic.longitude == update_clinic["longitude"]))).scalar()
    assert persited_clinic

    res_json = res.get_json()
    assert "clinic" in res_json
    res_clinic = res_json["clinic"]

    assert_clinic(res_clinic, update_clinic)


def test_should_return_404_if_clinic_to_update_not_exists(app, client):
    """
    Should return status 404 if clinic to update not exists
    """
    with app.app_context():
        populate_clinics()

    update_clinic = ClinicBuilder().complete().build()

    res = client.put(f"/api/clinics/{0}", json=update_clinic)

    assert res.status_code == 404
    res_json = res.get_json()
    assert "message" in res_json


def test_should_return_400_whether_request_payload_is_invalid_on_update_patient(
        client):
    """
    Should return status 400 whether request payload is invalid on update patient
    """
    new_clinic = {}

    res = client.put("/api/clinics/0", json=new_clinic)

    assert res.status_code == 400
    res_json = res.get_json()

    assert len(res_json) == 5
    assert "name" in res_json
    assert "cnpj" in res_json
    assert "phone" in res_json
    assert "type" in res_json

    new_clinic = ClinicBuilder().with_name(fake.pystr(
        min_chars=1, max_chars=1)).with_cnpj("not a cnpj").with_phone(
            "not a phone number").with_latitude(-91).with_longitude(
                181).with_type(0).build()

    res = client.put("/api/clinics/0", json=new_clinic)

    assert res.status_code == 400
    res_json = res.get_json()

    assert len(res_json) == 6
    assert "name" in res_json
    assert "cnpj" in res_json
    assert "phone" in res_json
    assert "type" in res_json
    assert "latitude" in res_json
    assert "longitude" in res_json

    new_clinic = ClinicBuilder().complete().with_name(
        fake.pystr(min_chars=256, max_chars=300)).with_latitude(
            "not a number").with_longitude("not a number").build()

    res = client.put("/api/clinics/0", json=new_clinic)

    assert res.status_code == 400
    res_json = res.get_json()

    assert len(res_json) == 3
    assert "name" in res_json
    assert "latitude" in res_json
    assert "longitude" in res_json


def test_should_return_400_whether_payload_have_cnpj_that_is_already_in_use_on_update_clinic(
        app, client):
    """
    Should return 400 if payload have cnpj that is already in use on update clinic
    """
    with app.app_context():
        clinics = populate_clinics()

    clinic_id = clinics[0]["id"]
    new_clinic = ClinicBuilder().with_cnpj(clinics[1]["cnpj"]).build()

    res = client.put(f"/api/clinics/{clinic_id}", json=new_clinic)

    assert res.status_code == 400
    res_json = res.get_json()
    assert "cnpj" in res_json
    assert "registered" in res_json["cnpj"]


def test_should_return_400_whether_payload_have_phone_that_is_already_in_use_on_update_clinic(
        app, client):
    """
    Should return 400 if payload have phone that is already in use
    """
    with app.app_context():
        clinics = populate_clinics()

    clinic_id = clinics[0]["id"]
    new_clinic = ClinicBuilder().with_phone(clinics[1]["phone"]).build()

    res = client.put(f"/api/clinics/{clinic_id}", json=new_clinic)

    assert res.status_code == 400
    res_json = res.get_json()
    assert "phone" in res_json
    assert "registered" in res_json["phone"]


#  PUT  #

#  DELETE  #


def test_should_return_204_when_delete_clinic_if_exists_or_not(client, app):
    """
    Should return 204 when delete clinic with him existing or not
    """
    with app.app_context():
        clinics = populate_clinics()

    clinic = clinics[0]
    res = client.delete("/api/clinics/" + str(clinic["id"]))
    assert res.status_code == 204

    with app.app_context():
        persited_clinic = session.get(Clinic, clinic["id"])
    assert not persited_clinic

    res = client.delete("/api/clinics/9999")
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

    res = client.post("/api/clinics", json=useless_payload)
    assert_useless(res)

    res = client.put("/api/clinics/123", json=useless_payload)
    assert_useless(res)

    res = client.get("/api/clinics", query_string=useless_payload)
    assert_useless(res)
