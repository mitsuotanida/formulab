from sqlalchemy.orm import Session
from app.models.exercise import Exercise

EXERCISES = [
    {
        "title": "Producción de P1 y P2 en dos máquinas",
        "description": "Una pequeña empresa manufacturera fabrica dos tipos de productos, P1 y P2, los cuales deben ser procesados en dos máquinas M1 y M2. Cada máquina tiene disponibilidad diaria de 8 hrs. Las tasas de producción en [unid./hora] y la utilidad unitaria neta se muestran en la tabla. La empresa desea planificar la producción diaria para maximizar la utilidad neta total.",
        "data_table": {"headers": ["Máquina", "P1 (unid/hr)", "P2 (unid/hr)", "Disponibilidad"], "rows": [["M1", "5", "6", "8 hr/día"], ["M2", "4", "8", "8 hr/día"], ["Utilidad neta (u.m.)", "6", "4", ""]]},
        "domain": "production", "type": "LP", "difficulty": "easy", "ra_ids": [1, 2, 3],
        "hints": [{"order": 1, "text": "Define x1 como unidades de P1 y x2 como unidades de P2 producidas por día."}, {"order": 2, "text": "Para la restricción de M1: cada unidad de P1 toma 1/5 hr y cada unidad de P2 toma 1/6 hr."}, {"order": 3, "text": "No olvides las restricciones de no negatividad: x1 ≥ 0, x2 ≥ 0."}],
        "reference_solution": {"variables": "x₁ = unidades de P1 producidas por día\nx₂ = unidades de P2 producidas por día", "objective": "Max Z = 6x₁ + 4x₂", "constraints": "(1/5)x₁ + (1/6)x₂ ≤ 8  (disponibilidad M1)\n(1/4)x₁ + (1/8)x₂ ≤ 8  (disponibilidad M2)\nx₁ ≥ 0, x₂ ≥ 0  (no negatividad)"},
    },
    {
        "title": "Mezcla de vitaminas con verduras",
        "description": "Se dispone de cinco tipos de verduras para preparar una mezcla que debe cumplir requerimientos mínimos de vitaminas A y C. La mezcla debe contener al menos 10 unidades de vitamina A y 25 unidades de vitamina C. Los contenidos vitamínicos y costos por unidad se muestran en la tabla. Formule el modelo que minimiza el costo total de la mezcla.",
        "data_table": {"headers": ["Verdura", "Vitamina A (u/kg)", "Vitamina C (u/kg)", "Costo ($/kg)"], "rows": [["V1", "3", "2", "4"], ["V2", "1", "5", "3"], ["V3", "2", "3", "5"], ["V4", "4", "1", "2"], ["V5", "0", "4", "3"]]},
        "domain": "production", "type": "LP", "difficulty": "easy", "ra_ids": [1, 2, 3],
        "hints": [{"order": 1, "text": "Define xᵢ como la cantidad en kg de la verdura i a incluir en la mezcla."}, {"order": 2, "text": "Las restricciones son de tipo ≥ (mínimos de vitaminas)."}],
        "reference_solution": {"variables": "xᵢ = kg de verdura i en la mezcla, i=1,...,5", "objective": "Min Z = 4x₁ + 3x₂ + 5x₃ + 2x₄ + 3x₅", "constraints": "3x₁ + x₂ + 2x₃ + 4x₄ ≥ 10  (vitamina A)\n2x₁ + 5x₂ + 3x₃ + x₄ + 4x₅ ≥ 25  (vitamina C)\nxᵢ ≥ 0 para todo i"},
    },
    {
        "title": "Distribución de azúcar entre proveedores",
        "description": "Un comerciante compra azúcar a granel y la vende en envases de 1 kg (a $300/kg) y 5 kg (a $250/kg). La demanda máxima es 20.000 kg (envases 1 kg) y 17.000 kg (envases 5 kg). Debe entregar obligatoriamente 5.000 kg en envases de 5 kg a un cliente fijo. Tiene dos proveedores: Proveedor 1 ofrece máximo 15.000 kg a $90/kg; Proveedor 2 cantidad ilimitada a $110/kg. Al menos 1/3 del azúcar total debe ir en envases de 1 kg.",
        "data_table": None,
        "domain": "logistics", "type": "LP", "difficulty": "medium", "ra_ids": [1, 2, 3],
        "hints": [{"order": 1, "text": "Necesitas 4 variables: una por cada combinación (proveedor, tipo de envase)."}, {"order": 2, "text": "La restricción de 1/3 en envases de 1 kg puede reescribirse: (x₁+x₃) ≥ (1/3)(x₁+x₂+x₃+x₄)."}],
        "reference_solution": {"variables": "x₁ = kg de prov.1 en envases 1kg\nx₂ = kg de prov.1 en envases 5kg\nx₃ = kg de prov.2 en envases 1kg\nx₄ = kg de prov.2 en envases 5kg", "objective": "Max Z = 210x₁ + 160x₂ + 190x₃ + 140x₄", "constraints": "x₁ + x₂ ≤ 15.000  (capacidad prov.1)\nx₁ + x₃ ≤ 20.000  (demanda envases 1kg)\nx₂ + x₄ ≤ 17.000  (demanda envases 5kg)\nx₂ + x₄ ≥ 5.000  (cliente fijo)\n2(x₁+x₃) ≥ x₂+x₄  (al menos 1/3 en envases 1kg)\nxᵢ ≥ 0"},
    },
    {
        "title": "Planificación de cultivos en fundo agrícola",
        "description": "Una oficina de coordinación agrícola administra 3 parcelas con restricciones de agua y tierra. Se pueden sembrar tres especies: alfalfa, ballica y trébol. Los datos de superficie arable, dotación de agua, consumo hídrico por hectárea, cuotas máximas y rentabilidad neta se muestran en la tabla. Además, la misma fracción de tierra cultivable debe sembrarse en cada parcela.",
        "data_table": {"headers": ["", "Parcela 1", "Parcela 2", "Parcela 3"], "rows": [["Tierra cultivable (ha)", "400", "600", "300"], ["Agua disponible (m³)", "600", "800", "375"], ["Consumo Alfalfa (m³/ha)", "3", "3", "3"], ["Consumo Ballica (m³/ha)", "2", "2", "2"], ["Consumo Trébol (m³/ha)", "1", "1", "1"], ["Cuota máx Alfalfa (ha)", "600", "", ""], ["Cuota máx Ballica (ha)", "500", "", ""], ["Cuota máx Trébol (ha)", "325", "", ""], ["Rentabilidad Alfalfa ($/ha)", "400", "", ""], ["Rentabilidad Ballica ($/ha)", "300", "", ""], ["Rentabilidad Trébol ($/ha)", "100", "", ""]]},
        "domain": "agriculture", "type": "LP", "difficulty": "medium", "ra_ids": [1, 2, 3],
        "hints": [{"order": 1, "text": "Define x_{c,p} = hectáreas del cultivo c en la parcela p (3 cultivos × 3 parcelas = 9 variables)."}, {"order": 2, "text": "La restricción de igual fracción: Σc x_{c,1}/400 = Σc x_{c,2}/600 = Σc x_{c,3}/300."}],
        "reference_solution": {"variables": "x_{c,p} = hectáreas del cultivo c en parcela p (c∈{A,B,T}, p∈{1,2,3})", "objective": "Max Z = 400(x_{A,1}+x_{A,2}+x_{A,3}) + 300(x_{B,1}+x_{B,2}+x_{B,3}) + 100(x_{T,1}+x_{T,2}+x_{T,3})", "constraints": "Σc x_{c,p} ≤ Tierra_p  (tierra por parcela)\n3x_{A,p} + 2x_{B,p} + x_{T,p} ≤ Agua_p  (agua por parcela)\nΣp x_{A,p} ≤ 600; Σp x_{B,p} ≤ 500; Σp x_{T,p} ≤ 325  (cuotas)\nΣc x_{c,1}/400 = Σc x_{c,2}/600 = Σc x_{c,3}/300  (igual fracción)\nx_{c,p} ≥ 0"},
    },
    {
        "title": "Portafolio básico de inversión",
        "description": "Un inversionista dispone de un presupuesto B para construir un portafolio con N activos disponibles. Cada activo n tiene rentabilidad Rₙ y cantidad máxima disponible Sₙ. Por diversificación, no se puede invertir más del 30% del presupuesto en un solo activo. Formule el modelo que maximiza la rentabilidad total del portafolio.",
        "data_table": None,
        "domain": "finance", "type": "LP", "difficulty": "medium", "ra_ids": [1, 2, 3],
        "hints": [{"order": 1, "text": "La variable de decisión es xₙ = pesos invertidos en el activo n."}, {"order": 2, "text": "La restricción de diversificación: xₙ ≤ 0.3·B para cada activo n."}],
        "reference_solution": {"variables": "xₙ = pesos invertidos en activo n (n=1,...,N)", "objective": "Max Z = Σₙ Rₙ·xₙ", "constraints": "Σₙ xₙ = B  (uso total del presupuesto)\nxₙ ≤ 0.3·B  (diversificación)\nxₙ ≤ Sₙ  (disponibilidad de cada activo)\nxₙ ≥ 0"},
    },
    {
        "title": "Producción con costo fijo de arranque de máquina",
        "description": "Una planta fabrica 3 productos (P1, P2, P3) usando 2 máquinas (M1, M2). Para producir en una máquina, ésta debe ser 'arrancada', incurriendo en un costo fijo. El costo de arranque de M1 es $500 y de M2 es $800. Cada máquina solo puede producir si fue arrancada (capacidad total de 100 unidades por máquina). La utilidad neta por unidad y las horas requeridas por unidad en cada máquina se dan en la tabla. Formule el MIP que maximiza la utilidad neta total.",
        "data_table": {"headers": ["", "P1", "P2", "P3", "Cap. máquina"], "rows": [["Hrs en M1", "2", "3", "1", "100"], ["Hrs en M2", "1", "2", "4", "100"], ["Utilidad neta ($)", "15", "20", "12", ""]]},
        "domain": "production", "type": "MIP", "difficulty": "medium", "ra_ids": [1, 2, 4, 5],
        "hints": [{"order": 1, "text": "Necesitas variables binarias yₖ = 1 si la máquina k es arrancada, 0 si no."}, {"order": 2, "text": "Restricción de enlace: la producción total en máquina k debe ser ≤ 100·yₖ (big-M)."}],
        "reference_solution": {"variables": "xⱼ = unidades del producto j producidas (j=1,2,3)\nyₖ = 1 si la máquina k es arrancada, 0 si no (k=1,2)", "objective": "Max Z = 15x₁ + 20x₂ + 12x₃ - 500y₁ - 800y₂", "constraints": "2x₁ + 3x₂ + x₃ ≤ 100·y₁  (capacidad M1 con arranque)\nx₁ + 2x₂ + 4x₃ ≤ 100·y₂  (capacidad M2 con arranque)\nxⱼ ≥ 0  (no negatividad)\nyₖ ∈ {0,1}  (binariedad)"},
    },
    {
        "title": "Localización de centros de distribución",
        "description": "LogiChile debe abastecer 3 ciudades (Maipú: 45 ton/mes, Puente Alto: 35 ton/mes, San Bernardo: 30 ton/mes) desde potenciales centros de distribución (CD) en Pudahuel, Lo Espejo y Quilicura. Abrir cada CD tiene un costo fijo mensual. Si se abre, puede enviar hasta su capacidad máxima. Cada ciudad DEBE ser abastecida completamente. Minimice el costo total (fijo + transporte).",
        "data_table": {"headers": ["CD", "Costo fijo (M$/mes)", "Cap. (ton/mes)", "c/ Maipú ($/ton)", "c/ P.Alto ($/ton)", "c/ S.Bdo ($/ton)"], "rows": [["Pudahuel", "2.5", "80", "120", "200", "150"], ["Lo Espejo", "1.8", "60", "180", "130", "90"], ["Quilicura", "2.1", "70", "160", "110", "200"]]},
        "domain": "logistics", "type": "MIP", "difficulty": "hard", "ra_ids": [4, 5],
        "hints": [{"order": 1, "text": "Variables: xᵢⱼ = toneladas enviadas de CD i a ciudad j (continua); yᵢ = 1 si se abre CD i (binaria)."}, {"order": 2, "text": "Restricción de capacidad con enlace: Σⱼ xᵢⱼ ≤ Capᵢ·yᵢ para cada CD i."}, {"order": 3, "text": "Restricción de demanda: Σᵢ xᵢⱼ = dⱼ para cada ciudad j."}],
        "reference_solution": {"variables": "xᵢⱼ = ton enviadas de CD i a ciudad j (i∈{1,2,3}, j∈{M,P,S})\nyᵢ = 1 si se abre CD i, 0 si no", "objective": "Min Z = 2.500.000y₁ + 1.800.000y₂ + 2.100.000y₃ + Σᵢⱼ cᵢⱼ·xᵢⱼ", "constraints": "Σᵢ xᵢⱼ = dⱼ  (demanda completa de ciudad j)\nΣⱼ xᵢⱼ ≤ Capᵢ·yᵢ  (capacidad + enlace con apertura)\nxᵢⱼ ≥ 0, yᵢ ∈ {0,1}"},
    },
    {
        "title": "Selección de proyectos con restricciones lógicas",
        "description": "Una empresa evalúa 5 proyectos de inversión (P1 a P5). Cada proyecto tiene un VPN y un costo. El presupuesto total disponible es $10M. Adicionalmente: (1) Si se selecciona P1, NO se puede seleccionar P2. (2) Si se seleccionan P3 Y P4 simultáneamente, DEBE seleccionarse P5. (3) Se deben elegir entre 2 y 4 proyectos en total. Maximice el VPN total.",
        "data_table": {"headers": ["Proyecto", "VPN (M$)", "Costo (M$)"], "rows": [["P1", "4.5", "3"], ["P2", "3.2", "2"], ["P3", "5.1", "4"], ["P4", "2.8", "2"], ["P5", "1.9", "1"]]},
        "domain": "finance", "type": "MIP", "difficulty": "hard", "ra_ids": [4, 5],
        "hints": [{"order": 1, "text": "Define yⱼ = 1 si se selecciona el proyecto j, 0 si no (binaria)."}, {"order": 2, "text": "Regla 1 (exclusión mutua): y₁ + y₂ ≤ 1."}, {"order": 3, "text": "Regla 2 (P3 y P4 implican P5): y₃ + y₄ - 1 ≤ y₅."}],
        "reference_solution": {"variables": "yⱼ = 1 si se selecciona proyecto j, 0 si no (j=1,...,5)", "objective": "Max Z = 4.5y₁ + 3.2y₂ + 5.1y₃ + 2.8y₄ + 1.9y₅", "constraints": "3y₁ + 2y₂ + 4y₃ + 2y₄ + y₅ ≤ 10  (presupuesto)\ny₁ + y₂ ≤ 1  (exclusión mutua P1 y P2)\ny₃ + y₄ - 1 ≤ y₅  (P3∧P4 → P5)\n2 ≤ Σⱼ yⱼ ≤ 4  (número de proyectos)\nyⱼ ∈ {0,1}"},
    },
    {
        "title": "Minimización de desviaciones absolutas de meta",
        "description": "Una empresa de manufactura tiene metas de producción mensual para 3 productos: meta₁=100, meta₂=150, meta₃=80 unidades. La producción real xᵢ puede desviarse de la meta. El costo de desviación es $5 por unidad de desviación en cualquier dirección (sobreproducción o subproducción). La capacidad total de producción es 320 unidades. Formule el modelo que minimiza el costo total de desviación.",
        "data_table": None,
        "domain": "production", "type": "NLP", "difficulty": "medium", "ra_ids": [1, 2, 3, 5],
        "hints": [{"order": 1, "text": "La función objetivo con valor absoluto |xᵢ - metaᵢ| no es diferenciable. Introduce variables auxiliares dᵢ⁺ y dᵢ⁻ para linealizar."}, {"order": 2, "text": "Define: xᵢ - metaᵢ = dᵢ⁺ - dᵢ⁻, con dᵢ⁺, dᵢ⁻ ≥ 0. Entonces |xᵢ - metaᵢ| = dᵢ⁺ + dᵢ⁻."}],
        "reference_solution": {"variables": "xᵢ = unidades producidas del producto i (i=1,2,3)\ndᵢ⁺ = unidades sobre la meta del producto i\ndᵢ⁻ = unidades bajo la meta del producto i", "objective": "Min Z = 5Σᵢ(dᵢ⁺ + dᵢ⁻)", "constraints": "xᵢ - metaᵢ = dᵢ⁺ - dᵢ⁻  (definición desviación, para cada i)\nx₁ + x₂ + x₃ ≤ 320  (capacidad total)\ndᵢ⁺, dᵢ⁻ ≥ 0; xᵢ ≥ 0"},
    },
    {
        "title": "Despacho económico de unidades generadoras",
        "description": "Un sistema eléctrico tiene 3 unidades generadoras (G1, G2, G3) con costos de operación cuadráticos: C₁(P₁) = 0.002P₁² + 2P₁ + 10, C₂(P₂) = 0.003P₂² + 1.5P₂ + 8, C₃(P₃) = 0.001P₃² + 3P₃ + 12 (en $/hr). La demanda total del sistema es 400 MW. Cada generador tiene límites de potencia: G1 [50,200] MW, G2 [30,150] MW, G3 [80,300] MW. Minimice el costo total de operación.",
        "data_table": {"headers": ["Generador", "a ($/MW²hr)", "b ($/MWhr)", "c ($/hr)", "Pmin (MW)", "Pmax (MW)"], "rows": [["G1", "0.002", "2", "10", "50", "200"], ["G2", "0.003", "1.5", "8", "30", "150"], ["G3", "0.001", "3", "12", "80", "300"]]},
        "domain": "energy", "type": "NLP", "difficulty": "hard", "ra_ids": [1, 2, 3, 5],
        "hints": [{"order": 1, "text": "Las funciones de costo son cuadráticas en Pᵢ, por lo que el modelo es NLP (programación no lineal)."}, {"order": 2, "text": "La restricción de balance de potencia: P₁ + P₂ + P₃ = 400 MW (igualdad estricta)."}],
        "reference_solution": {"variables": "Pᵢ = potencia generada por la unidad i en MW (i=1,2,3)", "objective": "Min Z = 0.002P₁² + 2P₁ + 10 + 0.003P₂² + 1.5P₂ + 8 + 0.001P₃² + 3P₃ + 12", "constraints": "P₁ + P₂ + P₃ = 400  (balance de potencia)\n50 ≤ P₁ ≤ 200  (límites G1)\n30 ≤ P₂ ≤ 150  (límites G2)\n80 ≤ P₃ ≤ 300  (límites G3)"},
    },
    {
        "title": "Planificación de inventario multi-período",
        "description": "Una empresa planifica producción e inventario para 4 períodos. Tiene capacidad de producción de 200 unidades/período. El costo de producción es $10/unidad y el costo de mantención de inventario es $2/unidad/período. La demanda por período es: D₁=100, D₂=150, D₃=120, D₄=180. El inventario inicial es 50 unidades y se requiere un inventario final mínimo de 30 unidades. Minimice el costo total.",
        "data_table": {"headers": ["Período", "Demanda (unid)", "Cap. prod. (unid)", "C. producción ($/u)", "C. inventario ($/u/per)"], "rows": [["1", "100", "200", "10", "2"], ["2", "150", "200", "10", "2"], ["3", "120", "200", "10", "2"], ["4", "180", "200", "10", "2"]]},
        "domain": "inventory", "type": "LP", "difficulty": "medium", "ra_ids": [1, 2, 3],
        "hints": [{"order": 1, "text": "Necesitas dos conjuntos de variables: xₜ (producción en período t) e Iₜ (inventario al final del período t)."}, {"order": 2, "text": "Balance de inventario: Iₜ = Iₜ₋₁ + xₜ - Dₜ para t=1,...,4 (con I₀=50)."}],
        "reference_solution": {"variables": "xₜ = unidades producidas en período t (t=1,...,4)\nIₜ = inventario al final del período t", "objective": "Min Z = 10(x₁+x₂+x₃+x₄) + 2(I₁+I₂+I₃+I₄)", "constraints": "I₀ = 50  (inventario inicial)\nIₜ = Iₜ₋₁ + xₜ - Dₜ  (balance de inventario, t=1,...,4)\n0 ≤ xₜ ≤ 200  (capacidad de producción)\nI₄ ≥ 30  (inventario final mínimo)\nIₜ ≥ 0  (no negatividad de inventario)"},
    },
    {
        "title": "Red de distribución de papayas (tres eslabones)",
        "description": "Una empresa frutícola transporta papayas desde I campos de cultivo a J plantas procesadoras, y luego a K centros de venta. El precio de venta es P ($/kg). Los costos de transporte son aᵢⱼ ($/kg) de campo i a planta j, y bⱼₖ ($/ton) de planta j a centro k. La capacidad de cada planta es cⱼ kg/temporada. La demanda mínima de cada centro es dₖ kg. La producción de cada campo es eᵢ kg. Formule el modelo paramétrico que maximiza el beneficio neto total.",
        "data_table": None,
        "domain": "logistics", "type": "LP", "difficulty": "hard", "ra_ids": [1, 2, 3],
        "hints": [{"order": 1, "text": "Necesitas dos conjuntos de variables de flujo: xᵢⱼ (campo→planta) y yⱼₖ (planta→centro)."}, {"order": 2, "text": "Balance de flujo en cada planta j: Σᵢ xᵢⱼ = Σₖ yⱼₖ (lo que entra = lo que sale)."}],
        "reference_solution": {"variables": "xᵢⱼ = kg enviados del campo i a la planta j\nyⱼₖ = kg enviados de la planta j al centro k", "objective": "Max Z = P·Σⱼₖ yⱼₖ - Σᵢⱼ aᵢⱼ·xᵢⱼ - Σⱼₖ bⱼₖ·yⱼₖ", "constraints": "Σⱼ xᵢⱼ ≤ eᵢ  (producción de campo i)\nΣⱼ yⱼₖ ≥ dₖ  (demanda mínima del centro k)\nΣᵢ xᵢⱼ ≤ cⱼ  (capacidad de planta j)\nΣᵢ xᵢⱼ = Σₖ yⱼₖ  (balance de flujo en planta j)\nxᵢⱼ, yⱼₖ ≥ 0"},
    },
    {
        "title": "Transporte de maíz con asignación todo-o-nada",
        "description": "Un importador recibe maíz en 3 puertos (S₁, S₂, S₃) con disponibilidades S₁=5000, S₂=7000, S₃=4000 toneladas. Debe distribuirlo a 5 clientes, cada uno con un pedido Qⱼ toneladas. La restricción clave es que un cliente debe recibir TODO su pedido de UN SOLO puerto (decisión todo-o-nada). El beneficio por tonelada enviada del puerto i al cliente j es Bᵢⱼ. Maximice el beneficio total.",
        "data_table": None,
        "domain": "logistics", "type": "MIP", "difficulty": "hard", "ra_ids": [4, 5],
        "hints": [{"order": 1, "text": "Necesitas una variable binaria yⱼ para indicar si el cliente j es atendido desde el puerto que maximice el beneficio. Mejor: variable binaria zᵢⱼ = 1 si el cliente j es atendido desde el puerto i."}, {"order": 2, "text": "La cantidad enviada: xᵢⱼ = Qⱼ·zᵢⱼ (si el cliente j viene del puerto i, recibe todo su pedido)."}],
        "reference_solution": {"variables": "xᵢⱼ = toneladas enviadas del puerto i al cliente j\nzᵢⱼ = 1 si el cliente j es abastecido por el puerto i, 0 si no", "objective": "Max Z = ΣᵢΣⱼ Bᵢⱼ·xᵢⱼ", "constraints": "Σⱼ xᵢⱼ ≤ Sᵢ  (disponibilidad en puerto i)\nxᵢⱼ = Qⱼ·zᵢⱼ  (todo-o-nada: cliente j recibe Qⱼ desde i si zᵢⱼ=1)\nΣᵢ zᵢⱼ ≤ 1  (cada cliente es atendido por a lo más un puerto)\nxᵢⱼ ≥ 0, zᵢⱼ ∈ {0,1}"},
    },
    {
        "title": "Minimización de norma cuadrática con restricción",
        "description": "Se desea encontrar el vector x = (x₁, x₂, x₃) de mínima norma euclídea que satisfaga la restricción presupuestaria: x₁ + x₂ + x₃ = 1, con xᵢ ≥ 0 para todo i. Formule el modelo de optimización no lineal correspondiente e identifique el tipo de modelo.",
        "data_table": None,
        "domain": "generic", "type": "NLP", "difficulty": "hard", "ra_ids": [1, 2, 5],
        "hints": [{"order": 1, "text": "La norma euclídea al cuadrado es x₁² + x₂² + x₃², que es una función convexa cuadrática."}, {"order": 2, "text": "El modelo tiene una restricción de igualdad y restricciones de no negatividad."}],
        "reference_solution": {"variables": "xᵢ = componente i del vector (i=1,2,3), xᵢ ≥ 0", "objective": "Min Z = x₁² + x₂² + x₃²  (norma euclídea al cuadrado)", "constraints": "x₁ + x₂ + x₃ = 1  (restricción presupuestaria)\nx₁, x₂, x₃ ≥ 0\nTipo: NLP convexo (objetivo cuadrático convexo, factible convexo)"},
    },
    {
        "title": "Producción multi-planta multi-período BioFarm Chile",
        "description": "BioFarm Chile produce tres suplementos — Proteína (P), Vitaminas (V) y Colágeno (C) — en dos plantas: PL1 (Santiago) y PL2 (Antofagasta). La planificación abarca 3 períodos mensuales (t=1: Enero, t=2: Febrero, t=3: Marzo).\n\nCada planta puede operar o no en cada período, incurriendo en un costo fijo mensual si opera: f₁ = $200/mes (PL1) y f₂ = $150/mes (PL2). La capacidad disponible en horas-máquina es Cap₁ = 120 hr/mes y Cap₂ = 100 hr/mes. Se permite mantener inventario al final de cada período. El inventario inicial es cero para todos los productos. Los costos de producción, consumo de horas-máquina, costo de inventario y demandas mensuales se detallan en la tabla.\n\nLa demanda de cada producto debe satisfacerse exactamente en cada mes (combinando producción del período e inventario previo). Formule el modelo MIP que minimiza el costo total (producción + inventario + costo fijo de operación). Defina explícitamente los conjuntos de índices, los parámetros, las variables de decisión, la función objetivo con notación de sumatoria y las restricciones indicando el conjunto de índices sobre el cual aplica cada una.",
        "data_table": {
            "headers": ["Parámetro", "Proteína (P)", "Vitaminas (V)", "Colágeno (C)"],
            "rows": [
                ["PL1 – Costo prod. ($/u)", "8", "12", "10"],
                ["PL2 – Costo prod. ($/u)", "10", "9", "11"],
                ["PL1 – Consumo máq. (hr/u)", "2", "3", "1"],
                ["PL2 – Consumo máq. (hr/u)", "1", "2", "3"],
                ["Costo inventario ($/u/mes)", "1", "2", "1,5"],
                ["Demanda Enero (unid.)", "20", "15", "25"],
                ["Demanda Febrero (unid.)", "30", "20", "25"],
                ["Demanda Marzo (unid.)", "25", "18", "30"],
            ]
        },
        "domain": "production",
        "type": "MIP",
        "difficulty": "hard",
        "ra_ids": [1, 2, 3, 4, 5],
        "hints": [
            {"order": 1, "text": "Define 3 conjuntos de índices: I={1,2} para plantas, J={P,V,C} para productos, T={1,2,3} para meses. La variable de producción es tridimensional: xᵢⱼₜ."},
            {"order": 2, "text": "La restricción de capacidad debe enlazar producción con la decisión binaria de operar: Σⱼ rᵢⱼ·xᵢⱼₜ ≤ Capᵢ·yᵢₜ  para todo i∈I, t∈T. Si yᵢₜ=0, la planta no puede producir (Capᵢ actúa como big-M)."},
            {"order": 3, "text": "El balance de inventario conecta períodos: Iⱼ,ₜ₋₁ + Σᵢ xᵢⱼₜ − Iⱼₜ = dⱼₜ  para todo j∈J, t∈T, con Iⱼ₀ = 0."},
        ],
        "reference_solution": {
            "variables": "Conjuntos:\nI = {1,2}: plantas (PL1-Santiago, PL2-Antofagasta)\nJ = {P,V,C}: productos (Proteína, Vitaminas, Colágeno)\nT = {1,2,3}: períodos (Enero, Febrero, Marzo)\n\nParámetros:\ncᵢⱼ: costo de producir 1 unidad del producto j en planta i ($/u)\nrᵢⱼ: horas-máquina por unidad del producto j en planta i (hr/u)\nCapᵢ: capacidad en horas-máquina de planta i por período\ndⱼₜ: demanda del producto j en período t (unidades)\nhⱼ: costo de inventario del producto j ($/u/mes)\nfᵢ: costo fijo de operación de planta i por período ($)\n\nVariables de decisión:\nxᵢⱼₜ ≥ 0: unidades del producto j producidas en planta i en período t  ∀i∈I, j∈J, t∈T\nIⱼₜ ≥ 0: inventario del producto j al final del período t  ∀j∈J, t∈T\nyᵢₜ ∈ {0,1}: 1 si planta i opera en período t, 0 si no  ∀i∈I, t∈T",
            "objective": "Min Z = ΣᵢΣⱼΣₜ cᵢⱼ·xᵢⱼₜ  +  ΣⱼΣₜ hⱼ·Iⱼₜ  +  ΣᵢΣₜ fᵢ·yᵢₜ",
            "constraints": "Σⱼ rᵢⱼ·xᵢⱼₜ ≤ Capᵢ·yᵢₜ   ∀i∈I, t∈T  (capacidad y enlace con operación)\nIⱼ,ₜ₋₁ + Σᵢ xᵢⱼₜ − Iⱼₜ = dⱼₜ   ∀j∈J, t∈T  (balance de inventario, Iⱼ₀=0)\nxᵢⱼₜ ≥ 0   ∀i∈I, j∈J, t∈T\nIⱼₜ ≥ 0   ∀j∈J, t∈T\nyᵢₜ ∈ {0,1}   ∀i∈I, t∈T\nModelo: MIP (variables continuas + binarias, restricciones lineales)"
        },
    },
    {
        "title": "Expansión de capacidad en puertos portuarios",
        "description": "Una empresa importadora de automóviles opera con 3 puertos (I, SA, PM) con capacidades actuales. La demanda aumentará en 20%. Cada puerto puede expandir su capacidad incurriendo en costos fijos (por construir) y costos variables de expansión por unidad adicional. El beneficio por auto transportado es $10.000. Debe decidir qué puertos expandir y cuánto para maximizar el beneficio neto total de transporte.",
        "data_table": {"headers": ["Puerto", "Cap. actual", "Costo fijo ($M)", "Costo variable ($/unid)", "Demanda asignada (actual)"], "rows": [["Iquique (I)", "5.000", "1.000", "1.000", "4.000"], ["San Antonio (SA)", "8.000", "1.800", "3.000", "7.000"], ["P. Montt (PM)", "6.000", "1.000", "1.800", "5.500"]]},
        "domain": "logistics", "type": "MIP", "difficulty": "hard", "ra_ids": [4, 5],
        "hints": [{"order": 1, "text": "Define yᵢ = 1 si se expande el puerto i (binaria) y uᵢ = unidades adicionales de capacidad construidas (continua ≥ 0)."}, {"order": 2, "text": "Si no se expande (yᵢ=0), no puede haber expansión: uᵢ ≤ M·yᵢ (restricción de enlace)."}],
        "reference_solution": {"variables": "xᵢ = autos transportados por puerto i\nuᵢ = unidades adicionales de capacidad en puerto i\nyᵢ = 1 si se expande puerto i, 0 si no", "objective": "Max Z = 10.000·Σᵢ xᵢ - Σᵢ(Fᵢ·yᵢ + Vᵢ·uᵢ)", "constraints": "xᵢ ≤ Capᵢ + uᵢ  (capacidad expandida)\nuᵢ ≤ M·yᵢ  (expansión solo si se invierte)\nxᵢ = 1.2·Dᵢ  (satisfacer demanda aumentada)\nuᵢ ≥ 0, yᵢ ∈ {0,1}"},
    },
]


def seed_exercises(db: Session, teacher_id) -> None:
    for ex_data in EXERCISES:
        existing = db.query(Exercise).filter(Exercise.title == ex_data["title"]).first()
        if not existing:
            db.add(Exercise(
                title=ex_data["title"],
                description=ex_data["description"],
                data_table=ex_data.get("data_table"),
                domain=ex_data["domain"],
                type=ex_data["type"],
                difficulty=ex_data["difficulty"],
                ra_ids=ex_data["ra_ids"],
                hints=ex_data.get("hints", []),
                reference_solution=ex_data.get("reference_solution"),
                ai_generated=False,
                created_by=teacher_id,
            ))
    db.commit()
    print(f"✓ {len(EXERCISES)} ejercicios seeded")
