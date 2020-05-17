def create_product_sklad(name, produkt_id,pocet,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "hlavny_sklad_produkt": {
            "id":"1",
            "name": str(name),
            "produkt_id":int(produkt_id),
            "pocet":pocet
        }
    }
    client.service.insert(**request_data)

def update_product_sklad(name, produkt_id,pocet,id,client):
    request_data = {
        "team_id": "021",
        "team_password" : "RM7MZR",
        "entity_id" : int(id),
        "hlavny_sklad_produkt": {
            "id":int(id),
            "name": str(name),
            "produkt_id": int(produkt_id),
            "pocet":int(pocet)
        }
    }
    client.service.update(**request_data)