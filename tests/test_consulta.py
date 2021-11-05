from conftest import client

def test_all_consultas(client):
    rv = client.get("/consultas")

    assert {'consultas' : []} == rv.get_json()
