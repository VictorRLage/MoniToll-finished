import requests


url = "https://api.pipefy.com/graphql"


payload = {"query": "mutation{createCard(input:{ pipe_id: \"302621694\" fields_attributes:[{field_id: \"nome_da_empresa\", field_value: \"Brandão Pedágios\"}{field_id: \"descri_o_do_alerta\", field_value: \"Alerta Identificado na CPU da Torre 1!\"}{field_id: \"m_tricas\", field_value: \"Alerta - 85%\"}{field_id: \"mais_detalhes_sobre_o_alerta\", field_value: \"O Alerta foi emitido por conta de alto uso da CPU!\"}]}){clientMutationId card {id title}}}"}
headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyIjp7ImlkIjozMDIwOTE4NzAsImVtYWlsIjoicmVuYXRvLnRpZXJub0BzcHRlY2guc2Nob29sIiwiYXBwbGljYXRpb24iOjMwMDIwMDc5OX19.u1OD3vfD6im7FYV9owyD6kVPdstkeU3_1tX-WJdZz0Pf5VM8QZ2VEO6vEye9ht82VD7t2bnBqMwtuWywW0rjEg",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
