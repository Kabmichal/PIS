class ProduktPobocka():
    def __init__(self, id, name, produkt_id,pobocka_id,pocet_pobocka,pokles_minima):
        self.id = id
        self.name = name
        self.produkt_id = produkt_id
        self.pobocka_id = pobocka_id
        self.pocet_pobocka = pocet_pobocka
        self.pokles_minima = pokles_minima


    def get_id(self):
        return self.id