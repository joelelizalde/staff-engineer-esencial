#!/usr/bin/env python3
"""Genera el PDF de «Staff Engineer · Liderazgo técnico · Edición esencial» con WeasyPrint.

Uso:
    python3 build_pdf.py

Requiere WeasyPrint (probado con 70.x). Escribe el PDF en la raíz del proyecto.
"""

import os
from contenido import COURSE, GLOSARIO, MODULES
from build_site import render_diagram, esc, slug, TOTAL_MIN

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, COURSE["pdf"])

CSS = r"""
@font-face{font-family:Fraunces;src:url(assets/fonts/Fraunces-500.ttf);font-weight:500}
@font-face{font-family:Fraunces;src:url(assets/fonts/Fraunces-700.ttf);font-weight:700}
@font-face{font-family:Inter;src:url(assets/fonts/Inter-400.ttf);font-weight:400}
@font-face{font-family:Inter;src:url(assets/fonts/Inter-500.ttf);font-weight:500}
@font-face{font-family:Inter;src:url(assets/fonts/Inter-600.ttf);font-weight:600}
@font-face{font-family:Inter;src:url(assets/fonts/Inter-700.ttf);font-weight:700}

@page{
  size:A4;
  margin:16mm 17mm 16mm;
  @top-left{content:string(chapter);font:500 7.5pt Inter;letter-spacing:.12em;text-transform:uppercase;color:#7b8390}
  @top-right{content:"Staff Engineer · Liderazgo técnico · Edición esencial";font:500 7.5pt Inter;letter-spacing:.06em;color:#7b8390}
  @bottom-center{content:counter(page);font:500 8.5pt Inter;color:#666e7a}
}
@page cover{margin:0;@top-left{content:none}@top-right{content:none}@bottom-center{content:none}}
@page front{margin:22mm 20mm;@top-left{content:none}@top-right{content:none}}

html{font-family:Inter;font-size:9.1pt;line-height:1.46;color:#2b3038}
body{margin:0}
a{color:#234a6d;text-decoration:none}
h1,h2,h3,h4{font-family:Fraunces;font-weight:500;letter-spacing:-.01em;color:#14171c}
p{margin:0 0 .7em;orphans:3;widows:3}
strong{font-weight:600;color:#14171c}
em{font-style:italic}
ul,ol{margin:0 0 .8em;padding-left:1.2em}
li{margin:.2em 0}

/* Portada */
.cover{page:cover;height:297mm;background:#14171c;color:#f4f4f0;padding:26mm 22mm;box-sizing:border-box;position:relative;page-break-after:always}
.cover .mark{width:16mm;height:16mm;border:1px solid #2e5f8a;border-radius:2.5mm;display:flex;align-items:center;justify-content:center;font-family:Fraunces;font-weight:700;font-size:15pt;color:#f4f4f0}
.cover .eyebrow{margin-top:12mm;font:600 8pt Inter;letter-spacing:.22em;text-transform:uppercase;color:#9cc4e8}
.cover h1{font-size:44pt;line-height:1.0;color:#f4f4f0;margin:8mm 0 6mm;letter-spacing:-.03em}
.cover h1 em{font-style:italic;color:#6aa9d8}
.cover .lede{font-size:12pt;line-height:1.6;color:#c6ccd5;max-width:120mm}
.cover .book{margin-top:8mm;font-size:9.5pt;color:#9aa3af;max-width:120mm}
.cover .book em{color:#e8edf3}
.cover .foot{position:absolute;left:22mm;right:22mm;bottom:22mm;border-top:1px solid rgba(255,255,255,.16);padding-top:5mm;display:flex;justify-content:space-between;font:500 8pt Inter;letter-spacing:.12em;text-transform:uppercase;color:#8e97a3}
.cover .stats{display:flex;gap:12mm;margin-top:14mm}
.cover .stats b{display:block;font-family:Fraunces;font-size:22pt;font-weight:500;color:#f4f4f0;line-height:1}
.cover .stats span{font:500 7.5pt Inter;letter-spacing:.14em;text-transform:uppercase;color:#8e97a3}

/* Portadilla / índice */
.front{page:front}
.front h1{font-size:30pt;margin:0 0 4mm}
.front .kicker{font:600 8pt Inter;letter-spacing:.2em;text-transform:uppercase;color:#2e5f8a}
.front .intro{font-size:10pt;color:#565d68;max-width:140mm;margin-bottom:6mm;line-height:1.5}
.toc-grid{columns:2;column-gap:11mm}
.toc-mod{margin:0 0 3.4mm;break-inside:avoid}
.toc-mod .mh{display:flex;gap:4mm;align-items:baseline;border-bottom:1px solid #d2d8e0;padding-bottom:.8mm;margin-bottom:.8mm}
.toc-mod .mh b{font-family:Fraunces;font-size:13pt;color:#2e5f8a;font-weight:500}
.toc-mod .mh span{font-weight:600;font-size:10.5pt;color:#14171c}
.toc-row{display:flex;gap:3mm;font-size:8.8pt;color:#363b44;padding:.3mm 0;line-height:1.35}
.toc-row .n{font-family:Inter;font-size:8pt;color:#7b8390;min-width:8mm}
.toc-row .t{flex:1}
.toc-row .t em{font-style:italic;color:#666e7a}
.toc-row a{margin-left:auto}
.toc-row a::after{content:target-counter(attr(href),page);font-size:8pt;color:#7b8390}
.toc-note{margin-top:7mm;padding-top:3mm;border-top:1px solid #d2d8e0;font-size:8.4pt;line-height:1.5;color:#666e7a;max-width:128mm}

/* Lecciones */
.chapter{break-before:page}
.kicker{display:flex;align-items:center;gap:3mm;font:600 8pt Inter;letter-spacing:.18em;text-transform:uppercase;color:#2e5f8a;margin-bottom:3mm}
.kicker::before{content:"";display:inline-block;width:8mm;height:.4mm;background:#2e5f8a}
.chapter h1{font-size:24pt;line-height:1.06;margin:0 0 3mm;string-set:chapter content();letter-spacing:-.02em}
.meta{display:flex;gap:6mm;font:500 7.5pt Inter;letter-spacing:.1em;text-transform:uppercase;color:#7b8390;border-top:1px solid #d2d8e0;border-bottom:1px solid #d2d8e0;padding:1.8mm 0;margin-bottom:5mm}
.lead{font-size:10.6pt;line-height:1.6;color:#363b44;margin-bottom:1em}

.brief{background:#eef2f6;border-left:2px solid #2e5f8a;padding:2.2mm 3.6mm;margin:2.4mm 0 3.2mm;break-inside:avoid}
.brief .k{font:600 7.5pt Inter;letter-spacing:.16em;text-transform:uppercase;color:#7b8390;margin-bottom:2mm}
.brief ul{columns:2;column-gap:8mm;margin:0;padding-left:4mm;font-size:9pt;color:#363b44}

figure.diagram{margin:2.2mm 0 2.6mm;padding:2mm;background:#fdfdfb;border:1px solid #d5dbe3;border-radius:2mm;break-inside:avoid}
figure.diagram svg{width:100%;height:auto}
figcaption{font-size:8pt;color:#786e5e;border-top:1px solid #dde3ea;margin-top:2mm;padding-top:2mm;line-height:1.45}

h2.sec{font-size:13.4pt;margin:3.2mm 0 1.4mm;padding-top:1.8mm;border-top:1px solid #d9dfe7;break-after:avoid}
h2.sec .sn{display:block;font:600 7.5pt Inter;letter-spacing:.18em;color:#2e5f8a;margin-bottom:1.5mm}
.body p{font-size:9.1pt;line-height:1.48;color:#2b3038;margin-bottom:.5em}

.box{margin:2.6mm 0;padding:2.2mm 3.2mm;border-radius:2mm;break-inside:avoid}
.extras{display:flex;gap:3mm;margin:2.6mm 0;break-inside:avoid}
.extras .box{flex:1;margin:0}
.box h3{font-family:Inter;font-weight:600;font-size:8.2pt;letter-spacing:.14em;text-transform:uppercase;margin:0 0 1.6mm}
.box ul{margin:0;padding-left:4mm;font-size:8.5pt}
.box p{margin:0;font-size:8.7pt;line-height:1.45}
.keys{background:#eef3f8;border:1px solid #cddbe7}
.keys h3{color:#8a5a2b}
.example{background:#f4f2ec;border:1px solid #ddd8cc}
.example h3{color:#7a5a24}
.caution{background:#eef2f7;border:1px solid #d3deea}
.caution h3{color:#234a6d}

/* Evaluación */
.quiz-q{border-top:1px solid #d9dfe7;padding-top:2mm;margin-top:2.2mm;break-inside:avoid}
.quiz-q .qq{font-weight:600;font-size:9.4pt;margin-bottom:1.2mm}
.quiz-q .qn{font:600 8pt Inter;letter-spacing:.1em;color:#2e5f8a;margin-right:2mm}
.quiz-q ol{list-style:none;padding:0;margin:0;font-size:9pt;line-height:1.45;color:#363b44}
.quiz-q ol li{margin:.35mm 0;padding-left:6mm;position:relative}
.quiz-q ol li::before{content:attr(data-letter);position:absolute;left:0;font:600 8pt Inter;color:#7b8390}
.answers{margin-top:4mm;padding:3mm 4mm;background:#eef2f6;border:1px solid #d5dbe3;break-inside:avoid;columns:2;column-gap:6mm}
.answers h3{font:600 8pt Inter;letter-spacing:.16em;text-transform:uppercase;color:#7b8390;margin:0 0 1.6mm;column-span:all}
.answers p{font-size:8.4pt;line-height:1.45;margin:0 0 1.5mm;break-inside:avoid}
.answers b{color:#234a6d}
.exercise{margin-top:4mm;break-inside:avoid}
.exercise h3{font:600 8pt Inter;letter-spacing:.16em;text-transform:uppercase;color:#7b8390;margin:0 0 1.5mm}
.exercise ol{font-size:8.8pt;line-height:1.45;color:#363b44;margin-bottom:0}

/* Glosario */
.gloss{margin-top:3mm;columns:2;column-gap:10mm}
.gloss .term{break-inside:avoid;border-bottom:1px solid #e4e9ef;padding:1.7mm 0}
.gloss h3{font-family:Inter;font-weight:600;font-size:9.8pt;margin:0 0 .6mm}
.gloss p{margin:0;font-size:9.2pt;color:#444a54}
"""


