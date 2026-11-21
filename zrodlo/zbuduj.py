#!/usr/bin/env python3
"""Buduje strony „Historii rodziny” z pliku rodzina.json.

Użycie:  python3 zbuduj.py   (dane: zrodlo/dane/rodzina.json, zasoby: zrodlo/zasoby/)
Wynik:   katalog główny repozytorium (index.html, podstrony, styl.css, strona.js)

Nowa para = nowy wpis w rodzina.json (z polem "rodzice" u dziecka wskazującym jej "id").
Teksty opowieści na razie są polami zastępczymi w szablonie poniżej.
"""
import json, shutil, sys
from html import escape as e
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent  # katalog główny repozytorium: tu powstaje gotowa strona
data = json.loads((SRC / "dane" / "rodzina.json").read_text(encoding="utf-8"))
PARY = {p["id"]: p for p in data["pary"]}
HOME = "zofia-i-bronislaw"
GEN = data["pokolenia"]
SITE = data["rodzina"]
SUB = data.get("podtytul", "Historia rodziny")

import hashlib as _h
VCSS = _h.md5(open(SRC / "zasoby" / "styl.css", "rb").read()).hexdigest()[:8]
VJS = _h.md5(open(SRC / "zasoby" / "strona.js", "rb").read()).hexdigest()[:8]
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,700;1,400'
         '&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Mono:wght@400;500&display=swap">')
PERSON_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3">'
              '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>')

# --- linia (Babci / Dziadka) i kolejność w drzewie ---------------------------
side, order = {}, []
def walk(pid, s):
    p = PARY.get(pid)
    if not p: return
    side[pid] = s
    order.append(pid)
for p in data["pary"]:
    if p["pokolenie"] == 1:
        side[p["id"]] = None
        order.append(p["id"])
for p in data["pary"]:
    if p.get("linia") and p["id"] not in side:
        side[p["id"]] = p["linia"]
        order.append(p["id"])
def expand(level):
    for pid in [i for i in order if PARY[i]["pokolenie"] == level]:
        p = PARY[pid]
        for who, s in (("ona", "her"), ("on", "his")):
            parent = p[who].get("rodzice")
            if parent in PARY and parent not in side:
                walk(parent, s if level == 1 else side[pid])
for lvl in range(1, 10): expand(lvl)

def full(o): return f'{o["imie"]} {o["nazwisko"]}'
def couple_name(p): return f'{p["ona"]["imie"]} i {p["on"]["imie"]}'
def years(o):
    if not o.get("ur") and not o.get("zm"): return ""
    return f'{o.get("ur") or "?"}–{o.get("zm") or "?"}'

# --- menu (hamburger + wysuwana szuflada z kaflami, od najmłodszego pokolenia) ---
def home(): return "index.html"
def url(pid): return home() if pid == HOME else f"{pid}.html"
def nav(current):
    tiers = []
    for g in sorted(GEN, key=float):
        items = [pid for pid in order if PARY[pid]["pokolenie"] == float(g)]
        if not items: continue
        tiles = []
        for pid in items:
            p = PARY[pid]
            s = {"her": "linia Babci", "his": "linia Dziadka"}.get(side.get(pid), "")
            cls = "tile " + (side.get(pid) or "main") + (" cur" if pid == current else "")
            ac = ' aria-current="page"' if pid == current else ""
            href = home() if pid == HOME else f"{pid}.html"
            tiles.append(f'<a class="{cls}" href="{href}"{ac}><span class="nm">{e(full(p["ona"]))}<br>i {e(full(p["on"]))}</span>'
                         f'<span class="yr">{years(p["ona"])} · {years(p["on"])}</span>'
                         f'{f"<span class=side>{s}</span>" if s else ""}</a>')
        tiers.append(f'<section><h2 class="gen">{e(GEN[str(g)])}</h2><div class="tiles">{"".join(tiles)}</div></section>')
    return (f'<div class="site"><div class="wrap"><button class="burger" type="button" id="burger" aria-expanded="false" aria-controls="drawer" aria-label="Menu">'
            f'<span class="bars" aria-hidden="true"></span></button>'
            f'<a class="brand" href="{home()}"><span class="bt">{e(SITE)}</span><small>{e(SUB)}</small></a></div></div>'
            f'<div class="scrim" id="scrim" hidden></div>'
            f'<aside class="drawer" id="drawer" aria-label="Wszystkie strony" hidden>'
            f'<div class="dhead"><strong>Rodzina</strong><button class="dclose" type="button" id="dclose">Zamknij ✕</button></div>'
            f'<p class="dnote">Od najmłodszego pokolenia do najstarszego</p>{"".join(tiers)}</aside>')

