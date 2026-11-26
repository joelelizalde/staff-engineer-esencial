# Staff Engineer — Edición esencial en español

Manual de estudio estático (sin build para el lector y sin dependencias en el navegador) para crecer en el carril técnico: arquetipos del rol, trabajo que importa, estrategia, calidad, influencia sin jerarquía, patrocinio, cambio de empresa y sostenibilidad.
Alineado temáticamente con *Staff Engineer: Leadership beyond the Management Track*, de Will Larson, pero con texto, ejemplos y diagramas originales.

## Qué incluye

- **21 lecciones** en **7 módulos** (3 lecciones y 1 evaluación por módulo), siguiendo el recorrido del libro: el rol → trabajo y estrategia → influencia → multiplicación → promoción → cambio de empresa → historias y primer año.
- Lectura continua: botón «Completar y seguir», navegación con ← y →, temario lateral siempre disponible.
- **7 evaluaciones** de 4 preguntas con explicaciones y **21 ejercicios** aplicados.
- Progreso guardado en `localStorage`, glosario con buscador y modo claro/oscuro.
- Buscador global con atajo `⌘K` / `Ctrl+K`.
- **21 diagramas originales** en SVG (flujo, capas, bucle, matriz y latencia).
- **68 términos** en el glosario.
- Manual en PDF: `Staff-Engineer-Esencial.pdf` (54 páginas).
- Tipografías locales (Fraunces + Inter), sin depender de Google Fonts.

## Estructura

```
index.html                      Portada y temario completo
stem1l1.html … stem7q.html      21 lecciones y 7 evaluaciones
glosario.html                   Glosario con búsqueda y filtro por letra
progreso.html                   Progreso por módulo
css/curso.css                   Diseño editorial responsive
js/curso.js                     Navegación, progreso, búsqueda y quizzes
assets/fonts/                   Tipografías locales
modulos/m01.py … m07.py         Contenido de cada módulo
contenido.py                    Reúne módulos, metadatos y glosario
build_site.py                   Generador del sitio
build_pdf.py                    Generador del PDF (WeasyPrint)
Staff-Engineer-Esencial.pdf
```

## Módulos

1. **El rol Staff-plus** — el carril técnico, los cuatro arquetipos y qué significa de verdad el título.
2. **Trabajo que importa** — elección de problemas, estrategia de ingeniería y calidad técnica sostenida.
3. **Influir sin jerarquía** — alinearse con la autoridad, liderar siguiendo y aprender a no equivocarse.
4. **Multiplicar al equipo** — crear espacio, construir una red de pares y presentar a dirección.
5. **Conseguir el título** — paquete de promoción, patrocinador, proyectos Staff y visibilidad.
6. **Cambiar de empresa** — elegir compañía, entrevistar para roles Staff-plus y negociar la oferta.
7. **Sostener el rol** — lecciones de catorce trayectorias, medición del impacto y primer año.

## Correspondencia con el libro

| Bloque | Tema | Lección |
|---|---|---|
| 01 | Arquetipos del rol Staff | `stem1l1`, `stem1l2` |
| 02 | Qué hace un Staff y alcance del puesto | `stem1l2`, `stem1l3` |
| 03 | ¿Importa el título? | `stem1l3` |
| 04 | Trabajar en lo que importa | `stem2l1` |
| 05 | Escribir estrategia de ingeniería | `stem2l2` |
| 06 | Gestionar la calidad técnica | `stem2l3` |
| 07 | Mantenerse alineado con la autoridad | `stem3l1` |
| 08 | Para liderar, primero seguir | `stem3l2` |
| 09 | Aprender a no equivocarse | `stem3l3` |
| 10 | Crear espacio para otros | `stem4l1` |
| 11 | Construir una red de pares | `stem4l2` |
| 12 | Presentar a dirección | `stem4l3` |
| 13 | Paquetes de promoción | `stem5l1` |
| 14 | Encontrar patrocinador | `stem5l2` |
| 15 | Proyectos Staff, sala y visibilidad | `stem5l3` |
| 16 | Decidir cambiar de empresa | `stem6l1` |
| 17 | Entrevistas Staff-plus | `stem6l2` |
| 18 | Negociar la oferta | `stem6l3` |
| 19 | Historias de catorce trayectorias | `stem7l1` |
| 20 | Impacto, revisión y primer año | `stem7l2`, `stem7l3` |

## Regenerar

```bash
python3 build_site.py          # solo el sitio
python3 build_site.py --pdf    # sitio + manual en PDF
```

El PDF se compone con WeasyPrint (probado con 70.x) a partir del mismo contenido y las mismas fuentes.

## Añadir o editar contenido

Cada módulo vive en `modulos/mNN.py` y expone un diccionario `MODULE`:

- `num`, `title`, `sub`
- `lessons`: lista de lecciones con `id`, `lnum`, `title`, `minutes`, `lead`, `diagram`, `caption`, `sections`, `brief`, `keys`, `example`, `caution`, `search`.
- `quiz`: `id`, `title`, `summary`, `questions`, `exercises`, `search`.

Los diagramas se declaran como tuplas: `("flow", [...])`, `("stack", [...])`, `("loop", [...])`, `("matrix", {...})`, `("curve", {...})`, `("latency", {...})` o `("bars", [...])`.
Al cambiar contenido, vuelve a ejecutar `build_site.py --pdf` para regenerar páginas y PDF.

## Atajos

| Tecla | Acción |
|---|---|
| ← / → | Lección anterior / siguiente |
| `C` | Marcar la página actual como completada |
| `/` o `⌘K` | Abrir el buscador |
| `Esc` | Cerrar buscador o menú |
| `?` | Recordatorio de atajos |

## Datos locales

El progreso y el tema se guardan solo en el navegador:

- `ste_progress_v1`
- `ste_theme`

El objeto global del curso es `window.STE`. No se envía nada a un servidor.

## Publicar en GitHub Pages

1. Crea un repositorio con el contenido de esta carpeta en la raíz.
2. **Settings → Pages → Deploy from a branch → main → / (root)**.
3. El sitio quedará en `https://<usuario>.github.io/<repositorio>/`.

No subas claves ni tokens al repositorio: el curso es estático y no necesita credenciales.

## Créditos

Manual original de estudio en español, alineado con los temas de *Staff Engineer: Leadership beyond the Management Track*, de Will Larson (2020).
No reproduce el texto ni las figuras del libro. Uso educativo.