def cover():
    hours = ("%.1f" % (TOTAL_MIN / 60)).replace(".", ",")
    return f'''<section class="cover">
  <div class="mark">STE</div>
  <div class="eyebrow">Edición esencial · Español · {COURSE["year"]}</div>
  <h1>Lidera sin<br>dejar de<br><em>construir</em>.</h1>
  <p class="lede">{esc(COURSE["description"])}</p>
  <p class="book">Basado en los temas de <em>{esc(COURSE["book"])}</em>, de {esc(COURSE["author"])}. Texto y diagramas originales: no reproduce el libro.</p>
  <div class="stats">
    <div><b>{sum(len(m["lessons"]) for m in MODULES)}</b><span>Lecciones</span></div>
    <div><b>{len(MODULES)}</b><span>Módulos</span></div>
    <div><b>{hours}</b><span>Horas</span></div>
    <div><b>{sum(1 for m in MODULES for l in m["lessons"] if l.get("diagram"))}</b><span>Diagramas</span></div>
  </div>
  <div class="foot"><span>{esc(COURSE["title"])} · {esc(COURSE["subtitle"])}</span><span>Manual en PDF</span></div>
</section>'''


def front():
    parts = [f'''<section class="front">
  <div class="kicker">Manual esencial</div>
  <h1>Contenido</h1>
  <p class="intro">Siete módulos que recorren el rol: arquetipos, foco, influencia, multiplicación, promoción, cambio de empresa y sostenibilidad. Cada módulo cierra con una evaluación y ejercicios.</p>
''']
    parts.append('<div class="toc-grid">')
    for m in MODULES:
        parts.append('<div class="toc-mod"><div class="mh">'
                     f'<b>{m["num"]}</b><span>{esc(m["title"])}</span></div>')
        for l in m["lessons"]:
            parts.append(f'<div class="toc-row"><span class="n">{m["num"]}.{l["lnum"]}</span>'
                         f'<span class="t">{esc(l["title"])}</span><a href="#{l["id"]}"></a></div>')
        q = m["quiz"]
        parts.append(f'<div class="toc-row"><span class="n">{m["num"]}.{len(m["lessons"]) + 1}</span>'
                     f'<span class="t"><em>{esc(q["title"])}</em></span><a href="#{q["id"]}"></a></div>')
        parts.append('</div>')
    parts.append('<div class="toc-mod"><div class="mh"><b>—</b><span>Glosario</span></div>'
                 '<div class="toc-row"><span class="n"></span><span class="t">Términos del curso</span><a href="#glosario"></a></div></div>')
    parts.append('</div>')
    parts.append('<p class="toc-note">Cada lección ocupa dos páginas: la primera abre el tema y la segunda cierra con las ideas clave, un caso concreto y un aviso. Cada módulo termina con una evaluación de cuatro preguntas y tres ejercicios. El glosario final reúne los 68 términos que se repiten a lo largo del curso.</p>')
    parts.append('</section>')
    return "\n".join(parts)


