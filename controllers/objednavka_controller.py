def vytvor_objednavku(name, zamestnanec_id,odoslana,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "objednavka": {
            "id":"1",
            "name": str(name),
            "zamestnanec_id": str(zamestnanec_id),
            "odoslana": 0
        }
    }
    client.service.insert(**request_data)

def uprav_objednavku(id, name, zamestnanec_id,odoslana,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "entity_id" : int(id),
        "objednavka": {
            "id":int(id),
            "name": str(name),
            "zamestnanec_id": str(zamestnanec_id),
            "odoslana": odoslana
        }
    }
    client.service.update(**request_data)

