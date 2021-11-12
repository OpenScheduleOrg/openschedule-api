import random
from datetime import date, datetime, timezone, timedelta

from app.models import db, Cliente, Clinica, Consulta, Horario
from app.common.exc import  APIExceptionHandler
from conftest import app
from db import generate_marcada

def test_add_consulta(app):

    with app.app_context():
        id_clinica = random.choice(Consulta.query.all()).id
        id_cliente = random.choice(Cliente.query.all()).id
        consultas = Consulta.query.all()
        id_clinica_almoco = Horario.query.filter_by(almoco=True).first().clinica.id


    #   Teste uma inserção correta, marcada como primeiro parametro para testar a validação que é dependente da ordem da construtor


    with app.app_context():
        new_consulta = Consulta(marcada=generate_marcada(id_clinica), id_clinica=id_clinica, id_cliente=id_cliente, descricao="Revisão", realizada=False)
        db.session.add(new_consulta)
        db.session.commit()
        db.session.refresh(new_consulta)
        consultas.append(new_consulta)
#   Testando criar uma consulta em clinica não existente

    try:
        with app.app_context():
            new_consulta = Consulta(marcada=generate_marcada(id_clinica), id_clinica=0, id_cliente=id_cliente)
            raise Exception("Consulta must be raise a exception APIExceptionHandler")
    except APIExceptionHandler as e:
        pass
    except Exception as e:
        raise e


#   Testando criar uma consulta como uma data e hora em um formata não ISO

    try:
        with app.app_context():
            new_consulta = Consulta(marcada="not a iso format of datetime", id_clinica=id_clinica, id_cliente=id_cliente)
            raise Exception("Consulta must be raise a exception APIExceptionHandler")
    except APIExceptionHandler as e:
        pass
    except Exception as e:
        raise e


#   Testando criar uma consulta em uma clinica sem horário no weekday 6

    today = datetime.now(timezone.utc)
    today = today + timedelta(days=(6 - today.weekday()))
    try:
        with app.app_context():
            new_consulta = Consulta(marcada=today, id_clinica=id_clinica, id_cliente=id_cliente)
            raise Exception("Consulta must be raise a exception APIExceptionHandler")
    except APIExceptionHandler as e:
        pass
    except Exception as e:
        raise e

#   Testando criar uma consulta em uma data e hora já inserida

    try:
        with app.app_context():
            new_consulta = Consulta(marcada=consultas[-1].marcada, id_clinica=id_clinica, id_cliente=id_cliente)
            raise Exception("Consulta must be raise a exception APIExceptionHandler")
    except APIExceptionHandler as e:
        pass
    except Exception as e:
        raise e

#   Testando criar uma consulta em uma data e hora já inserida

    try:
        with app.app_context():
            new_consulta = Consulta(marcada=consultas[-1].marcada, id_clinica=id_clinica, id_cliente=id_cliente)
            raise Exception("Consulta must be raise a exception APIExceptionHandler")
    except APIExceptionHandler as e:
        pass
    except Exception as e:
        raise e

#   Testando a inserção em horas fora do periodo de expediente


    with app.app_context():
        marcada = generate_marcada(id_clinica_almoco)
        horario = Horario.query.filter_by(id_clinica=id_clinica_almoco, dia_semana=marcada.weekday()).first()

        antes_am_inicio = datetime.combine(marcada.date(), horario.am_inicio, tzinfo=timezone.utc) - timedelta(minutes=1)
        am_fim_antes_pm_inicio = datetime.combine(marcada.date(), horario.am_fim, tzinfo=timezone.utc)
        pm_fim = datetime.combine(marcada.date(), horario.pm_fim, tzinfo=timezone.utc)

        # Antes do horário de expediente
        try:
            new_consulta = Consulta(marcada=antes_am_inicio, id_clinica=id_clinica_almoco, id_cliente=id_cliente)
            raise Exception("Consulta must be raise a exception APIExceptionHandler")
        except APIExceptionHandler as e:
            pass
        except Exception as e:
            raise e

        # no horário de almoço
        try:
            new_consulta = Consulta(marcada=am_fim_antes_pm_inicio, id_clinica=id_clinica_almoco, id_cliente=id_cliente)
            raise Exception("Consulta must be raise a exception APIExceptionHandler")
        except APIExceptionHandler as e:
            pass
        except Exception as e:
            raise e

        # no pós expediente
        try:
            new_consulta = Consulta(marcada=pm_fim, id_clinica=id_clinica_almoco, id_cliente=id_cliente)
            raise Exception("Consulta must be raise a exception APIExceptionHandler")
        except APIExceptionHandler as e:
            pass
        except Exception as e:
            raise e
