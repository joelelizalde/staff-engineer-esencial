#!/usr/bin/env python3
"""Genera el sitio estático de «System Design · Volumen 2 · Edición esencial».

Uso:
    python3 build_site.py

Escribe index.html, las 28 páginas de lección/evaluación, glosario.html
y progreso.html en la raíz del proyecto. No necesita dependencias externas.
"""

import html
import json
import os
import re
import unicodedata
from contenido import COURSE, GLOSARIO, MODULES

ROOT = os.path.dirname(os.path.abspath(__file__))
INK = "#14171C"
MUTED = "#6D7480"
LINE = "#BFC5CF"
SURFACE = "#FDFDFB"
ACCENT = "#2E5F8A"
TEAL = "#8A5A2B"
FONT = "Inter, Arial, sans-serif"

TOTAL = sum(len(m["lessons"]) + 1 for m in MODULES)
N_LESSONS = sum(len(m["lessons"]) for m in MODULES)
N_DIAGRAMS = sum(1 for m in MODULES for l in m["lessons"] if l.get("diagram"))
TOTAL_MIN = sum(l["minutes"] for m in MODULES for l in m["lessons"]) + 10 * len(MODULES)


# ---------------------------------------------------------------- utilidades
def esc(text):
    return html.escape(str(text), quote=True)


def slug(text):
    s = unicodedata.normalize("NFD", text)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "seccion"


def plain(text):
    return re.sub(r"<[^>]+>", "", text)


def words(text):
    return len(re.findall(r"[\wÁÉÍÓÚÜÑáéíóúüñ]+", plain(text)))


def lesson_words(lesson):
    n = words(lesson["lead"])
    for sec in lesson["sections"]:
        for p in sec["p"]:
            n += words(p)
    n += sum(words(k) for k in lesson["keys"])
    n += words(lesson["example"]) + words(lesson["caution"])
    return n


def hours_label(minutes):
    h = minutes / 60
    return ("%.1f h" % h).replace(".", ",")


def flat_items():
    items = []
    for m in MODULES:
        for l in m["lessons"]:
            items.append({
                "id": l["id"], "num": l["lnum"], "lnum": l["lnum"],
                "title": l["title"], "href": l["id"] + ".html",
                "kind": "lesson", "search": l["search"], "mod": m["num"],
                "modTitle": m["title"], "minutes": l["minutes"],
            })
        q = m["quiz"]
        items.append({
            "id": q["id"], "num": len(m["lessons"]) + 1,
            "lnum": len(m["lessons"]) + 1,
            "title": q["title"], "href": q["id"] + ".html",
            "kind": "quiz", "search": q["search"], "mod": m["num"],
            "modTitle": m["title"], "minutes": 10,
        })
    return items


ITEMS = flat_items()
BY_ID = {i["id"]: i for i in ITEMS}
for idx, it in enumerate(ITEMS):
    it["index"] = idx
    it["prev"] = ITEMS[idx - 1] if idx > 0 else None
    it["next"] = ITEMS[idx + 1] if idx + 1 < len(ITEMS) else None


def data_blob(current=None):
    mods = []
    for m in MODULES:
        entries = []
        for it in ITEMS:
            if it["mod"] == m["num"]:
                entries.append({
                    "id": it["id"], "num": it["num"], "lnum": it["lnum"],
                    "title": it["title"], "href": it["href"],
                    "kind": it["kind"], "search": it["search"],
                })
        mods.append({"num": m["num"], "title": m["title"], "lessons": entries})
    cur = BY_ID.get(current)
    nxt = cur["next"] if cur else None
    prv = cur["prev"] if cur else None
    payload = {
        "total": TOTAL, "current": current,
        "next": {"title": nxt["title"], "href": nxt["href"]} if nxt else None,
        "prev": {"title": prv["title"], "href": prv["href"]} if prv else None,
        "modules": mods,
    }
    blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return blob.replace("</", "<\\/")


# ---------------------------------------------------------------- iconos
ICON_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"></path></svg>'
ICON_SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="7"></circle><path d="m16.5 16.5 4 4"></path></svg>'
ICON_MOON = '<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4 8.5 8.5 0 1 0 20 14.5Z"></path></svg>'
ICON_SUN = '<svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"></path></svg>'
ICON_ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'
ICON_BACK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M11 18l-6-6 6-6"></path></svg>'
ICON_DOWN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M7 10l5 5 5-5M4 20h16"></path></svg>'
ICON_CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="12" cy="12" r="8.5"></circle><path d="M12 7.5V12l3 1.8"></path></svg>'
ICON_BOOK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21.5Z"></path><path d="M4 5.5v16M8 7h8M8 11h6"></path></svg>'
ICON_GRID = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><rect x="4" y="4" width="6" height="6" rx="1"></rect><rect x="14" y="4" width="6" height="6" rx="1"></rect><rect x="4" y="14" width="6" height="6" rx="1"></rect><rect x="14" y="14" width="6" height="6" rx="1"></rect></svg>'
ICON_CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m4 12.5 5 5L20 6.5"></path></svg>'


# ---------------------------------------------------------------- diagramas
def _arrow(x1, y1, x2, y2, color=LINE):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="2"/>'
            f'<polygon points="{x2:.1f},{y2:.1f} {x2-7:.1f},{y2-4.5:.1f} {x2-7:.1f},{y2+4.5:.1f}" fill="{color}"/>')


def diag_flow(labels):
    n = len(labels)
    margin, gap, h, y = 26, 26, 88, 34
    bw = (840 - 2 * margin - gap * (n - 1)) / n
    out = [f'<svg viewBox="0 0 840 160" role="img" aria-label="Diagrama de flujo: {" a ".join(esc(l) for l in labels)}">']
    for i, label in enumerate(labels):
        x = margin + i * (bw + gap)
        last = i == n - 1
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="{h}" rx="10" '
                   f'fill="{SURFACE}" stroke="{ACCENT if last else LINE}" stroke-width="{2 if last else 1.4}"/>')
        fs = 15 if len(label) <= 18 else 13
        out.append(f'<text x="{x + bw/2:.1f}" y="{y + h/2 + 5:.1f}" font-family="{FONT}" '
                   f'font-size="{fs}" font-weight="600" fill="{INK}" text-anchor="middle">{esc(label)}</text>')
        if not last:
            x1 = x + bw + 5
            x2 = x + bw + gap - 5
            out.append(_arrow(x1, y + h / 2, x2, y + h / 2))
    out.append("</svg>")
    return "".join(out)


