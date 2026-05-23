from abc import ABC, abstractmethod
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash


class MonsterTyp(Enum):
    VAMPIR = "Vampir"
    WERWOLF = "Werwolf"
    ZOMBIE = "Zombie"
    GEIST = "Geist"
    HEXE = "Hexe"
    DRACHE = "Drache"


class Monster(ABC):
    def __init__(
        self,
        id: int,
        name: str,
        monster_typ: MonsterTyp,
        alter: int,
        region: str,
        hobbys: list[str] | None = None,
        aengste: list[str] | None = None,
        kullanici_adi: str | None = None,
        sifre: str = "passwort123",
    ):
        self.id = id
        self.name = name
        self.monsterTyp = monster_typ
        self.alter = alter
        self.region = region
        self.aktiv = True
        self.hobbys: list[str] = hobbys or []
        self.aengste: list[str] = aengste or []
        self.kullanici_adi: str = kullanici_adi or name.lower()
        self._sifre_hash: str = generate_password_hash(sifre)

    def sifre_dogrula(self, sifre: str) -> bool:
        return check_password_hash(self._sifre_hash, sifre)

    def registrieren(self) -> None:
        self.aktiv = True

    def anmelden(self) -> bool:
        return self.aktiv

    def sucheMatches(self) -> list:
        return []

    def swipeRechts(self, ziel: "Monster") -> None:
        pass

    def swipeLinks(self, ziel: "Monster") -> None:
        pass

    def blockieren(self, ziel: "Monster") -> None:
        pass

    def berechne_kompatibilitaet(self, andere: "Monster") -> dict:
        gemeinsame_hobbys = sorted(set(self.hobbys) & set(andere.hobbys))
        gemeinsame_aengste = sorted(set(self.aengste) & set(andere.aengste))
        score = len(gemeinsame_hobbys) * 2 + len(gemeinsame_aengste)
        max_score = len(self.hobbys) * 2 + len(self.aengste)
        prozent = round((score / max_score) * 100) if max_score > 0 else 0
        return {
            "score": score,
            "prozent": prozent,
            "gemeinsame_hobbys": gemeinsame_hobbys,
            "gemeinsame_aengste": gemeinsame_aengste,
        }

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "monsterTyp": self.monsterTyp.value,
            "alter": self.alter,
            "region": self.region,
            "aktiv": self.aktiv,
        }
