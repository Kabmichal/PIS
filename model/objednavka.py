class Objednavka():
    def __init__(self, id, name, rola, pobocka_id):
        self.id = id
        self.name = name
        self.rola = rola
        self.pobocka_id = pobocka_id

    def get_id(self):
        return self.id