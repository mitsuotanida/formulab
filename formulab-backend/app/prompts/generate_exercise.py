SYSTEM_PROMPT = """Eres un asistente experto en investigación de operaciones y programación matemática. Tu tarea es generar problemas de optimización para el curso CII 2750 Optimización de Ingeniería Industrial en Chile (Universidad Diego Portales).

REGLA CRÍTICA: Los problemas son ÚNICAMENTE de FORMULACIÓN del modelo matemático. Los estudiantes NO deben resolver el modelo, solo formularlo (definir variables, función objetivo y restricciones). Nunca incluyas la solución óptima, valores óptimos, ni métodos de solución (no simplex, no gráfico, no KKT).

CONTEXTO PREFERIDO: Usa empresas y escenarios del sector tecnológico: startups SaaS, plataformas cloud (estilo AWS/Azure), data centers, CDN, fintech, e-commerce, empresas de software, telecomunicaciones, ciberseguridad, plataformas de streaming, etc. Si el dominio no es tech, usa empresas latinoamericanas reconocidas (Falabella, Entel, Mercado Libre, Rappi, etc.).

REGLA DE ENUNCIADO AUTOCONTENIDO: El enunciado debe incluir TODOS los datos necesarios para formular la solución completa. Un estudiante que lea el enunciado debe poder inferir directamente las variables, la función objetivo y cada restricción, sin ambigüedades.

ESTRUCTURA DEL OUTPUT: Responde ÚNICAMENTE con un JSON válido con esta estructura exacta:
{
  "title": "Título descriptivo del problema – NombreEmpresa (máx 80 caracteres)",
  "description": "Narrativa completa y autocontenida. Todos los parámetros deben estar definidos (con nombre, valor o notación) en el texto o en la tabla.",
  "data_table": {
    "headers": ["columna1", "columna2", ...],
    "rows": [["val1", "val2", ...], ...]
  },
  "question": "Formule el modelo de programación matemática. Defina claramente las variables de decisión, la función objetivo y todas las restricciones.",
  "ra_ids": [1, 2, 3],
  "reference_solution": {
    "variables": "definición de variables con unidades",
    "objective": "función objetivo con dirección y expresión matemática completa",
    "constraints": "lista de restricciones con interpretación en lenguaje natural"
  }
}

Si el problema no necesita tabla de datos, omite data_table (null).

GUÍA DE CALIDAD:
- LP fácil: 2-3 variables, 2-4 restricciones, contexto tech cotidiano
- LP/MIP medio: 3-5 variables, 4-7 restricciones, contexto operacional tech
- MIP/NLP difícil: variables binarias o no linealidades explícitas, 5-10 restricciones
- Para MIP: incluir al menos una variable binaria con lógica de sí/no, todo-o-nada, o costos fijos
- Para NLP: incluir valor absoluto (linealizable), función cuadrática, o producto de variables
- Cohesión: cada dato numérico en el enunciado debe aparecer en exactamente una restricción o en el objetivo
"""

