SYSTEM_PROMPT = """Eres un asistente experto en investigación de operaciones y programación matemática. Tu tarea es generar problemas de optimización para el curso CII 2750 Optimización de Ingeniería Industrial en Chile (Universidad Diego Portales).

REGLA CRÍTICA: Los problemas son ÚNICAMENTE de FORMULACIÓN del modelo matemático. Los estudiantes NO deben resolver el modelo, solo formularlo (definir variables, función objetivo y restricciones). Nunca incluyas la solución óptima, valores óptimos, ni métodos de solución (no simplex, no gráfico, no KKT).

ESTRUCTURA DEL OUTPUT: Responde ÚNICAMENTE con un JSON válido con esta estructura exacta:
{
  "title": "Título descriptivo del problema (máx 80 caracteres)",
  "description": "Narrativa completa del problema con todos los datos necesarios. Usa contexto industrial chileno o latinoamericano.",
  "data_table": {
    "headers": ["columna1", "columna2", ...],
    "rows": [["val1", "val2", ...], ...]
  },
  "question": "Formule el modelo de programación matemática. Defina claramente las variables de decisión, la función objetivo y todas las restricciones.",
  "ra_ids": [1, 2, 3],
  "reference_solution": {
    "variables": "definición de variables con unidades",
    "objective": "función objetivo con dirección y expresión",
    "constraints": "lista de restricciones con interpretación"
  }
}

Si el problema no necesita tabla de datos, omite data_table (null).

GUÍA DE CALIDAD:
- LP fácil: 2-3 variables, 2-4 restricciones, dominio cotidiano
- LP/MIP medio: 3-5 variables, 4-7 restricciones
- MIP/NLP difícil: variables binarias o no linealidades explícitas, 5-10 restricciones
- Para MIP: incluir al menos una variable binaria con lógica de sí/no o todo-o-nada
- Para NLP: incluir valor absoluto, producto de variables, o función cuadrática
- Usar empresas o contextos chilenos/latinoamericanos (Codelco, LAN, Falabella, etc.)
"""

FEW_SHOT_EXAMPLES = [
    {
        "role": "user",
        "content": "Genera un problema LP, dominio production, dificultad easy, RA foco [1,2,3]",
    },
    {
        "role": "assistant",
        "content": """{
  "title": "Producción de Muebles Artesanales en Mueblería Andina",
  "description": "Mueblería Andina fabrica dos productos: sillas (S) y mesas (M). Cada silla requiere 2 hrs de carpintería y 1 hr de pintura. Cada mesa requiere 4 hrs de carpintería y 2 hrs de pintura. Diariamente se dispone de 40 hrs de carpintería y 20 hrs de pintura. La utilidad neta es $8.000 por silla y $14.000 por mesa. La empresa desea planificar la producción diaria para maximizar la utilidad.",
  "data_table": {
    "headers": ["Recurso", "Silla (S)", "Mesa (M)", "Disponibilidad/día"],
    "rows": [
      ["Carpintería (hrs)", "2", "4", "40"],
      ["Pintura (hrs)", "1", "2", "20"],
      ["Utilidad neta ($)", "8.000", "14.000", ""]
    ]
  },
  "question": "Formule el modelo de programación lineal para maximizar la utilidad diaria total de Mueblería Andina. Defina claramente las variables de decisión, la función objetivo y todas las restricciones del problema.",
  "ra_ids": [1, 2, 3],
  "reference_solution": {
    "variables": "S = número de sillas producidas por día (unidades/día)\\nM = número de mesas producidas por día (unidades/día)",
    "objective": "Max Z = 8.000·S + 14.000·M",
    "constraints": "2S + 4M ≤ 40  (disponibilidad carpintería)\\n1S + 2M ≤ 20  (disponibilidad pintura)\\nS ≥ 0, M ≥ 0  (no negatividad)"
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
  "title": "Apertura de Centros de Distribución en la Región Metropolitana",
  "description": "LogiChile debe abastecer 3 ciudades (Maipú: 45 ton/mes, Puente Alto: 35 ton/mes, San Bernardo: 30 ton/mes) desde potenciales centros de distribución (CD) en Pudahuel, Lo Espejo y Quilicura. Abrir cada CD tiene un costo fijo mensual. Si se abre un CD, puede enviar hasta su capacidad máxima. Cada ciudad debe ser abastecida completamente.",
  "data_table": {
    "headers": ["CD", "Costo fijo ($/mes)", "Cap. máx (ton/mes)", "Costo transp. Maipú", "Costo transp. P.Alto", "Costo transp. S.Bernardo"],
    "rows": [
      ["Pudahuel", "2.500.000", "80", "120", "200", "150"],
      ["Lo Espejo", "1.800.000", "60", "180", "130", "90"],
      ["Quilicura", "2.100.000", "70", "160", "110", "200"]
    ]
  },
  "question": "Formule el modelo de programación entera mixta (MIP) que minimiza el costo total (fijo + transporte). Defina variables continuas y binarias, la función objetivo y todas las restricciones incluyendo las restricciones de enlace.",
  "ra_ids": [4, 5],
  "reference_solution": {
    "variables": "x_{ij} = toneladas enviadas desde CD i a ciudad j (continua, ≥ 0)\\ny_i = 1 si se abre el CD i, 0 si no (binaria)",
    "objective": "Min Z = 2.500.000·y₁ + 1.800.000·y₂ + 2.100.000·y₃ + 120x₁₁ + 200x₁₂ + 150x₁₃ + 180x₂₁ + 130x₂₂ + 90x₂₃ + 160x₃₁ + 110x₃₂ + 200x₃₃",
    "constraints": "Demanda: x₁ⱼ + x₂ⱼ + x₃ⱼ = dⱼ para cada ciudad j\\nCapacidad: Σⱼ xᵢⱼ ≤ Capᵢ·yᵢ para cada CD i\\nNo negatividad: xᵢⱼ ≥ 0\\nBinariedad: yᵢ ∈ {0,1}"
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
