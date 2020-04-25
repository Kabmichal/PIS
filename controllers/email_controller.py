

def posli_email(name, id_zamestnanec,id_produkt,datum,vybaveny,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "email": {
            "id":"1",
            "name": str(name),
            "id_zamestnanec": id_zamestnanec,
            "id_produkt": id_produkt,
            "datum":datum,
            "vybaveny":vybaveny
        }
    }
    client.service.insert(**request_data)

def uprav_email(name, id_zamestnanec,id_produkt,id,datum,vybaveny,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "entity_id" : int(id),
        "pobocka": {
            "id":int(id),
            "name": str(name),
            "id_zamestnanec": id_zamestnanec,
            "id_produkt": id_produkt,
            "datum":datum,
            "vybaveny":vybaveny
        }
    }
    client.service.update(**request_data)

