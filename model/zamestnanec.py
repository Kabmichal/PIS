class Zamestnanec():
    def __init__(self, id, name, rola,email ,heslo ,is_authenticated, pobocka_id):
        self.id = id
        self.name = name
        self.rola = rola
        self.pobocka_id = pobocka_id
        self.email = email
        self.heslo = heslo
        self.is_authenticated = "True"

    def get_id(self):
        return self.id

    def get_is_authenticated(self):
        return self.is_authenticated