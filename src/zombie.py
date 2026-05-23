from src.monster import Monster, MonsterTyp


class Zombie(Monster):
    def __init__(self, id, name, alter, region, hobbys=None, aengste=None, kullanici_adi=None, sifre="passwort123"):
        super().__init__(id, name, MonsterTyp.ZOMBIE, alter, region, hobbys, aengste, kullanici_adi, sifre)
