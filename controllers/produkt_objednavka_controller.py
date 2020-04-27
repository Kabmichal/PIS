def vytvor_produkt_objednavka(name, objednavka_id,email_id,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "produkt_objednavka": {
            "id":"1",
            "name":str(name),
            "objednavka_id": objednavka_id,
            "email_id": email_id
        }
    }
    client.service.insert(**request_data)

def uprav_produkt_objednavka(id, name, objednavka_id,email_id,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "entity_id" : int(id),
        "produkt_objednavka": {
            "id":int(id),
            "name": str(name),
            "objednavka_id": objednavka_id,
            "email_id": email_id
        }
    }
    client.service.update(**request_data)

