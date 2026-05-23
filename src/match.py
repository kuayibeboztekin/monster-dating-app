from datetime import datetime
from enum import Enum


class MatchStatus(Enum):
    ANGENOMMEN = "Angenommen"
    AKTIVER_CHAT = "Aktiver Chat"
    BEENDET = "Beendet"


class Match:
    def __init__(self, id: int, monster1, monster2):
        self.id = id
        self.monster1 = monster1
        self.monster2 = monster2
        self.status = MatchStatus.ANGENOMMEN
        self.matchDatum = datetime.now()