def diag_stack(labels):
    n = len(labels)
    rh, gap = 25, 8
    total = n * rh + (n - 1) * gap
    top = (170 - total) / 2
    out = [f'<svg viewBox="0 0 840 170" role="img" aria-label="Diagrama de capas: {" → ".join(esc(l) for l in labels)}">']
    for i, label in enumerate(labels):
        y = top + i * (rh + gap)
        last = i == n - 1
        out.append(f'<rect x="220" y="{y:.1f}" width="400" height="{rh}" rx="7" fill="{SURFACE}" '
                   f'stroke="{ACCENT if last else LINE}" stroke-width="{1.8 if last else 1.2}"/>')
        out.append(f'<rect x="220" y="{y:.1f}" width="4" height="{rh}" rx="2" fill="{ACCENT if last else LINE}"/>')
        out.append(f'<text x="420" y="{y + rh/2 + 4.5:.1f}" font-family="{FONT}" font-size="13" '
                   f'font-weight="500" fill="{INK}" text-anchor="middle">{esc(label)}</text>')
    out.append("</svg>")
    return "".join(out)


def diag_loop(labels):
    pos = [(420, 28), (668, 85), (420, 142), (172, 85)]
    bw, bh = 176, 42
    out = ['<svg viewBox="0 0 840 170" role="img" aria-label="Diagrama de bucle de entrenamiento">']
    out.append(f'<circle cx="420" cy="85" r="30" fill="none" stroke="{LINE}" stroke-width="1.2" stroke-dasharray="3 4"/>')
    out.append(f'<text x="420" y="82" font-family="{FONT}" font-size="9" font-weight="600" fill="{MUTED}" text-anchor="middle" letter-spacing="1">ITERA</text>')
    out.append(f'<text x="420" y="94" font-family="{FONT}" font-size="9" font-weight="600" fill="{MUTED}" text-anchor="middle" letter-spacing="1">CIÓN</text>')
    for i, label in enumerate(labels[:4]):
        cx, cy = pos[i]
        x, y = cx - bw / 2, cy - bh / 2
        out.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="9" fill="{SURFACE}" '
                   f'stroke="{ACCENT if i == 0 else LINE}" stroke-width="{1.8 if i == 0 else 1.3}"/>')
        out.append(f'<text x="{cx}" y="{cy + 4.5}" font-family="{FONT}" font-size="13" font-weight="600" '
                   f'fill="{INK}" text-anchor="middle">{esc(label)}</text>')
    arrows = [
        (512, 38, 578, 62), (656, 110, 514, 138),
        (328, 138, 266, 110), (188, 62, 326, 38),
    ]
    out.append(f'<defs><marker id="lp-arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" fill="{MUTED}"/></marker></defs>')
    for x1, y1, x2, y2 in arrows:
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{MUTED}" stroke-width="1.7" '
                   f'marker-end="url(#lp-arrow)"/>')
    out.append("</svg>")
    return "".join(out)


def diag_attention(tokens):
    n = len(tokens)
    pw, gap = 96, 8
    total = n * pw + (n - 1) * gap
    x0 = (840 - total) / 2
    out = ['<svg viewBox="0 0 840 176" role="img" aria-label="Atención de la última posición sobre el contexto">']
    centers = []
    for i, tok in enumerate(tokens):
        x = x0 + i * (pw + gap)
        centers.append(x + pw / 2)
    qx = centers[-1]
    for i, cx in enumerate(centers[:-1]):
        strength = 0.18 + 0.62 * (i / max(1, n - 2))
        width = 1.1 + 2.2 * (i / max(1, n - 2))
        out.append(f'<path d="M {qx - 2:.1f} 118 C {qx - 2:.1f} 34, {cx + 2:.1f} 34, {cx + 2:.1f} 112" '
                   f'fill="none" stroke="{ACCENT}" stroke-opacity="{strength:.2f}" stroke-width="{width:.2f}"/>')
    for i, tok in enumerate(tokens):
        x = x0 + i * (pw + gap)
        last = i == n - 1
        out.append(f'<rect x="{x:.1f}" y="118" width="{pw}" height="34" rx="8" fill="{SURFACE}" '
                   f'stroke="{ACCENT if last else LINE}" stroke-width="{1.8 if last else 1.2}"/>')
        out.append(f'<text x="{x + pw/2:.1f}" y="140" font-family="{FONT}" font-size="12.5" '
                   f'font-weight="500" fill="{INK}" text-anchor="middle">{esc(tok)}</text>')
    out.append(f'<text x="{qx:.1f}" y="18" font-family="{FONT}" font-size="9.5" font-weight="600" '
               f'fill="{MUTED}" text-anchor="middle" letter-spacing="1">CONSULTA</text>')
    out.append("</svg>")
    return "".join(out)


def diag_matrix(spec):
    rows = int(spec.get("rows", 5))
    cols = int(spec.get("cols", 8))
    mark = int(spec.get("mark", 0))
    cw = max(34, min(52, int(400 / max(1, cols))))
    ch, gap = 24, 5
    gw = cols * cw + (cols - 1) * gap
    gh = rows * ch + (rows - 1) * gap
    x0 = (840 - gw) / 2 + 12
    y0 = (162 - gh) / 2
    out = ['<svg viewBox="0 0 840 170" role="img" aria-label="Matriz de tokens por dimensiones">']
    for r in range(rows):
        out.append(f'<text x="{x0-12}" y="{y0 + r*(ch+gap) + ch/2 + 4:.1f}" font-family="{FONT}" font-size="9" '
                   f'fill="{MUTED}" text-anchor="end">{r+1}</text>')
    for c in range(cols):
        out.append(f'<text x="{x0 + c*(cw+gap) + cw/2:.1f}" y="{y0-8:.1f}" font-family="{FONT}" font-size="9" '
                   f'fill="{MUTED}" text-anchor="middle">{c+1}</text>')
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            hot = idx == mark
            out.append(f'<rect x="{x0 + c*(cw+gap):.1f}" y="{y0 + r*(ch+gap):.1f}" width="{cw}" height="{ch}" rx="4" '
                       f'fill="{ACCENT if hot else SURFACE}" stroke="{ACCENT if hot else LINE}" stroke-width="{1.5 if hot else 1}"/>')
    out.append("</svg>")
    return "".join(out)