# --- strona pary --------------------------------------------------------------
def facts(o, fem):
    def row(label, sym, y, key):
        if not (o.get(key + "_data") or y): return ""
        d = o.get(key + "_data") or (y if y else '[data]')
        m = o.get(key + "_miejsce")
        if m is None: m = ""
        return f'<dt>{label}</dt><dd><span class="sym">{sym}</span>{e(d)}{", " + e(m) if m else ""}</dd>'
    def parent(label, name, pid):
        if not name: return ""
        if pid in PARY:
            return f'<dt>{label}</dt><dd><a href="{pid}.html">{e(name)}</a></dd>'
        return f'<dt>{label}</dt><dd>{e(name)}</dd>'
    return ('<dl class="facts">'
            + row("Urodzona" if fem else "Urodzony", "*", o.get("ur"), "ur")
            + row("Zmarła" if fem else "Zmarł", "†", o.get("zm"), "zm")
            + "".join(f'<dt>{e(a)}</dt><dd>{e(b)}</dd>' for a, b in o.get("fakty", []))
            + parent("Ojciec", o.get("ojciec"), o.get("rodzice"))
            + parent("Matka", o.get("matka"), o.get("rodzice"))
            + '</dl>'
            + (f'<p class="factnote">{e(o["uwaga"])}</p>' if o.get("uwaga") else ''))

def person(o, fem):
    nm = full(o)
    pt = o.get("portret")
    if pt:
        cap = pt.get("podpis", nm)
        inner = (f'<div class="portrait"><img src="{e(pt["plik"])}" alt="{e(cap)}"></div>')
        data = f'data-cap="{e(cap)}" data-src="{e(pt.get("zrodlo", ""))}"'
    else:
        # strony bez portretu: bez ramki na zdjęcie profilowe
        return (f'<article class="person"><figure class="noportrait">'
                f'<figcaption><strong>{e(nm)}</strong><span>{years(o)}</span></figcaption></figure>'
                f'{facts(o, fem)}</article>')
    return (f'<article class="person"><figure>'
            f'<button class="zoom" type="button" {data} aria-label="Powiększ zdjęcie: {e(nm)}">{inner}</button>'
            f'<figcaption><strong>{e(nm)}</strong><span>{years(o)}</span></figcaption></figure>'
            f'{facts(o, fem)}</article>')

def zoom(cap, src, label, cls="", img=None):
    inner = (f'<img src="{e(img)}" alt="{e(cap)}" loading="lazy" class="{cls}">' if img
             else f'<div class="ph{(" " + cls) if cls else ""}">{label}</div>')
    return (f'<button class="zoom" type="button" data-cap="{e(cap)}" data-src="{e(src)}" aria-label="Powiększ: {e(cap)}">{inner}</button>')

def srcline(text, url=None):
    t = e(text)
    return f'<a href="{e(url)}" target="_blank" rel="noopener">{t}</a>' if url else t

def gallery(items, label="Dokumenty i zdjęcia"):
    out = []
    for it in items:
        if isinstance(it, dict):
            c, s_, l, k, f, u = it.get("podpis", ""), it.get("zrodlo", ""), it.get("etykieta", "Zdjęcie"), it.get("ksztalt", ""), it.get("plik"), it.get("url")
        else:
            (c, s_, l, k), f, u = it, None, None
        out.append(f'<figure>{zoom(c, s_, l, k, f)}<figcaption class="cap">{c}<span class="src">{srcline(s_, u)}</span></figcaption></figure>')
    return f'<div class="label">{label}</div><div class="gallery">' + "".join(out) + '</div>'

def element(el):
    if "etykieta_tekst" in el: return f'<div class="label">{e(el["etykieta_tekst"])}</div>'
    if "kolumny" in el: return '<div class="twocol">' + "".join(element(x) for x in el["kolumny"]) + '</div>'
    if "transkrypcja" in el:
        t = el["transkrypcja"]
        return (f'<blockquote class="trans"><div class="label">{e(t.get("naglowek", "Transkrypcja"))}</div>'
                + "".join(f'<div class="tl">{e(l)}</div>' for l in t["linie"])
                + (f'<p class="tnote">{e(t["uwaga"])}</p>' if t.get("uwaga") else "") + '</blockquote>')
    if "przypis" in el:
        z = el["przypis"]
        return f'<p class="srcnote">{e(z["etykieta"])} {srcline(z["tekst"], z.get("url"))}</p>'
    if "akapit" in el: return f'<p>{e(el["akapit"])}</p>'
    if "tekst_zastepczy" in el: return f'<p class="placeholder-text">{e(el["tekst_zastepczy"])}</p>'
    if "zdjecie" in el:
        z = el["zdjecie"]
        cls = "inline" + (" wide" if z.get("szeroko") else "") + (" right" if z.get("prawo") else "")
        return (f'<figure class="{cls}">{zoom(z["podpis"], z.get("zrodlo", ""), z.get("etykieta", "Miejsce na zdjęcie"), "", z.get("plik"))}'
                f'<figcaption class="cap">{e(z["podpis"])}<span class="src">{srcline(z.get("zrodlo", ""), z.get("url"))}</span></figcaption></figure>')
    if "galeria" in el: return gallery(el["galeria"], el.get("etykieta", "Dokumenty i zdjęcia"))
    return ""

