import re
import json
from flask import Response
from sqlalchemy.sql.expression import desc


def CPFormat(cpf: str):
    if(re.match(r"^\d{11}$", cpf)):
        return cpf[0:3]+"."+cpf[3:6]+"."+cpf[6:9]+"-"+cpf[9:11]
    if(re.match(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", cpf)):
        return cpf
    return None

def gen_response(status, **body):
    return Response(json.dumps(body, indent=4, sort_keys=True, default=str), status=status, mimetype="application/json")


def insertSort(ls):
    ls = ls[:]

    for i in range(1, len(ls)):
        elem = ls[i]
        ls.pop(i)
        for desci in range(i-1, -1, -1):

            if(ls[desci].agenda.data < elem.agenda.data):
                ls.insert(desci+1, elem)
                break
            if(desci == 0):
                ls.insert(0, elem)

    return ls
