

def pridaj_produkt(name, min_pocet,dalsi_predaj,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "produkt": {
            "id":"1",
            "name": str(name),
            "min_pocet": int(min_pocet),
            "dalsi_predaj":int(dalsi_predaj)
        }
    }
    client.service.insert(**request_data)

def uprav_produkt(name, min_pocet,dalsi_predaj,id,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "entity_id" : int(id),
        "produkt": {
            "id":int(id),
            "name": str(name),
            "min_pocet": int(min_pocet),
            "dalsi_predaj":bool(dalsi_predaj)
        }
    }
    client.service.update(**request_data)