def custom_story(h):
    return f'<article class="story"><h3>{e(h["tytul"])}</h3>' + "".join(element(x) for x in h["elementy"]) + '</article>'

def story(o, right):
    nm = full(o)
    return (f'<article class="story"><h3>{e(nm)}</h3>'
            f'<p class="placeholder-text">[Dzieciństwo i młodość: dom rodzinny, rodzeństwo, szkoła, praca. Tekst zastępczy, do podmiany.]</p>'
            f'<figure class="inline{" right" if right else ""}">{zoom("[Podpis: kto, gdzie, kiedy]", "[Źródło zdjęcia]", "Miejsce na zdjęcie")}'
            f'<figcaption class="cap">[Podpis zdjęcia: kto, gdzie, kiedy]<span class="src">Źródło: [album / archiwum]</span></figcaption></figure>'
            f'<p class="placeholder-text">[Kolejny akapit. Zdjęcia można wstawiać między akapitami.]</p>'
            + gallery([(f"Akt urodzenia: {e(nm)}", "Sygn. [___], nr [___/rrrr]", "Skan aktu<br>urodzenia", "doc"),
                       ("[Podpis zdjęcia]", "[rok]", "Zdjęcie", "")])
            + '</article>')

def couple_page(p):
    pid, gen = p["id"], p["pokolenie"]
    ch1, ch2 = p.get("rozdzialy", ["Zanim się poznali", "Wspólne życie"])
    title = couple_name(p)
    kids = ""
    nxt = []
    for who in ("ona", "on"):
        o = p[who]; rp = o.get("rodzice")
        if rp in PARY:
            nxt.append(f'<a href="{rp}.html"><span class="label">Rodzice: {e(full(o))}</span><strong>{e(couple_name(PARY[rp]))}</strong></a>')
        elif o.get("ojciec") and o.get("matka"):
            nxt.append(f'<span class="none"><span class="label">Rodzice: {e(full(o))}</span>{e(o["ojciec"])} i {e(o["matka"])}</span>')
    for k in [k for k in p.get("dzieci", []) if k.get("strona")]:
        nxt.append(f'<a class="down" href="{url(k["strona"])}"><span class="label">Ich dziecko: {e(k["imie"])}</span>'
                   f'<strong>{e(couple_name(PARY[k["strona"]]))}</strong></a>')
    kids_html = ""
    if p.get("lista_dzieci"):
        parts = []
        for k in p["lista_dzieci"]:
            if k.get("grupa"):
                parts.append(f'<li class="grp">{e(k["grupa"])}</li>')
            else:
                nm = e(k["imie"])
                if k.get("strona"): nm = f'<a href="{url(k["strona"])}">{nm}</a>'
                parts.append(f'<li><strong>{nm}</strong>' + (f' <span>{e(k["opis"])}</span>' if k.get("opis") else '') + '</li>')
        kids_html = f'<section class="chapter" id="dzieci"><h2>Dzieci</h2><ul class="kidlist">{"".join(parts)}</ul></section>'
    elif p.get("dzieci_lista"):
        items = "".join(f'<li><strong>{e(k["imie"])}</strong> <span>{e(k["opis"])}</span></li>' for k in p["dzieci"])
        kids_html = f'<section class="chapter" id="dzieci"><h2>Dzieci</h2><ul class="kidlist">{items}</ul></section>'
    elif p.get("dzieci"):
        items = "".join('<li><strong>' + (f'<a href="{url(k["strona"])}">{e(k["imie"])}</a>' if k.get("strona") else e(k["imie"])) + '</strong></li>' for k in p["dzieci"])
        kids_html = f'<section class="chapter" id="dzieci"><h2>Dzieci</h2><ul class="kidlist">{items}</ul></section>'
    def shared_default():
        return f'''<article class="story"><h3>Wspólna historia</h3>
      <p class="placeholder-text">[Jak i gdzie się poznali. Tekst zastępczy, do podmiany.]</p>
      <div class="twocol">
        <figure class="inline">{zoom("[Zdjęcie ślubne, miejsce, data]", "[Źródło]", "Miejsce na zdjęcie<br>ślubne")}<figcaption class="cap">[Zdjęcie ślubne, miejsce, data]<span class="src">Źródło: [album]</span></figcaption></figure>
        <figure class="inline">{zoom("Akt małżeństwa", "Sygn. [___], nr [___/rrrr]", "Skan aktu<br>małżeństwa")}<figcaption class="cap">Akt małżeństwa<span class="src">Sygn. [___], nr [___/rrrr]</span></figcaption></figure>
      </div>
      <p class="placeholder-text">[Dalsze lata: gdzie zamieszkali, praca, dzieci, ważne wydarzenia.]</p>
      {gallery([("[Podpis zdjęcia]", "[rok]", "Zdjęcie", ""), ("[Podpis zdjęcia]", "[rok]", "Zdjęcie", ""), ("Akt zgonu", "Sygn. [___]", "Skan aktu<br>zgonu", "doc")])}
    </article>'''
    tresc = p.get("tresc") or []
    chap = []
    for c in tresc:
        parts = []
        for h in c["historie"]:
            sz = h.get("szablon")
            if sz == "ona": parts.append(story(p["ona"], True))
            elif sz == "on": parts.append(story(p["on"], False))
            elif sz == "wspolna": parts.append(shared_default())
            else: parts.append(custom_story(h))
        chap.append(f'<section class="chapter"><h2>{e(c["tytul"])}</h2>{f'<div class="years">{e(c["lata"])}</div>' if c.get("lata") else ""}{"".join(parts)}</section>')
    chapters_html = "".join(chap)
    body = f'''
<div class="wrap page">
  {"" if pid == HOME else f'<div class="crumbs"><a href="{home()}">Strona główna</a> › {e(GEN[str(gen)])} › {e(title)}</div>'}
  <header class="title">
    <div class="series">Historia rodziny · {e(GEN[str(gen)])}</div>
    <h1>{e(title)}</h1>
    {f'<p class="sub">{e(p["podtytul"])}</p>' if p.get("podtytul") else ""}
  </header>
  <section class="pair" aria-label="{e(title)}">{person(p["ona"], True)}{person(p["on"], False)}</section>
  {chapters_html}
  {kids_html}
  <section class="chapter"><h2>Dalej w drzewie</h2><div class="next">{"".join(nxt)}</div></section>
  <footer><span>{e(SITE)}</span><a href="{home()}">Strona główna</a></footer>
</div>
<dialog id="lightbox" aria-label="Powiększenie"><div class="ph" id="lb-img"></div>
  <div class="bar"><figcaption class="cap"><span id="lb-cap"></span><span class="src" id="lb-src"></span></figcaption>
  <button class="close" type="button" id="lb-close">Zamknij</button></div></dialog>'''
    return f'{title} · {SITE}', nav(pid) + body