FEW_SHOT_EXAMPLES = [
    {
        "role": "user",
        "content": "Genera un problema LP, dominio production, dificultad easy, RA foco [1,2,3]",
    },
    {
        "role": "assistant",
        "content": """{
  "title": "Procesamiento de tareas en servidores cloud – NexusCloud",
  "description": "NexusCloud procesa dos tipos de tareas en su infraestructura cloud: renderizado de video (R) y entrenamiento de modelos ML (M). Dispone de dos clusters de servidores: Cluster A (CA) y Cluster B (CB), con 10 horas diarias de operación cada uno. Las tasas de procesamiento [tareas/hora] son: CA procesa 4 tareas R y 6 tareas M por hora; CB procesa 5 tareas R y 3 tareas M por hora. El ingreso neto por tarea completada es $12 para R y $9 para M. Determine cuántas tareas de cada tipo procesar diariamente para maximizar el ingreso neto total sin exceder la disponibilidad de ningún cluster.",
  "data_table": {
    "headers": ["Cluster", "Renderizado R (tar/hr)", "ML Entrenamiento M (tar/hr)", "Disponibilidad"],
    "rows": [
      ["Cluster A (CA)", "4", "6", "10 hr/día"],
      ["Cluster B (CB)", "5", "3", "10 hr/día"],
      ["Ingreso neto ($/tarea)", "12", "9", ""]
    ]
  },
  "question": "Formule el modelo de programación lineal que maximiza el ingreso neto diario de NexusCloud. Defina las variables de decisión, la función objetivo y todas las restricciones.",
  "ra_ids": [1, 2, 3],
  "reference_solution": {
    "variables": "xR = tareas de renderizado procesadas por día\\nxM = tareas de entrenamiento ML procesadas por día",
    "objective": "Max Z = 12·xR + 9·xM",
    "constraints": "(1/4)xR + (1/6)xM <= 10  (disponibilidad CA)\\n(1/5)xR + (1/3)xM <= 10  (disponibilidad CB)\\nxR >= 0, xM >= 0  (no negatividad)"
  }
}""",
    },
    {
        "role": "user",
        "content": "Genera un problema MIP, dominio logistics, dificultad medium, RA foco [4,5]",
    },
    {
        "role": "assistant",
        "content": """{
  "title": "Ubicación de nodos de caché para red CDN – EdgeFlow",
  "description": "EdgeFlow debe atender la demanda de contenido de 3 regiones de usuarios: Región Norte (50 TB/mes), Región Centro (40 TB/mes), Región Sur (30 TB/mes). Evalúa instalar nodos de caché (NC) en tres ubicaciones: Iquique (NC1), Santiago (NC2) y Concepción (NC3). Instalar cada NC tiene un costo fijo mensual. Si se instala, puede transmitir hasta su capacidad máxima. Cada región debe recibir toda su demanda de contenido. Los costos de transmisión por TB desde cada NC a cada región se muestran en la tabla.",
  "data_table": {
    "headers": ["Nodo Caché", "Costo fijo (M$/mes)", "Cap. máx (TB/mes)", "Costo R.Norte ($/TB)", "Costo R.Centro ($/TB)", "Costo R.Sur ($/TB)"],
    "rows": [
      ["Iquique (NC1)", "1.200.000", "90", "100", "250", "180"],
      ["Santiago (NC2)", "1.800.000", "120", "200", "80", "120"],
      ["Concepción (NC3)", "1.000.000", "70", "220", "150", "90"]
    ]
  },
  "question": "Formule el MIP que minimiza el costo total mensual (fijo + transmisión). Defina variables continuas xij [TB] y binarias yi, la función objetivo y todas las restricciones incluyendo las restricciones de enlace.",
  "ra_ids": [4, 5],
  "reference_solution": {
    "variables": "xij = TB enviados del NC i a la región j (continua, >= 0)\\nyi = 1 si se instala el NC i, 0 si no (binaria)",
    "objective": "Min Z = 1.200.000·y1 + 1.800.000·y2 + 1.000.000·y3 + Sum_ij cij·xij",
    "constraints": "Sum_i xij = dj  para cada región j  (demanda completa)\\nSum_j xij <= Capi·yi  para cada NC i  (capacidad + enlace con instalación)\\nxij >= 0, yi en {0,1}"
  }
}""",
    },
]


def build_generation_messages(
    exercise_type: str,
    domain: str,
    difficulty: str,
    ra_focus: list[int],
    custom_context: str | None = None,
) -> list[dict]:
    user_request = f"Genera un problema {exercise_type}, dominio {domain}, dificultad {difficulty}, RA foco {ra_focus}"
    if custom_context:
        user_request += f". Contexto adicional: {custom_context}"
    messages = list(FEW_SHOT_EXAMPLES)
    messages.append({"role": "user", "content": user_request})
    return messages
