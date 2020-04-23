

def pridaj_pobocku(name, adresa,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "pobocka": {
            "id":"1",
            "name": str(name),
            "adresa": str(adresa)
        }
    }
    client.service.insert(**request_data)

def uprav_pobocku(name, adresa,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "entity_id" : int(id),
        "pobocka": {
            "id":int(id),
            "name": str(name),
            "adresa": str(adresa)
        }
    }
    client.service.update(**request_data)