def diag_curve(spec):
    out = ['<svg viewBox="0 0 840 184" role="img" aria-label="Curvas de pérdida de entrenamiento y validación">']
    left, right, top, bottom = 62, 790, 26, 142
    out.append(f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="{LINE}" stroke-width="1.3"/>')
    out.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="{LINE}" stroke-width="1.3"/>')
    train = [(left, top + 18), (210, top + 56), (380, top + 80), (550, top + 92), (720, top + 98)]
    val = [(left, top + 18), (210, top + 52), (380, top + 66), (550, top + 80), (720, top + 106)]
    def poly(pts, color, dash=""):
        d = " ".join(("M" if i == 0 else "L") + f" {x:.1f} {y:.1f}" for i, (x, y) in enumerate(pts))
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.2"{extra}/>'
    out.append(poly(train, ACCENT))
    out.append(poly(val, TEAL, "5 4"))
    for x, y in train:
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{ACCENT}"/>')
    for x, y in val:
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{TEAL}"/>')
    out.append(f'<text x="{left}" y="168" font-family="{FONT}" font-size="10" fill="{MUTED}" text-anchor="start">{esc(spec.get("x", "épocas"))}</text>')
    out.append(f'<text x="{left-8}" y="{top+4}" font-family="{FONT}" font-size="10" fill="{MUTED}" text-anchor="end">{esc(spec.get("y", "pérdida"))}</text>')
    out.append(f'<rect x="560" y="24" width="10" height="3" rx="1.5" fill="{ACCENT}"/>')
    out.append(f'<text x="578" y="29" font-family="{FONT}" font-size="10" fill="{INK}">{esc(spec.get("a", "entrenamiento"))}</text>')
    out.append(f'<rect x="680" y="24" width="10" height="3" rx="1.5" fill="{TEAL}"/>')
    out.append(f'<text x="698" y="29" font-family="{FONT}" font-size="10" fill="{INK}">{esc(spec.get("b", "validación"))}</text>')
    out.append("</svg>")
    return "".join(out)


def diag_latency(spec):
    out = ['<svg viewBox="0 0 840 184" role="img" aria-label="Latencia p50 estable frente a p99 que se dispara">']
    left, right, top, bottom = 62, 790, 26, 142
    out.append(f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="{LINE}" stroke-width="1.3"/>')
    out.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="{LINE}" stroke-width="1.3"/>')
    xs = [left, 170, 285, 400, 515, 630, 720]
    p50 = [108, 107, 109, 108, 110, 109, 108]
    p99 = [104, 96, 78, 60, 44, 38, 74]
    def poly(pts, color, dash=""):
        d = " ".join(("M" if i == 0 else "L") + f" {x:.1f} {y:.1f}" for i, (x, y) in enumerate(zip(xs, pts)))
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.2"{extra}/>'
    out.append(poly(p50, TEAL))
    out.append(poly(p99, ACCENT, "5 4"))
    for x, y in zip(xs, p50):
        out.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="{TEAL}"/>')
    for x, y in zip(xs, p99):
        out.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="{ACCENT}"/>')
    out.append(f'<text x="{left}" y="168" font-family="{FONT}" font-size="10" fill="{MUTED}" text-anchor="start">{esc(spec.get("x", "tiempo"))}</text>')
    out.append(f'<text x="{left-8}" y="{top+4}" font-family="{FONT}" font-size="10" fill="{MUTED}" text-anchor="end">{esc(spec.get("y", "latencia"))}</text>')
    out.append(f'<rect x="560" y="24" width="10" height="3" rx="1.5" fill="{TEAL}"/>')
    out.append(f'<text x="578" y="29" font-family="{FONT}" font-size="10" fill="{INK}">p50</text>')
    out.append(f'<rect x="680" y="24" width="10" height="3" rx="1.5" fill="{ACCENT}"/>')
    out.append(f'<text x="698" y="29" font-family="{FONT}" font-size="10" fill="{INK}">p99</text>')
    out.append("</svg>")
    return "".join(out)


def diag_bars(pairs):
    n = len(pairs)
    bw, gap = 84, 52
    total = n * bw + (n - 1) * gap
    x0 = (840 - total) / 2
    base, maxh = 140, 88
    out = ['<svg viewBox="0 0 840 184" role="img" aria-label="Barras comparativas de métricas">']
    out.append(f'<line x1="{x0-20}" y1="{base}" x2="{x0+total+20}" y2="{base}" stroke="{LINE}" stroke-width="1.3"/>')
    for i, (label, value) in enumerate(pairs):
        x = x0 + i * (bw + gap)
        h = max(4, float(value) * maxh)
        color = ACCENT if i == 0 else TEAL
        out.append(f'<rect x="{x:.1f}" y="{base-h:.1f}" width="{bw}" height="{h:.1f}" rx="6" fill="{color}" opacity="0.9"/>')
        out.append(f'<text x="{x + bw/2:.1f}" y="{base-h-8:.1f}" font-family="{FONT}" font-size="11" font-weight="600" fill="{INK}" text-anchor="middle">{int(round(float(value)*100))}%</text>')
        out.append(f'<text x="{x + bw/2:.1f}" y="{base+18:.1f}" font-family="{FONT}" font-size="10.5" fill="{MUTED}" text-anchor="middle">{esc(label)}</text>')
    out.append("</svg>")
    return "".join(out)


def render_diagram(spec, caption):
    kind = spec[0]
    data = spec[1] if len(spec) > 1 else None
    if kind == "flow":
        svg = diag_flow(data)
    elif kind == "stack":
        svg = diag_stack(data)
    elif kind == "loop":
        svg = diag_loop(data)
    elif kind == "attention":
        svg = diag_attention(data)
    elif kind == "matrix":
        svg = diag_matrix(data or {})
    elif kind == "curve":
        svg = diag_curve(data or {})
    elif kind == "latency":
        svg = diag_latency(data or {})
    elif kind == "bars":
        svg = diag_bars(data)
    else:
        raise ValueError("tipo de diagrama desconocido: " + kind)
    cap = f"<figcaption>{esc(caption)}</figcaption>" if caption else ""
    return f'<figure class="diagram">{svg}{cap}</figure>'


# ---------------------------------------------------------------- chrome
def brand(href="index.html"):
    return (f'<a class="brand" href="{href}">\n'
            f'  <span class="brand-mark">{esc(COURSE["brand"])}</span>\n'
            f'  <span class="brand-text"><strong>{esc(COURSE["title"])}</strong><span>{esc(COURSE["subtitle"])}</span></span>\n'
            f'</a>')


def sidebar(current=None):
    cur = BY_ID.get(current)
    cur_mod = cur["mod"] if cur else None
    parts = ['<aside class="sidebar" id="sidebar" aria-label="Temario del curso">', brand()]
    parts.append('<div class="side-progress"><div class="side-progress-top">'
                 '<svg class="ring" viewBox="0 0 46 46" aria-hidden="true"><circle class="ring-bg" cx="23" cy="23" r="18"></circle><circle class="ring-fg" data-ring cx="23" cy="23" r="18"></circle></svg>'
                 f'<div class="side-progress-text"><strong><span data-done-count>0</span> de {TOTAL} pasos</strong><span>Tu avance</span></div>'
                 '</div></div>')
    parts.append(f'<nav class="side-nav"><div class="nav-label">Temario · {len(MODULES)} módulos</div>')
    for m in MODULES:
        is_cur = m["num"] == cur_mod
        parts.append(f'<details class="mod" data-module="{m["num"]}"{" open" if is_cur else ""}'
                     f'{" data-current=\"true\"" if is_cur else ""}>')
        parts.append('<summary>')
        parts.append(f'  <span class="mod-num">{m["num"]}</span>')
        parts.append(f'  <span class="mod-name">{esc(m["title"])}</span>')
        parts.append(f'  <span class="mod-count" data-modcount="{m["num"]}">0/{len(m["lessons"]) + 1}</span>')
        parts.append(f'  <span class="mod-bar" aria-hidden="true"><i data-modbar="{m["num"]}"></i></span>')
        parts.append('</summary>')
        parts.append('<ol class="lessons">')
        for l in m["lessons"]:
            cls = "lesson-link"
            aria = ""
            if l["id"] == current:
                cls += " is-current"
                aria = ' aria-current="page"'
            parts.append(f'<li><a class="{cls}" data-lesson="{l["id"]}" href="{l["id"]}.html"{aria}>'
                         f'<span class="ln">{m["num"]}.{l["lnum"]}</span><span class="lt">{esc(l["title"])}</span><span class="dot" aria-hidden="true"></span></a></li>')
        q = m["quiz"]
        cls = "lesson-link quiz"
        aria = ""
        if q["id"] == current:
            cls += " is-current"
            aria = ' aria-current="page"'
        parts.append(f'<li><a class="{cls}" data-lesson="{q["id"]}" href="{q["id"]}.html"{aria}>'
                     f'<span class="ln">{m["num"]}.{len(m["lessons"]) + 1}</span><span class="lt">{esc(q["title"])}</span><span class="dot" aria-hidden="true"></span></a></li>')
        parts.append('</ol></details>')
    parts.append('</nav>')
    parts.append('<div class="side-foot">'
                 '<a href="glosario.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21.5Z"></path><path d="M4 5.5v16"></path></svg> Glosario</a>'
                 '<a href="progreso.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 19V9M10 19V5M16 19v-7M22 19H2"></path></svg> Mi progreso</a>'
                 f'<a href="{COURSE["pdf"]}">{ICON_DOWN.replace("<svg", "<svg width=\"15\" height=\"15\"")} Manual en PDF</a>'
                 f'<div class="edition">{esc(COURSE["brand"])} · {esc(COURSE["year"])}</div>'
                 '</div>')
    parts.append('</aside>')
    return "\n".join(parts)


def topbar(crumbs, with_menu=True):
    menu = (f'<button class="icon-btn menu-btn" type="button" data-menu-toggle aria-label="Abrir el temario" '
            f'aria-controls="sidebar" aria-expanded="false">{ICON_MENU}</button>') if with_menu else ""
    crumb_html = '<span class="sep">/</span>'.join(crumbs)
    return (f'<header class="topbar">\n  {menu}\n'
            f'  <nav class="crumbs" aria-label="Migas de pan">{crumb_html}</nav>\n'
            '  <div class="top-actions">\n'
            f'    <button class="search-btn" type="button" data-search-open aria-label="Buscar en el curso">{ICON_SEARCH}<span>Buscar</span><kbd>⌘K</kbd></button>\n'
            f'    <button class="icon-btn" type="button" data-theme-toggle aria-label="Cambiar tema">{ICON_MOON}{ICON_SUN}</button>\n'
            '  </div>\n'
            '  <div class="readbar" data-readbar></div>\n'
            '</header>')


def searchbox_and_toast():
    return ('<div class="searchbox" data-search role="dialog" aria-modal="true" aria-label="Buscar en el curso">\n'
            '  <div class="search-panel">\n'
            f'    <div class="search-top">{ICON_SEARCH}<input class="search-input" type="search" placeholder="Busca una lección o un tema…" aria-label="Buscar una lección o un tema" autocomplete="off"><button class="search-close" type="button" data-search-close>ESC</button></div>\n'
            '    <div class="search-results"></div>\n'
            '    <div class="sr-hint"><span>↑ ↓ para navegar · Enter para abrir</span><span>Esc para cerrar</span></div>\n'
            '  </div>\n'
            '</div>\n'
            '<div class="toast" data-toast role="status" aria-live="polite"></div>')


def page_head(title, desc, body_class, theme_key, current=None, sidebar_html=None):
    return f'''<!DOCTYPE html>
<html lang="es" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#f5f1e8">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="css/curso.css">
<script>(function(){{try{{var t=localStorage.getItem('{theme_key}');if(!t){{t=window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}}document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}}})();</script>
</head>
<body class="{body_class}">
<a class="skip" href="#contenido">Saltar al contenido</a>
{sidebar_html if sidebar_html is not None else sidebar(current)}
<div class="overlay" data-overlay></div>'''


# ---------------------------------------------------------------- lecciones
def render_lesson(module, lesson, item, toc_ids):
    mnum = module["num"]
    body = []
    body.append('<div class="lesson-wrap">')
    body.append('  <article class="lesson">')
    body.append('    <header>')
    body.append(f'  <div class="kicker">Módulo {mnum} · Lección {lesson["lnum"]} de {len(module["lessons"])}</div>')
    body.append(f'  <h1>{esc(lesson["title"])}</h1>')
    wc = lesson_words(lesson)
    body.append('  <div class="lesson-meta">'
                f'<span>{ICON_CLOCK} {lesson["minutes"]} min de lectura</span>'
                f'<span>{ICON_BOOK} {wc} palabras</span>'
                f'<span>{ICON_GRID} {len(lesson["sections"])} apartados</span></div>')
    body.append('</header>')
    body.append('    <div class="brief">')
    body.append('  <div class="brief-k">En esta lección</div>')
    body.append('  <div><ul>' + ''.join(f'<li>{esc(b)}</li>' for b in lesson["brief"]) + '</ul>'
                '<p>Lee de principio a fin; al terminar, el botón inferior te lleva directo a la siguiente lección.</p></div>')
    body.append('</div>')
    body.append('<div class="prose">')
    body.append(f'<p class="lead">{esc(lesson["lead"])}</p>')
    body.append(render_diagram(lesson["diagram"], lesson.get("caption", "")))
    for sec in lesson["sections"]:
        hid = slug(sec["h"])
        toc_ids.append((hid, sec["h"], 2))
        body.append(f'<h2 id="{hid}">{esc(sec["h"])}</h2>')
        for p in sec["p"]:
            body.append(f'<p>{esc(p)}</p>')
    toc_ids.append(("ideas-clave", "Ideas clave", 2))
    body.append('<aside class="lesson-extra keypoints"><h2 id="ideas-clave">Ideas clave</h2><ul>'
                + ''.join(f'<li>{esc(k)}</li>' for k in lesson["keys"]) + '</ul></aside>')
    toc_ids.append(("caso", "Caso concreto", 2))
    body.append(f'<aside class="lesson-extra example"><h2 id="caso">Caso concreto</h2><p>{esc(lesson["example"])}</p></aside>')
    toc_ids.append(("cuidado", "Cuidado", 2))
    body.append(f'<aside class="lesson-extra caution"><h2 id="cuidado">Cuidado</h2><p>{esc(lesson["caution"])}</p></aside>')
    body.append('</div>')
    body.append(finish_section(item, lesson["title"], is_quiz=False))
    body.append('  </article>')
    body.append(render_toc(toc_ids))
    body.append('</div>')
    return "\n".join(body)


def finish_section(item, prev_title, is_quiz=False):
    nxt = item["next"]
    prv = item["prev"]
    if nxt:
        eyebrow = "Siguiente lección"
        h2 = nxt["title"]
        text = ("La evaluación se da por superada cuando aciertas al menos 2 de 3. Si prefieres, puedes seguir sin responder."
                if is_quiz else
                "Continúa la lectura sin volver al índice. También puedes usar la flecha → del teclado.")
        actions = []
        if is_quiz:
            actions.append(f'<a class="btn btn-cream" href="{nxt["href"]}">Siguiente lección {ICON_ARROW}</a>')
            actions.append(f'<a class="quiet" href="{nxt["href"]}">Saltar sin completar</a>')
        else:
            actions.append(f'<a class="btn btn-cream" href="{nxt["href"]}" data-complete-link="{item["id"]}">Completar y seguir {ICON_ARROW}</a>')
            actions.append(f'<a class="quiet" href="{nxt["href"]}">Saltar sin completar</a>')
    else:
        eyebrow = "Fin del recorrido"
        h2 = "Has construido el mapa completo"
        text = "Vuelve al temario para repasar, revisa el glosario o descarga el manual en PDF para consultarlo sin conexión."
        actions = [f'<a class="btn btn-cream" href="progreso.html">Revisar mi progreso {ICON_ARROW}</a>',
                   '<a class="quiet" href="index.html">Volver al temario</a>']
    prev_link = ""
    if prv:
        prev_link = (f'<div class="finish-prev"><a href="{prv["href"]}">{ICON_BACK} Anterior: {esc(prv["title"])}</a></div>')
    return ('    <section class="finish">\n'
            f'  <div class="eyebrow">{eyebrow}</div>\n'
            f'  <h2>{esc(h2)}</h2>\n'
            f'  <p>{text}</p>\n'
            '  <div class="finish-actions">\n    ' + "\n    ".join(actions) + '\n  </div>\n'
            f'  {prev_link}\n'
            '</section>')


def render_toc(toc_ids):
    links = []
    seen = set()
    for hid, label, lvl in toc_ids:
        if hid in seen:
            continue
        seen.add(hid)
        cls = ' class="lvl3"' if lvl == 3 else ""
        links.append(f'<a{cls} href="#{hid}">{esc(label)}</a>')
    return ('<aside class="toc" aria-label="En esta página"><div class="toc-label">En esta página</div>'
            + ''.join(links) + '</aside>')


def render_quiz(module, quiz, item, toc_ids):
    mnum = module["num"]
    n = len(quiz["questions"])
    need = (n * 2 + 2) // 3
    body = []
    body.append('<div class="lesson-wrap">')
    body.append('  <article class="lesson">')
    body.append('    <header>')
    body.append(f'  <div class="kicker">Módulo {mnum} · Evaluación</div>')
    body.append(f'  <h1>{esc(quiz["title"])}</h1>')
    body.append('  <div class="lesson-meta">'
                f'<span>{ICON_CLOCK} 10 min</span>'
                f'<span>{ICON_BOOK} {n} preguntas</span>'
                f'<span>{ICON_CHECK} {need}/{n} para aprobar</span></div>')
    body.append('</header>')
    body.append('    <div class="brief">')
    body.append('  <div class="brief-k">Evaluación</div>')
    body.append('  <div><ul><li>Resumen del capítulo</li>'
                f'<li>{n} preguntas de comprensión</li><li>Ejercicios aplicados</li></ul>'
                f'<p>Necesitas {need} de {n} respuestas correctas para dar el módulo por consolidado.</p></div>')
    body.append('</div>')
    body.append('<div class="prose"><h2 id="resumen">Resumen del módulo</h2>')
    for p in quiz["summary"]:
        body.append(f'<p>{esc(p)}</p>')
    body.append('</div>')
    toc_ids.append(("resumen", "Resumen del capítulo", 2))
    toc_ids.append(("evaluacion", "Evaluación", 2))

    body.append(f'<section class="exam" id="evaluacion" data-exam="{quiz["id"]}">')
    body.append(f'<div class="exam-head"><h2>Evaluación del módulo {mnum}</h2><span>{n} preguntas · sin límite de tiempo</span></div>')
    for qi, q in enumerate(quiz["questions"]):
        body.append(f'<div class="q" data-answer="{q["answer"]}" data-why="{esc(q["why"])}">')
        body.append(f'  <div class="q-h"><span class="q-n">{qi+1:02d}</span><p class="q-t">{esc(q["q"])}</p></div>')
        body.append('  <div class="opts">')
        for oi, opt in enumerate(q["options"]):
            name = f'{quiz["id"]}-q{qi}'
            body.append(f'<label class="opt"><input type="radio" name="{name}" value="{oi}"><span>{esc(opt)}</span></label>')
        body.append('</div>')
        body.append('  <div class="fb" role="status"></div>')
        body.append('</div>')
    body.append('<div class="exam-foot">')
    body.append(f'  <span class="exam-score" data-score><b>0 / {n}</b> correctas</span>')
    body.append('  <button class="btn btn-ink" type="button" data-check>Comprobar respuestas</button>')
    body.append('  <button class="btn btn-line" type="button" data-retry hidden>Reintentar</button>')
    body.append('</div>')
    body.append('<div class="exam-pass" role="status"></div>')
    body.append('</section>')

    toc_ids.append(("ejercicios", "Ejercicios", 2))
    body.append('<section class="prose" id="ejercicios" style="margin-top:38px">')
    body.append('<h2 style="border-top:1px solid var(--line)">Ejercicios para practicar</h2>')
    body.append('<p>No hace falta entregarlos: el objetivo es convertir la lectura en decisiones concretas. Dedica entre 15 y 30 minutos a cada uno.</p>')
    body.append('<ol>' + ''.join(f'<li>{esc(e)}</li>' for e in quiz["exercises"]) + '</ol>')
    body.append('</section>')
    body.append(finish_section(item, quiz["title"], is_quiz=True))
    body.append('  </article>')
    body.append(render_toc(toc_ids))
    body.append('</div>')
    return "\n".join(body)


def dock(item):
    prv = item["prev"]
    nxt = item["next"]
    left = (f'<a class="dock-btn" href="{prv["href"]}" aria-label="Lección anterior: {esc(prv["title"])}" title="Anterior (←)">{ICON_BACK}</a>'
            if prv else f'<span class="dock-btn" aria-disabled="true">{ICON_BACK}</span>')
    right = (f'<a class="dock-next" href="{nxt["href"]}" title="Siguiente (→)">Siguiente {ICON_ARROW}</a>'
             if nxt else '<a class="dock-next" href="progreso.html" title="Ver progreso">Progreso ' + ICON_ARROW + '</a>')
    return ('<nav class="dock" aria-label="Navegación entre lecciones">\n'
            f'  {left}\n'
            f'  <div class="dock-mid"><span>Paso {item["index"]+1} / {TOTAL}</span><i><b data-dockbar></b></i></div>\n'
            f'  {right}\n'
            '</nav>')


# ---------------------------------------------------------------- páginas
def build_lesson_pages():
    for m in MODULES:
        for l in m["lessons"]:
            item = BY_ID[l["id"]]
            toc = []
            content = render_lesson(m, l, item, toc)
            desc = l["lead"][:157].rsplit(" ", 1)[0] + "…"
            html_doc = page_head(
                f'{l["title"]} · {COURSE["title"]}',
                desc,
                "is-lesson", "ste_theme", l["id"],
            )
            html_doc += f'<main class="main" id="contenido">\n'
            html_doc += topbar([f'<a href="index.html">Curso</a>', f'<span>Módulo {m["num"]}</span>', f'<strong>{esc(l["title"])}</strong>'])
            html_doc += f'\n{content}\n</main>\n'
            html_doc += dock(item) + "\n"
            html_doc += searchbox_and_toast() + "\n"
            html_doc += f'<script>window.STE={data_blob(l["id"])};</script>\n<script src="js/curso.js"></script>\n</body>\n</html>\n'
            with open(os.path.join(ROOT, l["id"] + ".html"), "w", encoding="utf-8") as f:
                f.write(html_doc)
        q = m["quiz"]
        item = BY_ID[q["id"]]
        toc = []
        content = render_quiz(m, q, item, toc)
        desc = "Evaluación del módulo %s: %s" % (m["num"], q["title"])
        html_doc = page_head(f'{q["title"]} · {COURSE["title"]}', desc, "is-lesson", "ste_theme", q["id"])
        html_doc += f'<main class="main" id="contenido">\n'
        html_doc += topbar([f'<a href="index.html">Curso</a>', f'<span>Módulo {m["num"]}</span>', '<strong>Evaluación</strong>'])
        html_doc += f'\n{content}\n</main>\n'
        html_doc += dock(item) + "\n"
        html_doc += searchbox_and_toast() + "\n"
        html_doc += f'<script>window.STE={data_blob(q["id"])};</script>\n<script src="js/curso.js"></script>\n</body>\n</html>\n'
        with open(os.path.join(ROOT, q["id"] + ".html"), "w", encoding="utf-8") as f:
            f.write(html_doc)


def module_rows(m):
    rows = []
    for l in m["lessons"]:
        rows.append(f'<a class="row" data-lesson-row="{l["id"]}" href="{l["id"]}.html">\n'
                    f'  <span class="row-num">{m["num"]}.{l["lnum"]}</span>\n'
                    f'  <span class="row-title">{esc(l["title"])}</span>\n'
                    '  <span class="row-type">Lección</span>\n'
                    f'  <span class="row-time">{l["minutes"]} min</span>\n'
                    '  <span class="row-check" aria-hidden="true"></span>\n'
                    '</a>')
    q = m["quiz"]
    rows.append(f'<a class="row quiz" data-lesson-row="{q["id"]}" href="{q["id"]}.html">\n'
                f'  <span class="row-num">{m["num"]}.{len(m["lessons"]) + 1}</span>\n'
                f'  <span class="row-title">{esc(q["title"])}</span>\n'
                '  <span class="row-type">Examen</span>\n'
                '  <span class="row-time">10 min</span>\n'
                '  <span class="row-check" aria-hidden="true"></span>\n'
                '</a>')
    return "".join(rows)


def build_index():
    first = ITEMS[0]
    hours = hours_label(TOTAL_MIN)
    mods = []
    for m in MODULES:
        mins = sum(l["minutes"] for l in m["lessons"]) + 10
        mods.append(f'<details class="module" data-module="{m["num"]}" open>\n  <summary>\n'
                    f'    <span class="module-num">{m["num"]}</span>\n'
                    f'    <span class="module-title-wrap"><span class="module-title">{esc(m["title"])}</span><span class="module-sub">{esc(m["sub"])}</span></span>\n'
                    f'    <span class="module-meta">{len(m["lessons"]) + 1} sesiones · {hours_label(mins)}<br><span data-modcount="{m["num"]}">0/{len(m["lessons"]) + 1}</span> completadas</span>\n'
                    '    <svg class="module-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="m6 9 6 6 6-6"></path></svg>\n'
                    '  </summary>\n'
                    f'  <div class="module-progress" aria-hidden="true"><i data-modbar="{m["num"]}"></i></div>\n'
                    f'  <div class="module-body">{module_rows(m)}</div>\n'
                    '</details>')

    doc = page_head(
        f'{COURSE["title"]} · {COURSE["subtitle"]}',
        COURSE["description"],
        "is-home", "ste_theme", None, sidebar_html="",
    )
    doc = doc.replace('<a class="skip" href="#contenido">Saltar al contenido</a>\n', '<a class="skip" href="#temario">Saltar al temario</a>\n')
    doc += ('<header class="masthead">\n' + brand() + '\n'
            '  <nav class="mast-nav" aria-label="Principal"><a href="#temario">Temario</a><a href="#metodo">Método</a><a href="glosario.html">Glosario</a><a href="progreso.html">Mi progreso</a></nav>\n'
            '  <div class="mast-actions">\n'
            f'    <button class="icon-btn" type="button" data-theme-toggle aria-label="Cambiar tema">{ICON_MOON}{ICON_SUN}</button>\n'
            f'    <a class="mast-cta" href="{first["href"]}">Empezar {ICON_ARROW}</a>\n'
            '  </div>\n</header>\n\n')
    doc += f'''<main>
<section class="hero">
  <div>
    <span class="eyebrow">Edición esencial · {COURSE["year"]}</span>
    <h1>Lidera sin<br>dejar de <em>construir</em>.</h1>
    <p class="lede">La edición esencial de <em>{esc(COURSE["book"])}</em>: arquetipos del rol, trabajo que importa, estrategia, calidad, influencia sin jerarquía, patrocinio y el salto de empresa. Siete módulos, 21 lecciones y las decisiones que separan a un Senior de un referente técnico.</p>
    <div class="hero-actions">
      <a class="btn btn-ink" href="{first["href"]}">Abrir la primera lección {ICON_ARROW}</a>
      <a class="btn btn-line" href="{COURSE["pdf"]}">{ICON_DOWN} Descargar el PDF</a>
    </div>
    <div class="hero-stats">
      <div class="hero-stat"><b>{N_LESSONS}</b><span>Lecciones</span></div>
      <div class="hero-stat"><b>{len(MODULES)}</b><span>Módulos</span></div>
      <div class="hero-stat"><b>{hours}</b><span>De lectura</span></div>
      <div class="hero-stat"><b>{N_DIAGRAMS}</b><span>Diagramas</span></div>
    </div>
  </div>
  <aside class="pass" aria-label="Tu progreso en el curso">
    <div class="pass-top"><span class="eyebrow">Pase de estudiante</span><span class="pass-edition">STE · {COURSE["year"]}<br>Español</span></div>
    <div class="pass-main"><span class="pass-big">{TOTAL}</span><span class="pass-big-label">pasos<br>por recorrer</span></div>
    <p class="pass-desc">Tu avance se guarda en este navegador. Empieza por donde quieras: el curso está pensado para leerse en orden.</p>
    <div class="pass-progress"><div class="bar"><i data-bar></i></div><span><b data-done-count>0</b> / {TOTAL}</span></div>
    <div class="pass-actions">
      <a class="btn btn-cream" data-resume href="{first["href"]}"><span><span data-resume-label>Empezar el curso</span><br><small style="font-weight:500;opacity:.7;font-size:10px" data-resume-title>{esc(first["title"])}</small></span>{ICON_ARROW}</a>
      <a class="btn btn-line" style="border-color:rgba(255,255,255,.22);color:#e9e1d1" href="{COURSE["pdf"]}">{ICON_DOWN} PDF</a>
    </div>
    <div class="pass-note"><span>{len(MODULES)} evaluaciones</span><span>Acceso libre</span></div>
  </aside>
</section>

<section class="section" id="temario">
  <div class="section-head">
    <div><span class="eyebrow">Plan de estudios</span><h2>Todo el temario, a la vista.</h2></div>
    <p>Siete módulos que recorren el rol: arquetipos, foco, influencia, multiplicación, promoción, cambio de empresa y sostenibilidad.</p>
    <button class="text-toggle" type="button" data-toggle-all>Contraer el temario</button>
  </div>
  {''.join(mods)}
</section>

<section class="section" id="metodo">
  <div class="section-head">
    <div><span class="eyebrow">Cómo está pensado</span><h2>Leer, decidir, aplicar.</h2></div>
    <p>Una experiencia de lectura continua: sin botones que te devuelvan al inicio y sin callejones sin salida.</p>
  </div>
  <div class="method-grid">
    <div class="method"><span class="n">01</span>{ICON_ARROW}<h3>Avanza sin fricción</h3><p>Cada lección termina con «Completar y seguir». También puedes usar las flechas del teclado.</p></div>
    <div class="method"><span class="n">02</span>{ICON_CHECK}<h3>Decide con criterio</h3><p>Al cerrar cada módulo, una evaluación de cuatro preguntas y ejercicios para llevar las ideas a tu contexto.</p></div>
    <div class="method"><span class="n">03</span>{ICON_DOWN}<h3>Llévatelo contigo</h3><p>El manual esencial en PDF incluye todo el curso, con los diagramas y el glosario, para consultarlo sin conexión.</p></div>
  </div>
</section>
</main>

<footer class="site-foot">
  <div class="foot-inner">
    <div><span class="eyebrow" style="color:#9cc4e8">Sigue profundizando</span><h2>El organigrama no es la carrera.</h2><p>Este manual convierte los capítulos de <em>{esc(COURSE["book"])}</em> en un recorrido práctico: arquetipos, foco, estrategia, calidad, influencia, patrocinio y cambio de empresa. Úsalo para tomar decisiones, no para memorizar títulos.</p></div>
    <div class="foot-links"><a href="{first["href"]}">Empezar el curso →</a><a href="glosario.html">Glosario de términos →</a><a href="progreso.html">Mi progreso →</a><a href="{COURSE["pdf"]}">Manual en PDF →</a></div>
  </div>
  <div class="foot-bottom"><span>{esc(COURSE["title"])} · {esc(COURSE["subtitle"])} · {COURSE["year"]}</span><span>Manual original · Temas de {esc(COURSE["author"])}</span></div>
</footer>
'''
    doc += searchbox_and_toast() + "\n"
    doc += f'<script>window.STE={data_blob(None)};</script>\n<script src="js/curso.js"></script>\n</body>\n</html>\n'
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)


def build_glossary():
    terms = sorted(GLOSARIO, key=lambda t: slug(t[0]))
    letters = sorted({slug(t[0])[0].upper() for t in terms})
    alpha = ['<button type="button" data-alpha="*" class="on" aria-label="Todos">*</button>']
    for letter in letters:
        alpha.append(f'<button type="button" data-alpha="{letter}" aria-label="Términos con {letter}">{letter}</button>')
    cards = []
    for term, definition, lid in terms:
        href = lid + ".html"
        cards.append(f'<article class="term" data-term="{esc(term)}"><h3>{esc(term)}</h3><p>{esc(definition)}</p>'
                     f'<a href="{href}">Ver en el curso {ICON_ARROW}</a></article>')
    doc = page_head("Glosario de liderazgo técnico · Staff Engineer", "Glosario en español del rol Staff-plus: arquetipos, patrocinio, estrategia, calidad, visibilidad, promoción y negociación.", "is-page", "ste_theme", None)
    doc += '<main class="main" id="contenido">\n'
    doc += topbar(['<a href="index.html">Curso</a>', '<strong>Glosario</strong>'])
    doc += f'''
<div class="page">
  <div class="page-head"><span class="eyebrow">Referencia rápida</span><h1>Glosario</h1><p>Los términos que aparecen una y otra vez en el curso, explicados en una frase. Busca o filtra por letra; cada entrada te lleva a la lección donde se desarrolla.</p></div>
  <div class="gloss-tools">
    <div class="gloss-search">{ICON_SEARCH}<input type="search" data-gloss-input placeholder="Buscar término: patrocinio, sala, SCQA…" aria-label="Buscar en el glosario"></div>
    <div class="alpha" aria-label="Filtrar por letra">{''.join(alpha)}</div>
  </div>
  <div class="gloss-grid">{''.join(cards)}</div>
</div>
</main>
'''
    doc += searchbox_and_toast() + "\n"
    doc += f'<script>window.STE={data_blob(None)};</script>\n<script src="js/curso.js"></script>\n</body>\n</html>\n'
    with open(os.path.join(ROOT, "glosario.html"), "w", encoding="utf-8") as f:
        f.write(doc)


def build_progress():
    rows = []
    for m in MODULES:
        rows.append(f'<div class="mp" data-mp="{m["num"]}">\n'
                    f'  <span class="n">{m["num"]}</span>\n'
                    f'  <span class="t">{esc(m["title"])}</span>\n'
                    '  <span class="b"><i data-mpbar></i></span>\n'
                    '  <span class="p" data-mppct>0%</span>\n'
                    '</div>')
    doc = page_head("Mi progreso · Staff Engineer", "Tu avance en el curso, guardado solo en este navegador.", "is-page", "ste_theme", None)
    doc += '<main class="main" id="contenido">\n'
    doc += topbar(['<a href="index.html">Curso</a>', '<strong>Mi progreso</strong>'])
    doc += f'''
<div class="page">
  <div class="page-head"><span class="eyebrow">Tu recorrido</span><h1>Mi progreso</h1><p>El avance se guarda solo en este navegador. Puedes completar lecciones y evaluaciones con el botón del final o con la tecla <strong>C</strong>.</p></div>
  <div class="dash">
    <div class="card dark">
      <div class="big-ring">
        <svg class="ring" viewBox="0 0 46 46" aria-hidden="true"><circle class="ring-bg" cx="23" cy="23" r="18"></circle><circle class="ring-fg" data-ring cx="23" cy="23" r="18"></circle></svg>
        <div><b><span data-done-count>0</span> / {TOTAL}</b><span>pasos completados</span></div>
      </div>
      <div class="dash-cta"><a class="btn btn-cream" data-resume href="{ITEMS[0]["href"]}">Continuar {ICON_ARROW}</a></div>
    </div>
    <div class="card">
      <h2>Resumen</h2>
      <div class="stat-grid">
        <div class="stat"><b data-pct>0%</b><span>Del curso</span></div>
        <div class="stat"><b>{len(MODULES)}</b><span>Módulos</span></div>
        <div class="stat"><b>{len(MODULES)}</b><span>Evaluaciones</span></div>
      </div>
      <p style="font-size:12.5px;color:var(--muted);margin:18px 0 0;line-height:1.55">Cuando termines un paso, aparecerá aquí y en el temario. El progreso no se sincroniza entre dispositivos.</p>
    </div>
  </div>
  <div class="card" style="margin-bottom:26px">
    <h2>Avance por módulo</h2>
    <div class="mod-progress-list">{''.join(rows)}</div>
  </div>
  <div class="card">
    <h2>Pasos completados</h2>
    <div class="completed-list" data-completed-list></div>
    <div data-completed-empty></div>
  </div>
  <button class="reset" type="button" data-reset>Borrar el progreso de este navegador</button>
</div>
</main>
'''
    doc += searchbox_and_toast() + "\n"
    doc += f'<script>window.STE={data_blob(None)};</script>\n<script src="js/curso.js"></script>\n</body>\n</html>\n'
    with open(os.path.join(ROOT, "progreso.html"), "w", encoding="utf-8") as f:
        f.write(doc)


def main():
    build_lesson_pages()
    build_index()
    build_glossary()
    build_progress()
    print(f"Generadas {TOTAL} páginas de curso + índice, glosario y progreso.")
    print(f"Lecciones: {N_LESSONS} · Módulos: {len(MODULES)} · Diagramas: {N_DIAGRAMS} · Minutos: {TOTAL_MIN}")


if __name__ == "__main__":
    import sys
    main()
    if "--pdf" in sys.argv:
        import build_pdf
        build_pdf.build()
