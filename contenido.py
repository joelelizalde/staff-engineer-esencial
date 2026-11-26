"""Contenido del curso «Staff Engineer · Edición esencial».

Cada módulo vive en modulos/mNN.py y expone un diccionario MODULE.
Este archivo los reúne y añade los metadatos del curso y el glosario.
"""

from modulos import m01, m02, m03, m04, m05, m06, m07

MODULES = [
    m01.MODULE,
    m02.MODULE,
    m03.MODULE,
    m04.MODULE,
    m05.MODULE,
    m06.MODULE,
    m07.MODULE,
]

COURSE = {
    "title": "Staff Engineer",
    "brand": "STE",
    "subtitle": "Liderazgo técnico · Edición esencial",
    "tagline": "Crecer sin dejar de ser ingeniero",
    "description": (
        "Edición esencial en español de «Staff Engineer», de Will Larson: arquetipos "
        "del rol, trabajo que importa, estrategia, calidad, influencia sin jerarquía, "
        "patrocinio y el salto de empresa, con texto y diagramas originales."
    ),
    "book": "Staff Engineer: Leadership beyond the Management Track",
    "author": "Will Larson",
    "pdf": "Staff-Engineer-Esencial.pdf",
    "year": "2026",
}

# Glosario: (término, definición breve, id de lección donde se desarrolla)
GLOSARIO = [
    ("Apuesta", "Proyecto complejo y visible que acepta un riesgo real y del que se espera un aprendizaje o un resultado concreto.", "stem5l3"),
    ("Arquetipo", "Patrón recurrente de rol Staff-plus; el libro describe cuatro: Tech Lead, Architect, Solver y Right Hand.", "stem1l2"),
    ("Arquitecto", "Arquetipo que responde por un dominio técnico concreto y por la dirección de su evolución.", "stem1l2"),
    ("Autoridad prestada", "Capacidad de decidir que la organización concede temporalmente y que depende de seguir alineado con quien la otorga.", "stem3l1"),
    ("Autoevaluación", "Revisión honesta del propio impacto y de las señales que lo rodean, sin confundir actividad con resultado.", "stem7l2"),
    ("Calidad técnica", "Nivel de mantenibilidad, fiabilidad y claridad del software respecto al umbral que la empresa necesita hoy.", "stem2l3"),
    ("Carril técnico", "Trayectoria de responsabilidad creciente que no exige pasar a gestión de personas.", "stem1l1"),
    ("Ciclo de feedback", "Secuencia de observar, dar contexto, probar un cambio y volver a observar para mejorar una relación o un sistema.", "stem3l2"),
    ("Comité de calibración", "Foro donde los líderes comparan evidencias y deciden promociones con criterios compartidos.", "stem5l1"),
    ("Compensación", "Conjunto de salario, variable, equity y beneficios que forma la oferta económica de un puesto.", "stem6l3"),
    ("Confianza", "Expectativa sostenida de que la otra persona actúa con criterio y sin sorpresas; es la moneda del rol Staff.", "stem3l1"),
    ("Contexto", "Información sobre prioridades, restricciones y personas que permite decidir bien sin escalar cada caso.", "stem3l1"),
    ("Deuda técnica", "Coste futuro acumulado por decisiones de diseño que hoy funcionan pero mañana frenan el cambio.", "stem2l3"),
    ("Diagnóstico", "Explicación precisa del problema que una estrategia pretende resolver y de por qué importa ahora.", "stem2l2"),
    ("Doble carril", "Estructura de carrera con una vía de gestión y otra de liderazgo técnico, con niveles comparables.", "stem1l1"),
    ("Documento de diseño", "Texto que fija el problema, las alternativas y la decisión de un proyecto concreto antes de construirlo.", "stem2l2"),
    ("Entrevista Staff", "Proceso orientado a evaluar alcance, criterio y liderazgo, no solo velocidad de programación.", "stem6l2"),
    ("Equity", "Participación diferida en el valor de la empresa; suele ser la parte más negociable de una oferta senior.", "stem6l3"),
    ("Escalera de calidad", "Secuencia de intervenciones que va de arreglar lo urgente a medir y sostener la calidad en el tiempo.", "stem2l3"),
    ("Estrategia", "Conjunto de diagnósticos y políticas que ayuda a tomar decisiones coherentes sin volver a debatirlo todo.", "stem2l2"),
    ("Feedback no bloqueante", "Opinión compartida de forma explícita como opcional, para no convertir una preferencia en un veto.", "stem3l2"),
    ("Flexibilidad", "Margen para adaptar horario, ubicación o condiciones más allá de la política estándar de la empresa.", "stem6l3"),
    ("Glue work", "Trabajo de coordinación, documentación y cuidado que mantiene unido al equipo aunque no siempre se vea.", "stem5l1"),
    ("Historia de carrera", "Relato concreto de cómo una persona llegó a un rol y qué decisiones tomó; se usa como evidencia, no como plantilla.", "stem7l1"),
    ("Hot spot", "Punto concreto donde se concentra un problema de calidad y donde un arreglo pequeño produce un alivio grande.", "stem2l3"),
    ("Identidad", "Idea que una persona tiene de sí misma como profesional y que condiciona qué trabajo elige y qué evita.", "stem7l1"),
    ("Impacto", "Cambio positivo y verificable en el negocio, el equipo o los usuarios; no es lo mismo que esfuerzo ni que visibilidad.", "stem7l2"),
    ("Influencia", "Capacidad de mover decisiones sin depender de la autoridad formal, mediante contexto, confianza y preguntas.", "stem3l3"),
    ("Ingeniero distinguido", "Nivel técnico superior a Principal, reservado a muy pocas personas con impacto excepcional y sostenido.", "stem1l1"),
    ("Ingeniero principal", "Nivel Staff-plus posterior a Staff, con alcance normalmente mayor y más responsabilidad de dirección técnica.", "stem1l1"),
    ("Liderazgo técnico", "Práctica de fijar dirección, crear claridad y elevar a otros desde la experiencia técnica, con o sin reportes.", "stem1l1"),
    ("Mano derecha", "Arquetipo Right Hand: persona que amplifica a un líder senior y opera como su representante en decisiones concretas.", "stem1l2"),
    ("Mentoría", "Relación de consejo y aprendizaje; ayuda a pensar, pero no sustituye al patrocinio que abre oportunidades.", "stem5l2"),
    ("Mérito", "Creencia de que el talento individual debe primar sobre la regla general; suele producir organizaciones de excepciones.", "stem6l1"),
    ("Narrativa", "Relato breve que explica por qué una petición importa en el contexto de la persona y de la empresa.", "stem6l3"),
    ("Nivel", "Posición dentro de una escala profesional que agrupa expectativas, responsabilidades y banda salarial.", "stem1l3"),
    ("Nivelación", "Momento del proceso en el que la empresa decide en qué nivel encaja una candidatura.", "stem6l2"),
    ("Oferta", "Propuesta formal de empleo que combina nivel, compensación, condiciones y expectativas de trabajo.", "stem6l3"),
    ("Onboarding", "Periodo inicial en el que una persona nueva absorbe contexto, relaciones y formas de trabajar.", "stem7l3"),
    ("Paquete de promoción", "Documento vivo que reúne proyectos, impacto, mentoría, glue work y aliados para preparar una promoción.", "stem5l1"),
    ("Patrocinador", "Persona con capital organizacional que defiende tu trabajo y tu promoción en foros donde tú no estás.", "stem5l2"),
    ("Patrón", "Regularidad que se repite en varias trayectorias y que ayuda a interpretar la propia sin copiarla literalmente.", "stem7l1"),
    ("Pirámide de Minto", "Estructura de comunicación que empieza por la conclusión y la descompone en argumentos agrupados y ordenados.", "stem4l3"),
    ("Política rectora", "Regla de decisión que una estrategia adopta para resolver un conflicto recurrente y explica su razón.", "stem2l2"),
    ("Práctica deliberada", "Entrenamiento intencional de una habilidad concreta, con feedback y repetición, en lugar de solo acumular horas.", "stem7l1"),
    ("Preening", "Trabajo de baja utilidad y alta visibilidad que busca reconocimiento más que resultado.", "stem2l1"),
    ("Primeros 90 días", "Ventana inicial para escuchar, mapear el sistema y elegir pocas apuestas antes de empujar cambios grandes.", "stem7l3"),
    ("Procedimentalista", "Organización que prioriza reglas consistentes y procesos iguales para todos por encima de las excepciones.", "stem6l1"),
    ("Programa de calidad", "Iniciativa coordinada, con patrocinador y métricas, para elevar la calidad técnica de toda la organización.", "stem2l3"),
    ("Proyecto Staff", "Proyecto ambiguo, complejo y visible que estira a quien lo lidera y suele actuar como prueba de nivel.", "stem5l3"),
    ("Punto de palanca", "Lugar del sistema donde una inversión pequeña preserva calidad futura: interfaces, estado y modelos de datos.", "stem2l3"),
    ("Reconocimiento", "Validación organizacional del trabajo; sin ella, el impacto real puede quedar invisible para quien decide.", "stem1l3"),
    ("Red de pares", "Grupo de personas de nivel similar con quien contrastar decisiones, carrera y problemas difíciles.", "stem4l2"),
    ("Referencia", "Persona que puede dar contexto sobre tu trabajo pasado y confirmar lo que dices en el proceso.", "stem6l2"),
    ("Revisión trimestral", "Chequeo periódico de apuestas, resultados y aprendizaje para corregir el rumbo antes de que sea tarde.", "stem7l2"),
    ("Riesgo existencial", "Problema que amenaza la supervivencia o la misión de la empresa y que exige atención prioritaria.", "stem2l1"),
    ("Sala", "Foro donde se toman decisiones relevantes; entrar y permanecer exige aportar algo distinto y tener patrocinio.", "stem5l3"),
    ("SCQA", "Apertura de documento en cuatro partes: situación, complicación, pregunta y respuesta.", "stem4l3"),
    ("Senior", "Nivel de carrera habitual antes de Staff; se espera autonomía técnica, pero no necesariamente dirección organizacional.", "stem1l1"),
    ("Snacking", "Trabajo fácil y de bajo impacto que da sensación de avance y desplaza lo verdaderamente importante.", "stem2l1"),
    ("Solver", "Arquetipo que se incorpora a problemas urgentes y difíciles, los desatasca y luego pasa a otro frente.", "stem1l2"),
    ("Staff-plus", "Etiqueta que agrupa los títulos Staff, Principal y Distinguished.", "stem1l1"),
    ("Tech Lead", "Arquetipo que guía la ejecución de un equipo o conjunto de equipos y sostiene su contexto técnico.", "stem1l2"),
    ("Título", "Reconocimiento formal de un nivel; abre puertas y conversaciones, pero no sustituye el trabajo que lo justifica.", "stem1l3"),
    ("Transparencia", "Práctica de hacer visible el trabajo, las decisiones y los motivos para que otros puedan confiar y aprender.", "stem4l2"),
    ("Vector técnico", "Dirección hacia la que apuntan las decisiones técnicas; alinearlas multiplica el efecto de cada esfuerzo.", "stem2l3"),
    ("Visibilidad", "Grado en que otros conocen tu trabajo y tu criterio; es un umbral que se cruza, no un fin en sí mismo.", "stem5l3"),
    ("Visión", "Imagen concreta y plausible del futuro técnico a dos o tres años que ayuda a conciliar estrategias distintas.", "stem2l2"),
]
