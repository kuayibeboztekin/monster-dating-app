# Anforderungen der Monster Dating App

## Scope V1.0

### In Scope
- Registrierung und Login
- Profil erstellen und bearbeiten
- Match suchen
- Suchfilter anwenden
- Swipe- und Matching-Mechanismus
- Privater 1:1-Chat
- Profil verifizieren
- Monster blockieren
- Profile oder Inhalte melden
- Standort-Privatsphäre verwalten
- Sicherheitsfilter für natürliche Feinde

### Out of Scope
- Video-Speed-Dating
- Virtuelle Treffen
- Gruppenchat
- Events / Eventkalender
- Premium / Zahlung / Boosts
- Geschenkservice
- Bewertungssystem nach Dates

## Funktionale Anforderungen

### Must Have
- Das System muss Monstern die Möglichkeit bieten, ein Benutzerkonto zu registrieren und sich sicher anzumelden.
- Das System muss Monstern die Möglichkeit bieten, ein Profil mit Spezies, Alter, Region, Interessen, Fähigkeiten und Profilbeschreibung zu erstellen und zu bearbeiten.
- Das System muss prüfen, ob ein Profil vollständig genug ist, bevor es für Matching-Vorschläge freigegeben wird.
- Das System muss Monstern die Möglichkeit bieten, nach potenziellen Matches zu suchen.
- Das System muss Monstern die Möglichkeit bieten, Suchergebnisse nach Kriterien wie Spezies, Interessen, Aktivitätsrhythmus und Region zu filtern.
- Das System muss verhindern, dass Monster, die als natürliche Feinde definiert sind, einander in Vorschlägen oder Suchergebnissen sehen.
- Das System muss Monstern die Möglichkeit bieten, vorgeschlagene Profile positiv oder negativ zu bewerten und bei beidseitigem Interesse ein Match zu erzeugen.
- Das System muss Monstern die Möglichkeit bieten, nach einem erfolgreichen Match private 1:1-Nachrichten auszutauschen.
- Das System muss Monstern die Möglichkeit bieten, andere Monster zu blockieren, sodass keine weiteren Nachrichten und Profilvorschläge mehr möglich sind.
- Das System muss Monstern die Möglichkeit bieten, Profile oder Nachrichten wegen Belästigung, Betrugsverdacht oder unangemessener Inhalte zu melden.
- Das System muss Monstern die Möglichkeit bieten, festzulegen, ob ihr Standort genau, grob oder gar nicht angezeigt wird.

### Should Have
- Das System soll Monstern die Möglichkeit bieten, ihr Profil durch einen Verifizierungsprozess bestätigen zu lassen.
- Das System soll bei verifizierten Profilen den Verifizierungsstatus sichtbar anzeigen.
- Das System soll Administrator:innen die Möglichkeit bieten, eingegangene Meldungen einzusehen und zu bearbeiten.

## Nicht-funktionale Anforderungen
- Die App muss Suchergebnisse für „Match suchen“ in maximal 2 Sekunden anzeigen.
- Die App muss Textnachrichten im Normalfall in maximal 1 Sekunde zustellen.
- Die App muss im Monatsmittel eine Verfügbarkeit von mindestens 99,5 % erreichen.
- Die App muss alle Datenübertragungen zwischen Client und Server verschlüsseln.
- Die App darf Passwörter niemals im Klartext speichern.
- Die App muss mindestens 10'000 gleichzeitig aktive Nutzer:innen unterstützen, ohne dass die Antwortzeit für Kernfunktionen 3 Sekunden überschreitet.
- Zentrale Funktionen wie Registrierung, Profilbearbeitung, Match-Suche und Blockieren müssen mit maximal 3 Interaktionen vom Hauptmenü aus erreichbar sein.
- Nach 5 fehlgeschlagenen Login-Versuchen innerhalb von 10 Minuten muss eine temporäre Sperre ausgelöst werden.

## Priorisierung
- Must have: Kernfunktionen für Konto, Profil, Matching, Chat, Blockieren, Melden und Standort-Privatsphäre
- Should have: Verifizierung und administrative Bearbeitung von Meldungen
- Won't have in V1.0: Events, Gruppenchat, virtuelle Treffen und Premium-Funktionen