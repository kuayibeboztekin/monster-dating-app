# Beschreibung des Klassendiagramms

## Überblick
Das Klassendiagramm der Monster Dating App orientiert sich an der V1.0-Kernfunktionalität.
Im Zentrum steht die abstrakte Basisklasse `Monster`. Von ihr erben konkrete Monster-Typen wie `Vampir`, `Werwolf`, `Zombie` und `Geist`.

## Wichtige Klassen
- `Monster` (abstrakt)
- `Vampir`
- `Werwolf`
- `Zombie`
- `Geist`
- `Profil`
- `Match`
- `Nachricht`
- `Suchfilter`
- `Meldung`
- `Administrator`

## Zentrale Modellidee
Ein Monster besitzt ein Profil und kann mit Suchfiltern nach potenziellen Matches suchen.
Wenn zwei Monster beidseitig Interesse zeigen, entsteht ein `Match`.
Erst nach einem erfolgreichen Match können private `Nachricht`-Objekte ausgetauscht werden.
Zusätzlich können Monster andere Monster blockieren oder Profile beziehungsweise Inhalte melden.
Administrator:innen prüfen eingegangene Meldungen.

## Vererbung
`Monster` ist die abstrakte Basisklasse.
Die Klassen `Vampir`, `Werwolf`, `Zombie` und `Geist` sind Spezialisierungen von `Monster` und erweitern gemeinsame Eigenschaften der Basisklasse um typspezifisches Verhalten.

## Wichtige Beziehungen
- Ein `Monster` besitzt genau ein `Profil`.
- Ein `Monster` kann 0..* `Match`-Beziehungen haben.
- Ein `Match` verbindet genau 2 Monster.
- Ein `Match` kann 0..* `Nachricht`-Objekte enthalten.
- Ein `Monster` kann 0..* `Meldung`-Objekte erzeugen.
- Ein `Administrator` bearbeitet `Meldung`-Objekte.
- Ein `Monster` kann einen `Suchfilter` verwenden, um Vorschläge einzugrenzen.

## Beziehungstypen
- `Monster` ◆— `Profil` als Komposition, weil ein Profil fachlich nicht unabhängig vom Monster existiert.
- `Match` ◆— `Nachricht` als Komposition, weil Nachrichten in diesem Modell zum jeweiligen Match gehören.
- `Monster` — `Match` als Assoziation.
- `Administrator` — `Meldung` als Assoziation.
- Vererbung zwischen `Monster` und den konkreten Monster-Typen.

## Mögliche Attribute
### Monster
- id: int
- name: String
- monsterTyp: MonsterTyp
- alter: int
- region: String
- aktiv: boolean

### Profil
- beschreibung: String
- interessen: List<String>
- faehigkeiten: List<String>
- verifizierungsstatus: Verifizierungsstatus
- standortSichtbarkeit: StandortSichtbarkeit
- vollstaendig: boolean

### Match
- id: int
- status: MatchStatus
- matchDatum: DateTime

### Nachricht
- id: int
- text: String
- sendeZeit: DateTime
- gelesen: boolean

### Suchfilter
- spezies: MonsterTyp
- interessen: List<String>
- aktivitaetsrhythmus: Aktivitaetsrhythmus
- region: String

### Meldung
- id: int
- grund: Meldungsgrund
- beschreibung: String
- status: Meldungsstatus
- erstelltAm: DateTime

## Mögliche Methoden
### Monster
- registrieren(): void
- anmelden(): boolean
- sucheMatches(filter: Suchfilter): List<Monster>
- swipeRechts(ziel: Monster): void
- swipeLinks(ziel: Monster): void
- blockieren(ziel: Monster): void
- melden(ziel: Monster, grund: Meldungsgrund): Meldung

### Profil
- istVollstaendig(): boolean
- aktualisieren(): void
- verifizierungAnfragen(): void

### Match
- matchErzeugen(): void
- chatFreischalten(): void
- statusAktualisieren(): void

### Nachricht
- senden(): void
- alsGelesenMarkieren(): void

### Administrator
- meldungPruefen(m: Meldung): void
- meldungBearbeiten(m: Meldung): void

## Enumerationen
- `MonsterTyp` = VAMPIR, WERWOLF, ZOMBIE, GEIST, HEXE, DRACHE
- `MatchStatus` = VORGESCHLAGEN, ANGENOMMEN, ABGELEHNT, AKTIVER_CHAT, BEENDET, BLOCKIERT
- `Aktivitaetsrhythmus` = TAGAKTIV, NACHTAKTIV, FLEXIBEL
- `StandortSichtbarkeit` = GENAU, GROB, AUSGEBLENDET
- `Verifizierungsstatus` = NICHT_VERIFIZIERT, IN_PRUEFUNG, VERIFIZIERT
- `Meldungsstatus` = OFFEN, IN_BEARBEITUNG, GESCHLOSSEN
- `Meldungsgrund` = BELAESTIGUNG, BETRUGSVERDACHT, UNANGEMESSENER_INHALT

## Begründung
Dieses Klassendiagramm passt zur V1.0-Anforderungsanalyse:
Registrierung, Profilverwaltung, Match-Suche, Filter, Swipe/Matching, privater Chat, Verifizierung, Blockieren, Melden und Standort-Privatsphäre werden fachlich abgebildet.
Bewusst nicht modelliert wurden Funktionen, die laut Scope nicht zu V1.0 gehören, zum Beispiel Gruppenchat, Events oder Premium-Funktionen.