import re as _re
def _ver_img(html):
    def rep(m):
        f = OUT / m.group(2)
        v = _h.md5(f.read_bytes()).hexdigest()[:8] if f.exists() else ""
        return f'{m.group(1)}="{m.group(2)}?v={v}"' if v else m.group(0)
    return _re.sub(r'(src)="((?:skany|zdjecia)/[^"?]+)"', rep, html)

# --- zapis -------------------------------------------------------------------
def doc(title, body):
    return (f'<!doctype html>\n<html lang="pl"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            f'<title>{e(title)}</title>{FONTS}<link rel="stylesheet" href="styl.css?v={VCSS}"></head>'
            f'<body>{body}<script src="strona.js?v={VJS}"></script></body></html>\n')

def fragment(title, body):  # wersja do podglądu w Claude (bez własnego <html>)
    return (f'<title>{e(title)}</title><meta name="claude:viewport-fit-sides" content="cover">'
            f'{FONTS}<link rel="stylesheet" href="styl.css?v={VCSS}">{body}<script src="strona.js?v={VJS}"></script>\n')

OUT.mkdir(exist_ok=True)
(OUT / ".nojekyll").write_text("", encoding="utf-8")
for f in ("styl.css", "strona.js"): shutil.copy(SRC / "zasoby" / f, OUT / f)
for f in OUT.glob("*.html"): f.unlink()
for p in data["pary"]:
    t, b = couple_page(p)
    name = "index.html" if p["id"] == HOME else f'{p["id"]}.html'
    (OUT / name).write_text(_ver_img(doc(t, b)), encoding="utf-8")
    if p["id"] == HOME and len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(fragment(SITE, b), encoding="utf-8")
print("Zbudowano", len(data["pary"]), "stron w", OUT)