def lesson_html(m, l):
    out = [f'<section class="chapter" id="{l["id"]}">']
    out.append(f'<div class="kicker">Módulo {m["num"]} · Lección {l["lnum"]} de {len(m["lessons"])}</div>')
    out.append(f'<h1>{esc(l["title"])}</h1>')
    out.append(f'<div class="meta"><span>{l["minutes"]} min de lectura</span><span>{len(l["sections"])} apartados</span><span>{esc(m["title"])}</span></div>')
    out.append(f'<p class="lead">{esc(l["lead"])}</p>')
    out.append('<div class="brief"><div class="k">En esta lección</div><ul>'
               + ''.join(f'<li>{esc(b)}</li>' for b in l["brief"]) + '</ul></div>')
    out.append(render_diagram(l["diagram"], l.get("caption", "")))
    out.append('<div class="body">')
    for i, sec in enumerate(l["sections"], 1):
        out.append(f'<h2 class="sec"><span class="sn">{i:02d}</span>{esc(sec["h"])}</h2>')
        for p in sec["p"]:
            out.append(f'<p>{esc(p)}</p>')
    out.append('</div>')
    out.append('<div class="box keys"><h3>Ideas clave</h3><ul>'
               + ''.join(f'<li>{esc(k)}</li>' for k in l["keys"]) + '</ul></div>')
    out.append('<div class="extras">')
    out.append(f'<div class="box example"><h3>Caso concreto</h3><p>{esc(l["example"])}</p></div>')
    out.append(f'<div class="box caution"><h3>Cuidado</h3><p>{esc(l["caution"])}</p></div>')
    out.append('</div>')
    out.append('</section>')
    return "\n".join(out)


