from conftest import client
from db import clientes_data

def test_all_clientes(client):
    rs = client.get("/clientes")

    assert rs.status_code == 200

    clientes_rs = rs.get_json()["clientes"]
    assert len(clientes_rs) == len(clientes_data)

    for ce in clientes_data:
        for key in ce.keys():

            for cr in clientes_rs:
                if cr[key] == ce[key]:
                    break

            assert cr[key] == ce[key]
            del cr[key];
