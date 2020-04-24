def pridaj_produkt_pobocka(name, produkt_id,pobocka_id,pocet_pobocka,pokles_minima,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "produkt_pobocka": {
            "id":"1",
            "name": str(name),
            "produkt_id": int(produkt_id),
            "pobocka_id":int(pobocka_id),
            "pocet_pobocka":int(pocet_pobocka),
            "pokles_minima":int(pokles_minima)
        }
    }
    client.service.insert(**request_data)

def uprav_produkt_pobocka(name, produkt_id,pobocka_id,pocet_pobocka,pokles_minima,id,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "entity_id" : int(id),
        "produkt_pobocka": {
            "id":int(id),
            "name": str(name),
            "produkt_id": int(produkt_id),
            "pobocka_id":int(pobocka_id),
            "pocet_pobocka":int(pocet_pobocka),
            "pokles_minima":int(pokles_minima)
        }
    }
    client.service.update(**request_data)

