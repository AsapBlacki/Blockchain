import hashlib


class Block:
    def __init__(self, p_hash_precedent, p_data, p_date, p_random):
        self.HashPrecedent = p_hash_precedent
        self.Data = p_data
        self.Date = p_date
        self.Random = p_random

    def preuve_de_travaille(self):
        hashage = hashlib.sha256()
        hashage.update(self.HashPrecedent.encode())
        hashage.update(self.Data.encode())
        hashage.update(self.Date.encode())
        hashage.update(self.Random.encode())
        hashage = hashage.hexdigest()

        nombre_tour = 1

        while True:
            for i in range(0, 4):
                if hashage.startswith('00000'):
                    print(hashage)
                    print(nombre_tour)
                    return nombre_tour
                else:
                    nombre_tour += 1
                    hashage = hashlib.sha256(hashage.encode()).hexdigest()
