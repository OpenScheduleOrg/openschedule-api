from flask import Blueprint, jsonify, request

api = Blueprint("api", "api")

from app.routes import cliente, clinica, consulta, horario


# STATUS CODE REFERENCE

#           Repostas de sucesso
## 200 OK Estas requisição foi bem sucedida.
## 201 CREATED indica que a requisição foi bem sucedida e que um novo recurso foi criado

#           Repostas de erro do cliente
## 400 BAD REQUEST Essa resposta significa que o servidor não entendeu a requisição pois está com uma sintaxe inválida.
## 404 NOT FOUND O servidor não encontra o recurso solicitado
## 422 UNPROCESSABLE ENTITY indica que o servidor entende o tipo de conteúdo da entidade da requisição, e a sintaxe da requisição esta correta, mas não foi possível processar as instruções presentes.

#           Respostas de erro do Servidor
## 500 INTERNAL SERVER ERROR O servidor encontrou uma situação com a qual não sabe lidar.