def quiz_html(m, q):
    letters = "abcd"
    out = [f'<section class="chapter" id="{q["id"]}">']
    out.append(f'<div class="kicker">Módulo {m["num"]} · Evaluación</div>')
    out.append(f'<h1>{esc(q["title"])}</h1>')
    out.append('<div class="meta"><span>10 min</span>'
               f'<span>{len(q["questions"])} preguntas</span><span>3 de 4 para aprobar</span></div>')
    out.append('<div class="body quiz-summary">')
    for p in q["summary"]:
        out.append(f'<p>{esc(p)}</p>')
    out.append('</div>')
    for qi, question in enumerate(q["questions"], 1):
        out.append('<div class="quiz-q">')
        out.append(f'<p class="qq"><span class="qn">{qi:02d}</span>{esc(question["q"])}</p>')
        out.append('<ol>' + ''.join(
            f'<li data-letter="{letters[oi]})">{esc(opt)}</li>'
            for oi, opt in enumerate(question["options"])) + '</ol>')
        out.append('</div>')
    out.append('<div class="answers"><h3>Respuestas y explicaciones</h3>')
    for qi, question in enumerate(q["questions"], 1):
        correct = letters[question["answer"]]
        out.append(f'<p><b>{qi:02d} · {correct})</b> {esc(question["why"])}</p>')
    out.append('</div>')
    out.append('<div class="exercise"><h3>Ejercicios para practicar</h3><ol>'
               + ''.join(f'<li>{esc(e)}</li>' for e in q["exercises"]) + '</ol></div>')
    out.append('</section>')
    return "\n".join(out)


def glossary_html():
    terms = sorted(GLOSARIO, key=lambda t: slug(t[0]))
    out = ['<section class="chapter" id="glosario">',
           '<div class="kicker">Referencia rápida</div>',
           '<h1>Glosario</h1>',
           '<p class="lead">Los términos que aparecen una y otra vez en el curso, explicados en una frase.</p>',
           '<div class="gloss">']
    for term, definition, _lid in terms:
        out.append(f'<div class="term"><h3>{esc(term)}</h3><p>{esc(definition)}</p></div>')
    out.append('</div></section>')
    return "\n".join(out)


def build():
    body = [cover(), front()]
    for m in MODULES:
        for l in m["lessons"]:
            body.append(lesson_html(m, l))
        body.append(quiz_html(m, m["quiz"]))
    body.append(glossary_html())
    doc = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<title>{esc(COURSE["title"])} · {esc(COURSE["subtitle"])}</title>
<style>{CSS}</style></head>
<body>
{"".join(body)}
</body></html>'''
    from weasyprint import HTML
    HTML(string=doc, base_url=ROOT + "/").write_pdf(OUT)
    size = os.path.getsize(OUT) / 1024
    print(f"PDF generado: {OUT} ({size:.0f} KB)")


if __name__ == "__main__":
    build()
