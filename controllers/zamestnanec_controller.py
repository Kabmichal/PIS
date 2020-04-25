
def try2_func(name, rola,pobocka_id,email,heslo,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "zamestnanec": {
            "id":"1",
            "name": str(name),
            "rola": int(rola),
            "pobocka_id":int(pobocka_id),
            "email":email,
            "heslo":heslo,
            "is_authenticated": "True"
        }
    }
    client.service.insert(**request_data)

def update_func(name, rola,pobocka_id,email,heslo,id,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "entity_id" : int(id),
        "zamestnanec": {
            "id":int(id),
            "name": str(name),
            "rola": int(rola),
            "pobocka_id":int(pobocka_id),
            "email":email,
            "heslo":heslo,
            "is_authenticated":"True"
        }
    }
    client.service.update(**request_data)