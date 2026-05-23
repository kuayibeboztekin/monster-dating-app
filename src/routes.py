from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from src.vampir import Vampir
from src.werwolf import Werwolf
from src.zombie import Zombie
from src.geist import Geist
from src.match import Match

routes = Blueprint("routes", __name__)

# Admin-Zugangsdaten
ADMIN_KULLANICI = "admin"
ADMIN_SIFRE = "admin123"

monster_liste = [
    Vampir(1, "Drakula", 500, "Siebenbürgen",
           hobbys=["Nachtfliegen", "Orgelspielen", "Antiquitäten sammeln"],
           aengste=["Knoblauch", "Sonnenlicht", "Silber"], sifre="drakula"),
    Werwolf(2, "Fenrir", 300, "Schwarzwald",
            hobbys=["Waldlaufen", "Heulen", "Mondbeobachtung"],
            aengste=["Silber", "Feuer", "Käfige"], sifre="fenrir"),
    Vampir(3, "Lilith", 800, "Wien",
           hobbys=["Orgelspielen", "Nachtfliegen", "Oper"],
           aengste=["Knoblauch", "Sonnenlicht", "Holzpfähle"], sifre="lilith"),
    Zombie(4, "Mortis", 25, "Hamburg",
           hobbys=["Wandern", "Kochen", "Gartenarbeit"],
           aengste=["Feuer", "Salz", "Einsamkeit"], sifre="mortis"),
    Geist(5, "Nebula", 150, "Prag",
          hobbys=["Mondbeobachtung", "Malen", "Musik hören"],
          aengste=["Lärm", "Sonnenlicht", "Salz"], sifre="nebula"),
    Werwolf(6, "Lykos", 200, "München",
            hobbys=["Waldlaufen", "Schwimmen", "Kochen"],
            aengste=["Silber", "Käfige", "Lärm"], sifre="lykos"),
    Vampir(7, "Seraphina", 650, "Budapest",
           hobbys=["Oper", "Antiquitäten sammeln", "Tanzen"],
           aengste=["Knoblauch", "Silber", "Holzpfähle"], sifre="seraphina"),
    Zombie(8, "Grom", 40, "Berlin",
           hobbys=["Wandern", "Heulen", "Gartenarbeit"],
           aengste=["Feuer", "Einsamkeit", "Sonnenlicht"], sifre="grom"),
    Geist(9, "Ophelia", 300, "Wien",
          hobbys=["Malen", "Oper", "Musik hören"],
          aengste=["Lärm", "Salz", "Feuer"], sifre="ophelia"),
    Werwolf(10, "Ragnar", 450, "Oslo",
            hobbys=["Heulen", "Schwimmen", "Mondbeobachtung"],
            aengste=["Silber", "Feuer", "Sonnenlicht"], sifre="ragnar"),
    Vampir(11, "Morrigan", 900, "Dublin",
           hobbys=["Nachtfliegen", "Tanzen", "Antiquitäten sammeln"],
           aengste=["Knoblauch", "Sonnenlicht", "Silber"], sifre="morrigan"),
    Zombie(12, "Cinder", 60, "Köln",
           hobbys=["Kochen", "Musik hören", "Wandern"],
           aengste=["Feuer", "Salz", "Käfige"], sifre="cinder"),
    Geist(13, "Zephyr", 200, "Zürich",
          hobbys=["Mondbeobachtung", "Schwimmen", "Malen"],
          aengste=["Lärm", "Sonnenlicht", "Käfige"], sifre="zephyr"),
    Werwolf(14, "Vixen", 180, "Hamburg",
            hobbys=["Waldlaufen", "Tanzen", "Kochen"],
            aengste=["Silber", "Lärm", "Feuer"], sifre="vixen"),
    Vampir(15, "Casimir", 720, "Krakau",
           hobbys=["Orgelspielen", "Oper", "Tanzen"],
           aengste=["Knoblauch", "Holzpfähle", "Sonnenlicht"], sifre="casimir"),
]

# In-Memory-Speicher
swipes_rechts: dict[int, list[int]] = {3: [1]}
swipes_links: dict[int, list[int]] = {}
matches: list[Match] = []
blockierungen: dict[int, list[int]] = {}
_match_counter = [1]


