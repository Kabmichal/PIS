class Produkt():
    def __init__(self, id, name, min_pocet,dalsi_predaj):
        self.id = id
        self.name = name
        self.min_pocet = min_pocet
        self.dalsi_predaj = dalsi_predaj
        
    def get_id(self):
        return self.id