# --- Hilfsfunktionen ---

def _finde_monster(monster_id: int):
    return next((m for m in monster_liste if m.id == monster_id), None)


def _finde_nach_kullanici(kullanici_adi: str):
    return next((m for m in monster_liste if m.kullanici_adi == kullanici_adi), None)


def _ist_gegenseitiger_match(swiper_id: int, ziel_id: int) -> bool:
    return swiper_id in swipes_rechts.get(ziel_id, [])


def _match_erstellen(monster1, monster2) -> Match:
    match = Match(_match_counter[0], monster1, monster2)
    _match_counter[0] += 1
    matches.append(match)
    return match


def _eingeloggt_als():
    mid = session.get("monster_id")
    return _finde_monster(mid) if mid else None


# --- Decorators ---

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("monster_id") and not session.get("is_admin"):
            flash("Bitte zuerst einloggen.", "warning")
            return redirect(url_for("routes.login"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Kein Zugriff.", "danger")
            return redirect(url_for("routes.login"))
        return f(*args, **kwargs)
    return decorated


# --- Auth-Routen ---

@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        kullanici_adi = request.form.get("kullanici_adi", "").strip().lower()
        sifre = request.form.get("sifre", "")

        if kullanici_adi == ADMIN_KULLANICI and sifre == ADMIN_SIFRE:
            session["is_admin"] = True
            session.pop("monster_id", None)
            return redirect(url_for("routes.admin"))

        monster = _finde_nach_kullanici(kullanici_adi)
        if monster and monster.sifre_dogrula(sifre):
            if not monster.aktiv:
                flash("Dein Konto wurde deaktiviert.", "danger")
                return redirect(url_for("routes.login"))
            session["monster_id"] = monster.id
            session.pop("is_admin", None)
            return redirect(url_for("routes.index"))

        flash("Benutzername oder Passwort falsch.", "danger")

    return render_template("login.html")


@routes.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("routes.login"))


# --- Hauptrouten ---

@routes.route("/")
@login_required
def index():
    return render_template("index.html", monster=monster_liste, ich=_eingeloggt_als())


@routes.route("/profil/<int:monster_id>")
@login_required
def profil(monster_id: int):
    monster = _finde_monster(monster_id)
    if monster is None:
        return "Monster nicht gefunden", 404
    ich = _eingeloggt_als()
    ist_blockiert = monster_id in blockierungen.get(ich.id if ich else -1, [])
    return render_template("profil.html", monster=monster, ich=ich, ist_blockiert=ist_blockiert)


@routes.route("/suche/<int:monster_id>")
@login_required
def suche(monster_id: int):
    monster = _finde_monster(monster_id)
    if monster is None:
        return "Monster nicht gefunden", 404

    bereits_geswiped = swipes_rechts.get(monster_id, []) + swipes_links.get(monster_id, [])
    blockiert_von_mir = blockierungen.get(monster_id, [])
    ich_bin_blockiert = [mid for mid, liste in blockierungen.items() if monster_id in liste]
    ausgeschlossen = set(bereits_geswiped + blockiert_von_mir + ich_bin_blockiert + [monster_id])

    kandidaten = [m for m in monster_liste if m.id not in ausgeschlossen]

    # Filter
    alter_min = request.args.get("alter_min", type=int)
    alter_max = request.args.get("alter_max", type=int)
    region = request.args.get("region", "").strip().lower()
    monster_typ = request.args.get("monster_typ", "").strip()
    hobby = request.args.get("hobby", "").strip().lower()

    if alter_min is not None:
        kandidaten = [m for m in kandidaten if m.alter >= alter_min]
    if alter_max is not None:
        kandidaten = [m for m in kandidaten if m.alter <= alter_max]
    if region:
        kandidaten = [m for m in kandidaten if region in m.region.lower()]
    if monster_typ:
        kandidaten = [m for m in kandidaten if m.monsterTyp.value == monster_typ]
    if hobby:
        kandidaten = [m for m in kandidaten if any(hobby in h.lower() for h in m.hobbys)]

    kandidaten_mit_score = [(k, monster.berechne_kompatibilitaet(k)) for k in kandidaten]
    kandidaten_mit_score.sort(key=lambda x: x[1]["score"], reverse=True)

    alle_regionen = sorted({m.region for m in monster_liste if m.id != monster_id})
    alle_typen = sorted({m.monsterTyp.value for m in monster_liste if m.id != monster_id})
    alle_hobbys = sorted({h for m in monster_liste for h in m.hobbys if m.id != monster_id})

    return render_template(
        "suche.html",
        monster=monster,
        kandidaten_mit_score=kandidaten_mit_score,
        alle_regionen=alle_regionen,
        alle_typen=alle_typen,
        alle_hobbys=alle_hobbys,
        filter_alter_min=alter_min or "",
        filter_alter_max=alter_max or "",
        filter_region=region,
        filter_typ=monster_typ,
        filter_hobby=hobby,
        ich=_eingeloggt_als(),
    )


@routes.route("/swipe/<int:swiper_id>/<int:ziel_id>/<richtung>")
@login_required
def swipe(swiper_id: int, ziel_id: int, richtung: str):
    swiper = _finde_monster(swiper_id)
    ziel = _finde_monster(ziel_id)
    if not swiper or not ziel:
        return "Monster nicht gefunden", 404

    if richtung == "rechts":
        swipes_rechts.setdefault(swiper_id, []).append(ziel_id)
        if _ist_gegenseitiger_match(swiper_id, ziel_id):
            _match_erstellen(swiper, ziel)
            return redirect(url_for("routes.match_gefunden", monster_id=swiper_id, ziel_id=ziel_id))
    elif richtung == "links":
        swipes_links.setdefault(swiper_id, []).append(ziel_id)

    return redirect(url_for("routes.suche", monster_id=swiper_id))


@routes.route("/match/<int:monster_id>/<int:ziel_id>")
@login_required
def match_gefunden(monster_id: int, ziel_id: int):
    monster = _finde_monster(monster_id)
    ziel = _finde_monster(ziel_id)
    if not monster or not ziel:
        return "Monster nicht gefunden", 404
    kompatibilitaet = monster.berechne_kompatibilitaet(ziel)
    return render_template("match_gefunden.html", monster=monster, ziel=ziel,
                           kompatibilitaet=kompatibilitaet, ich=_eingeloggt_als())


@routes.route("/matches/<int:monster_id>")
@login_required
def meine_matches(monster_id: int):
    monster = _finde_monster(monster_id)
    if monster is None:
        return "Monster nicht gefunden", 404
    meine = [m for m in matches if m.monster1.id == monster_id or m.monster2.id == monster_id]
    return render_template("matches.html", monster=monster, matches=meine, ich=_eingeloggt_als())


# --- Engelleme ---

@routes.route("/blockieren/<int:blocker_id>/<int:ziel_id>")
@login_required
def blockieren(blocker_id: int, ziel_id: int):
    blockierungen.setdefault(blocker_id, [])
    if ziel_id not in blockierungen[blocker_id]:
        blockierungen[blocker_id].append(ziel_id)
    flash("Benutzer wurde blockiert.", "success")
    return redirect(url_for("routes.index"))


@routes.route("/entblocken/<int:blocker_id>/<int:ziel_id>")
@login_required
def entblocken(blocker_id: int, ziel_id: int):
    if blocker_id in blockierungen and ziel_id in blockierungen[blocker_id]:
        blockierungen[blocker_id].remove(ziel_id)
    flash("Blockierung aufgehoben.", "info")
    return redirect(url_for("routes.profil", monster_id=ziel_id))


# --- Admin ---

@routes.route("/admin")
@admin_required
def admin():
    alle_blockierungen = [
        {"blocker": _finde_monster(bid), "ziel": _finde_monster(zid)}
        for bid, liste in blockierungen.items()
        for zid in liste
    ]
    return render_template("admin.html", monster_liste=monster_liste,
                           matches=matches, blockierungen=alle_blockierungen)


@routes.route("/admin/deaktivieren/<int:monster_id>", methods=["POST"])
@admin_required
def admin_deaktivieren(monster_id: int):
    monster = _finde_monster(monster_id)
    if monster:
        monster.aktiv = not monster.aktiv
    return redirect(url_for("routes.admin"))
