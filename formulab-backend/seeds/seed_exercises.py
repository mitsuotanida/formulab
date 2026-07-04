from sqlalchemy.orm import Session
from app.models.exercise import Exercise

EXERCISES = [
    # ── LP EASY ────────────────────────────────────────────────────────────────
    {
        "title": "Procesamiento de solicitudes en clusters cloud – DataStream Analytics",
        "description": (
            "DataStream Analytics procesa dos tipos de solicitudes en su plataforma cloud: "
            "consultas SQL (tipo Q) y tareas de inferencia de Machine Learning (tipo M). "
            "La empresa dispone de dos clusters de servidores: Cluster GPU (CG) y Cluster CPU (CC), "
            "con 8 horas diarias de operación cada uno.\n\n"
            "Las tasas de procesamiento indican cuántas solicitudes por hora atiende cada cluster: "
            "CG procesa 5 solicitudes tipo Q y 6 tipo M por hora; "
            "CC procesa 4 solicitudes tipo Q y 8 tipo M por hora. "
            "El ingreso neto por solicitud completada es $6 para Q y $4 para M.\n\n"
            "Formule el modelo de programación lineal que determina cuántas solicitudes de cada tipo "
            "procesar diariamente para maximizar el ingreso neto total, sin superar la disponibilidad "
            "horaria de ningún cluster."
        ),
        "data_table": {
            "headers": ["Recurso", "SQL (Q) [solic/hr]", "ML (M) [solic/hr]", "Disponibilidad"],
            "rows": [
                ["Cluster GPU (CG)", "5", "6", "8 hr/día"],
                ["Cluster CPU (CC)", "4", "8", "8 hr/día"],
                ["Ingreso neto ($/solic.)", "6", "4", ""],
            ],
        },
        "domain": "production", "type": "LP", "difficulty": "easy", "ra_ids": [1, 2, 3],
        "hints": [
            {"order": 1, "text": "Define x_Q como solicitudes SQL y x_M como tareas ML procesadas por día."},
            {"order": 2, "text": "Si CG procesa 5 Q/hr, cada solicitud Q consume 1/5 hr de CG. Con 8 hr disponibles: (1/5)·x_Q + (1/6)·x_M ≤ 8."},
            {"order": 3, "text": "No olvides las restricciones de no negatividad: x_Q ≥ 0, x_M ≥ 0."},
        ],
        "reference_solution": {
            "variables": "x_Q = solicitudes tipo SQL procesadas por día\nx_M = tareas de ML procesadas por día",
            "objective": "Max Z = 6·x_Q + 4·x_M",
            "constraints": "(1/5)x_Q + (1/6)x_M ≤ 8  (disponibilidad CG)\n(1/4)x_Q + (1/8)x_M ≤ 8  (disponibilidad CC)\nx_Q ≥ 0, x_M ≥ 0  (no negatividad)",
        },
    },
    {
        "title": "Composición de infraestructura cloud con mínimo costo – CloudIoT",
        "description": (
            "CloudIoT necesita componer un paquete de infraestructura cloud que cumpla requerimientos "
            "mínimos de ancho de banda para su plataforma IoT: al menos 10 unidades de capacidad de "
            "subida (upload) y 25 unidades de capacidad de bajada (download) por mes.\n\n"
            "La empresa puede contratar unidades de cinco tipos de nodos (N1 a N5). Cada nodo tiene "
            "una capacidad de upload y download por unidad contratada, y un costo mensual fijo. "
            "Los datos se muestran en la tabla.\n\n"
            "Formule el modelo de programación lineal que determina cuántas unidades (xi >= 0) "
            "contratar de cada tipo de nodo para minimizar el costo mensual total, "
            "satisfaciendo los requerimientos mínimos de ancho de banda."
        ),
        "data_table": {
            "headers": ["Nodo", "Upload (u/nodo)", "Download (u/nodo)", "Costo ($/nodo/mes)"],
            "rows": [
                ["N1", "3", "2", "4"],
                ["N2", "1", "5", "3"],
                ["N3", "2", "3", "5"],
                ["N4", "4", "1", "2"],
                ["N5", "0", "4", "3"],
            ],
        },
        "domain": "production", "type": "LP", "difficulty": "easy", "ra_ids": [1, 2, 3],
        "hints": [
            {"order": 1, "text": "Define xi = unidades contratadas del nodo i (i=1,...,5)."},
            {"order": 2, "text": "Las restricciones de upload y download son de tipo >= (mínimos requeridos)."},
        ],
        "reference_solution": {
            "variables": "xi = unidades contratadas del nodo i (i=1,...,5)",
            "objective": "Min Z = 4x1 + 3x2 + 5x3 + 2x4 + 3x5",
            "constraints": "3x1 + x2 + 2x3 + 4x4 >= 10  (mínimo upload)\n2x1 + 5x2 + 3x3 + x4 + 4x5 >= 25  (mínimo download)\nxi >= 0 para todo i",
        },
    },
    # ── LP MEDIUM ──────────────────────────────────────────────────────────────
    {
        "title": "Distribución de licencias de software entre modalidades y proveedores – TechCorp",
        "description": (
            "TechCorp revende licencias de software en dos modalidades: individual "
            "(precio de venta: $300/licencia) y empresarial en paquetes de 5 "
            "(precio de venta: $250/licencia). La demanda máxima proyectada es "
            "20.000 licencias en modalidad individual y 17.000 en modalidad empresarial.\n\n"
            "TechCorp tiene un contrato fijo con un cliente corporativo que exige recibir "
            "obligatoriamente 5.000 licencias en modalidad empresarial. "
            "Cuenta con dos proveedores de licencias base: Proveedor 1 (P1) surte hasta 15.000 "
            "licencias a $90/licencia; Proveedor 2 (P2) tiene capacidad ilimitada a $110/licencia.\n\n"
            "Por política de diversificación de mercado, al menos un tercio del total de licencias "
            "vendidas debe ser en modalidad individual.\n\n"
            "Las variables de decisión son las cantidades de licencias compradas a cada proveedor y "
            "asignadas a cada modalidad. Formule el modelo de programación lineal que maximiza "
            "el margen neto total (precio de venta menos costo de compra)."
        ),
        "data_table": None,
        "domain": "logistics", "type": "LP", "difficulty": "medium", "ra_ids": [1, 2, 3],
        "hints": [
            {"order": 1, "text": "Necesitas 4 variables: una por cada combinación (proveedor x modalidad): x1 (P1->individual), x2 (P1->empresarial), x3 (P2->individual), x4 (P2->empresarial)."},
            {"order": 2, "text": "La política de 1/3 individual: (x1+x3) >= (1/3)(x1+x2+x3+x4), que se reescribe como 2(x1+x3) >= x2+x4."},
        ],
        "reference_solution": {
            "variables": "x1 = licencias de P1 vendidas en modalidad individual\nx2 = licencias de P1 vendidas en modalidad empresarial\nx3 = licencias de P2 vendidas en modalidad individual\nx4 = licencias de P2 vendidas en modalidad empresarial",
            "objective": "Max Z = (300-90)x1 + (250-90)x2 + (300-110)x3 + (250-110)x4\n       = 210x1 + 160x2 + 190x3 + 140x4",
            "constraints": "x1 + x2 <= 15.000  (capacidad P1)\nx1 + x3 <= 20.000  (demanda individual)\nx2 + x4 <= 17.000  (demanda empresarial)\nx2 + x4 >= 5.000  (contrato cliente corporativo)\n2(x1+x3) >= x2+x4  (al menos 1/3 en modalidad individual)\nxi >= 0",
        },
    },
    {
        "title": "Asignación de carga de trabajo en data centers multi-región – CloudNet",
        "description": (
            "CloudNet administra tres data centers regionales (DC1: São Paulo, DC2: Bogotá, "
            "DC3: Santiago) y ofrece tres tipos de servicios cloud: Compute (C), Storage (S) "
            "y Network (N). El objetivo es maximizar el ingreso neto mensual asignando "
            "rack-units (ru) a cada servicio en cada data center.\n\n"
            "Cada data center tiene una capacidad total de rack-units disponibles y un límite "
            "de ancho de banda mensual. El consumo de ancho de banda por rack-unit es: "
            "3 Gbps para Compute, 2 Gbps para Storage y 1 Gbps para Network "
            "(igual en todos los DCs). Los ingresos netos son: Compute=$400/ru, "
            "Storage=$300/ru, Network=$100/ru. Existen cuotas máximas de demanda global "
            "(suma de los tres DCs): Compute <= 600 ru, Storage <= 500 ru, Network <= 325 ru.\n\n"
            "Restricción operativa: la fracción de rack-units utilizados respecto al total disponible "
            "debe ser la misma en los tres data centers (política de uso uniforme de capacidad).\n\n"
            "Formule el modelo de programación lineal definiendo x_{c,p} = rack-units del "
            "servicio c en el data center p."
        ),
        "data_table": {
            "headers": ["", "DC1 (São Paulo)", "DC2 (Bogotá)", "DC3 (Santiago)"],
            "rows": [
                ["Rack-units disponibles", "400", "600", "300"],
                ["Ancho de banda (Gbps/mes)", "600", "800", "375"],
                ["Consumo Compute (Gbps/ru)", "3", "3", "3"],
                ["Consumo Storage (Gbps/ru)", "2", "2", "2"],
                ["Consumo Network (Gbps/ru)", "1", "1", "1"],
                ["Cuota máx. Compute (ru, total)", "600", "", ""],
                ["Cuota máx. Storage (ru, total)", "500", "", ""],
                ["Cuota máx. Network (ru, total)", "325", "", ""],
                ["Ingreso Compute ($/ru/mes)", "400", "", ""],
                ["Ingreso Storage ($/ru/mes)", "300", "", ""],
                ["Ingreso Network ($/ru/mes)", "100", "", ""],
            ],
        },
        "domain": "production", "type": "LP", "difficulty": "medium", "ra_ids": [1, 2, 3],
        "hints": [
            {"order": 1, "text": "Define x_{c,p} = rack-units del servicio c en el DC p (3 servicios x 3 DCs = 9 variables)."},
            {"order": 2, "text": "La restricción de uso uniforme: Sum_c x_{c,1}/400 = Sum_c x_{c,2}/600 = Sum_c x_{c,3}/300."},
        ],
        "reference_solution": {
            "variables": "x_{c,p} = rack-units del servicio c en el data center p\n(c en {C, S, N},  p en {1, 2, 3})",
            "objective": "Max Z = 400(x_{C,1}+x_{C,2}+x_{C,3}) + 300(x_{S,1}+x_{S,2}+x_{S,3}) + 100(x_{N,1}+x_{N,2}+x_{N,3})",
            "constraints": "Sum_c x_{c,p} <= RU_p  para todo p  (rack-units disponibles en DC p)\n3x_{C,p} + 2x_{S,p} + x_{N,p} <= BW_p  para todo p  (ancho de banda en DC p)\nSum_p x_{C,p} <= 600; Sum_p x_{S,p} <= 500; Sum_p x_{N,p} <= 325  (cuotas totales)\nSum_c x_{c,1}/400 = Sum_c x_{c,2}/600 = Sum_c x_{c,3}/300  (uso uniforme entre DCs)\nx_{c,p} >= 0",
        },
    },
    {
        "title": "Portafolio de inversión en startups tecnológicas – Fondo VC Andino",
        "description": (
            "El Fondo VC Andino dispone de un presupuesto B para construir un portafolio "
            "con N startups tecnológicas disponibles. Cada startup n ofrece una tasa de retorno "
            "esperada Rn y tiene un monto máximo disponible para inversión Sn "
            "(según la ronda de financiamiento abierta). "
            "Por política de diversificación, el fondo no puede invertir más del 30% del "
            "presupuesto total en una sola startup, independientemente de su potencial.\n\n"
            "Formule el modelo de programación lineal que determina cuánto invertir en "
            "cada startup (xn en pesos) para maximizar el retorno total esperado del portafolio, "
            "cumpliendo las restricciones de presupuesto, disponibilidad y diversificación."
        ),
        "data_table": None,
        "domain": "finance", "type": "LP", "difficulty": "medium", "ra_ids": [1, 2, 3],
        "hints": [
            {"order": 1, "text": "La variable de decisión es xn = pesos invertidos en la startup n."},
            {"order": 2, "text": "Restricción de diversificación: xn <= 0.3·B para cada startup n."},
        ],
        "reference_solution": {
            "variables": "xn = monto invertido en la startup n (n=1,...,N) [pesos]",
            "objective": "Max Z = Sum_n Rn·xn",
            "constraints": "Sum_n xn = B  (uso total del presupuesto)\nxn <= 0.3·B  para todo n  (diversificación: máximo 30% por startup)\nxn <= Sn  para todo n  (disponibilidad de la startup n)\nxn >= 0  para todo n",
        },
    },
    {
        "title": "Planificación de adquisición de licencias multi-período – Nexus Software",
        "description": (
            "Nexus Software debe planificar la compra de licencias de su plataforma de desarrollo "
            "durante 4 trimestres (T1 a T4). Cada trimestre, la empresa puede adquirir hasta "
            "200 licencias a un costo de $10 por licencia. Las licencias no utilizadas en un "
            "trimestre quedan disponibles para el siguiente, incurriendo en un costo de "
            "mantenimiento de $2 por licencia por trimestre.\n\n"
            "La demanda de licencias activas (número mínimo a tener disponible para los equipos) "
            "por trimestre es: D1=100, D2=150, D3=120, D4=180. El inventario inicial es "
            "I0=50 licencias. Al finalizar el año (cierre de T4), se requiere mantener un "
            "stock mínimo de 30 licencias activas como reserva para el siguiente año.\n\n"
            "Formule el modelo de programación lineal definiendo xt = licencias compradas en "
            "el trimestre t e It = licencias en inventario al cierre del trimestre t, "
            "para minimizar el costo total anual (compras + mantenimiento)."
        ),
        "data_table": {
            "headers": ["Trimestre", "Demanda (lic)", "Cap. compra (lic)", "Costo compra ($/lic)", "Costo mantención ($/lic/trim)"],
            "rows": [
                ["T1", "100", "200", "10", "2"],
                ["T2", "150", "200", "10", "2"],
                ["T3", "120", "200", "10", "2"],
                ["T4", "180", "200", "10", "2"],
            ],
        },
        "domain": "inventory", "type": "LP", "difficulty": "medium", "ra_ids": [1, 2, 3],
        "hints": [
            {"order": 1, "text": "Necesitas dos conjuntos de variables: xt (compras en período t) e It (inventario al cierre del período t)."},
            {"order": 2, "text": "Balance de inventario: It = It-1 + xt - Dt para t=1,...,4 (con I0=50)."},
        ],
        "reference_solution": {
            "variables": "xt = licencias compradas en el trimestre t (t=1,...,4)\nIt = licencias en inventario al cierre del trimestre t",
            "objective": "Min Z = 10(x1+x2+x3+x4) + 2(I1+I2+I3+I4)",
            "constraints": "I0 = 50  (inventario inicial)\nIt = It-1 + xt - Dt  para todo t  (balance de inventario)\n0 <= xt <= 200  para todo t  (capacidad de compra por trimestre)\nI4 >= 30  (stock mínimo al finalizar el año)\nIt >= 0  para todo t",
        },
    },
    # ── MIP MEDIUM ─────────────────────────────────────────────────────────────
    {
        "title": "Asignación de trabajos a servidores con costo fijo de activación – DevOps Cloud",
        "description": (
            "DevOps Cloud ejecuta tres tipos de trabajos de procesamiento por lotes: "
            "J1 (compilación de código), J2 (pruebas de integración) y J3 (análisis de logs). "
            "Estos trabajos se ejecutan en dos servidores virtuales (S1 y S2).\n\n"
            "Para que un servidor pueda procesar cualquier trabajo, debe activarse previamente, "
            "lo que incurre en un costo fijo de arranque: $500 para S1 y $800 para S2. "
            "Una vez activo, cada servidor dispone de 100 horas de procesamiento por turno. "
            "Si un servidor no se activa, no puede procesar ningún trabajo.\n\n"
            "Las horas requeridas por unidad de trabajo en cada servidor y la utilidad neta "
            "por unidad procesada se muestran en la tabla.\n\n"
            "Formule el MIP que determina cuántas unidades de cada tipo de trabajo procesar "
            "(xj >= 0) y qué servidores activar (yk en {0,1}), para maximizar la utilidad "
            "neta total (ingresos de trabajos menos costos fijos de activación)."
        ),
        "data_table": {
            "headers": ["", "J1 (compilación)", "J2 (pruebas)", "J3 (logs)", "Cap. disponible"],
            "rows": [
                ["Horas en S1 (hr/unidad)", "2", "3", "1", "100 hr/turno"],
                ["Horas en S2 (hr/unidad)", "1", "2", "4", "100 hr/turno"],
                ["Utilidad neta ($/unidad)", "15", "20", "12", ""],
            ],
        },
        "domain": "production", "type": "MIP", "difficulty": "medium", "ra_ids": [1, 2, 4, 5],
        "hints": [
            {"order": 1, "text": "Necesitas variables binarias yk = 1 si el servidor k es activado, 0 si no."},
            {"order": 2, "text": "Restricción de enlace (big-M): la carga total en el servidor k debe ser <= 100·yk. Si yk=0, no puede haber producción."},
        ],
        "reference_solution": {
            "variables": "xj = unidades del trabajo j procesadas por turno (j=1,2,3),  xj >= 0\nyk = 1 si el servidor k es activado, 0 si no (k=1,2),  yk en {0,1}",
            "objective": "Max Z = 15x1 + 20x2 + 12x3 - 500y1 - 800y2",
            "constraints": "2x1 + 3x2 + x3 <= 100·y1  (capacidad S1, activo solo si y1=1)\nx1 + 2x2 + 4x3 <= 100·y2  (capacidad S2, activo solo si y2=1)\nxj >= 0  para todo j\nyk en {0,1}  para todo k",
        },
    },
    # ── MIP HARD ───────────────────────────────────────────────────────────────
    {
        "title": "Localización de servidores edge para plataforma de streaming – StreamLite",
        "description": (
            "StreamLite debe atender la demanda de ancho de banda de tres zonas de usuarios: "
            "Zona Norte (45 Gbps/mes), Zona Central (35 Gbps/mes) y Zona Sur (30 Gbps/mes). "
            "Para ello, evalúa instalar servidores edge (SE) en tres ubicaciones candidatas: "
            "Antofagasta (SE1), Valparaíso (SE2) y Concepción (SE3).\n\n"
            "Instalar un servidor edge en cada ubicación tiene un costo fijo mensual. "
            "Si se instala un SE, puede transmitir hasta su capacidad máxima. Cada zona debe "
            "recibir exactamente su demanda de ancho de banda (no puede quedar sin servicio). "
            "Los costos de transmisión por Gbps desde cada ubicación hacia cada zona se "
            "muestran en la tabla.\n\n"
            "Formule el MIP que minimiza el costo total mensual (costos fijos de instalación "
            "más costos de transmisión), definiendo variables continuas xij [Gbps] y "
            "variables binarias yi = 1 si se instala el SE en la ubicación i."
        ),
        "data_table": {
            "headers": ["Servidor Edge", "Costo fijo (M$/mes)", "Cap. máx. (Gbps/mes)", "Costo Z.Norte ($/Gbps)", "Costo Z.Central ($/Gbps)", "Costo Z.Sur ($/Gbps)"],
            "rows": [
                ["Antofagasta (SE1)", "2,5", "80", "120", "200", "150"],
                ["Valparaíso (SE2)", "1,8", "60", "180", "130", "90"],
                ["Concepción (SE3)", "2,1", "70", "160", "110", "200"],
            ],
        },
        "domain": "logistics", "type": "MIP", "difficulty": "hard", "ra_ids": [4, 5],
        "hints": [
            {"order": 1, "text": "Variables: xij = Gbps enviados del SE i a la zona j (continua >= 0); yi = 1 si se instala el SE i (binaria)."},
            {"order": 2, "text": "Restricción de capacidad con enlace: Sum_j xij <= Capi·yi para cada SE i. Si yi=0, no puede transmitir."},
            {"order": 3, "text": "Restricción de demanda completa: Sum_i xij = dj para cada zona j (igualdad estricta)."},
        ],
        "reference_solution": {
            "variables": "xij = Gbps enviados del servidor edge i a la zona j  (i en {1,2,3}, j en {N,C,S}),  xij >= 0\nyi = 1 si se instala el SE en la ubicación i, 0 si no,  yi en {0,1}",
            "objective": "Min Z = 2.500.000·y1 + 1.800.000·y2 + 2.100.000·y3 + Sum_ij cij·xij",
            "constraints": "Sum_i xij = dj  para todo j  (demanda completa de cada zona)\nSum_j xij <= Capi·yi  para todo i  (capacidad + enlace con instalación)\nxij >= 0, yi en {0,1}",
        },
    },
    {
        "title": "Selección de módulos de software con restricciones de compatibilidad – Nuacom",
        "description": (
            "Nuacom está evaluando desarrollar 5 módulos de software para su plataforma SaaS: "
            "M1 (Autenticación OAuth), M2 (SSO Gateway), M3 (Motor de Analítica), "
            "M4 (Pipeline de Datos) y M5 (Hub de Integración). "
            "El VPN esperado y el costo de desarrollo de cada módulo se muestran en la tabla. "
            "El presupuesto total disponible para desarrollo es $10M.\n\n"
            "Las siguientes restricciones técnicas aplican:\n"
            "(1) M1 y M2 son incompatibles: si se desarrolla M1, NO puede desarrollarse M2 "
            "(y viceversa), pues ambos resuelven el mismo problema de autenticación con "
            "arquitecturas distintas.\n"
            "(2) Si se desarrollan M3 y M4 simultáneamente, es obligatorio desarrollar también "
            "M5, ya que el Hub de Integración es la capa de conexión necesaria entre ambos.\n"
            "(3) El portafolio debe incluir entre 2 y 4 módulos "
            "(restricción de capacidad del equipo y foco estratégico).\n\n"
            "Defina yj = 1 si se selecciona el módulo j, 0 si no (j=1,...,5), y formule el "
            "MIP que maximiza el VPN total del portafolio de desarrollo."
        ),
        "data_table": {
            "headers": ["Módulo", "Descripción", "VPN esperado (M$)", "Costo de desarrollo (M$)"],
            "rows": [
                ["M1", "Autenticación OAuth", "4,5", "3"],
                ["M2", "SSO Gateway", "3,2", "2"],
                ["M3", "Motor de Analítica", "5,1", "4"],
                ["M4", "Pipeline de Datos", "2,8", "2"],
                ["M5", "Hub de Integración", "1,9", "1"],
            ],
        },
        "domain": "finance", "type": "MIP", "difficulty": "hard", "ra_ids": [4, 5],
        "hints": [
            {"order": 1, "text": "Define yj = 1 si se selecciona el módulo j, 0 si no (binaria)."},
            {"order": 2, "text": "Incompatibilidad M1-M2: y1 + y2 <= 1."},
            {"order": 3, "text": "M3 y M4 implican M5: y3 + y4 - 1 <= y5 (si y3=y4=1, entonces y5 >= 1)."},
        ],
        "reference_solution": {
            "variables": "yj = 1 si se selecciona el módulo j, 0 si no (j=1,...,5),  yj en {0,1}",
            "objective": "Max Z = 4,5y1 + 3,2y2 + 5,1y3 + 2,8y4 + 1,9y5",
            "constraints": "3y1 + 2y2 + 4y3 + 2y4 + y5 <= 10  (presupuesto)\ny1 + y2 <= 1  (incompatibilidad M1-M2)\ny3 + y4 - 1 <= y5  (M3 y M4 implican M5)\n2 <= Sum_j yj <= 4  (rango de módulos a desarrollar)\nyj en {0,1}  para todo j",
        },
    },
    {
        "title": "Red de distribución CDN de tres niveles – ContentEdge",
        "description": (
            "ContentEdge opera una red de distribución de contenido (CDN) con tres eslabones: "
            "I servidores de origen (SO), J nodos de caché intermedios (NC) y K puntos de "
            "entrega final (PE). El precio de entrega al usuario es P [$/GB]. Los costos de "
            "transferencia son aij [$/GB] del servidor de origen i al nodo de caché j, "
            "y bjk [$/GB] del nodo de caché j al punto de entrega k.\n\n"
            "La capacidad mensual de cada nodo de caché es cj [GB/mes]. La demanda mínima "
            "de contenido de cada punto de entrega es dk [GB/mes]. La disponibilidad mensual "
            "de cada servidor de origen es ei [GB/mes].\n\n"
            "Formule el modelo paramétrico de programación lineal que maximiza el beneficio "
            "neto total de la red CDN, definiendo variables de flujo en cada eslabón e "
            "incluyendo las restricciones de balance de flujo en los nodos de caché "
            "(lo que entra al nodo j debe igualar lo que sale)."
        ),
        "data_table": None,
        "domain": "logistics", "type": "LP", "difficulty": "hard", "ra_ids": [1, 2, 3],
        "hints": [
            {"order": 1, "text": "Necesitas dos conjuntos de variables de flujo: xij (SO->NC) e yjk (NC->PE)."},
            {"order": 2, "text": "Balance de flujo en cada nodo j: Sum_i xij = Sum_k yjk (lo que entra = lo que sale)."},
        ],
        "reference_solution": {
            "variables": "xij = GB transferidos del servidor de origen i al nodo de caché j  [GB/mes]\nyjk = GB transferidos del nodo de caché j al punto de entrega k  [GB/mes]",
            "objective": "Max Z = P·Sum_jk yjk - Sum_ij aij·xij - Sum_jk bjk·yjk",
            "constraints": "Sum_j xij <= ei  para todo i  (disponibilidad de origen i)\nSum_k yjk >= dk  para todo k  (demanda mínima del PE k)\nSum_i xij <= cj  para todo j  (capacidad del NC j)\nSum_i xij = Sum_k yjk  para todo j  (balance de flujo en NC j)\nxij, yjk >= 0",
        },
    },
    {
        "title": "Asignación de cargas de procesamiento a clústeres HPC – JobCloud",
        "description": (
            "JobCloud ejecuta trabajos de cómputo de alto rendimiento (HPC) para 5 clientes "
            "corporativos (CL1 a CL5). Cada cliente tiene un requerimiento fijo de GPU-horas "
            "por mes: Q1, Q2, Q3, Q4 y Q5. JobCloud dispone de tres clústeres HPC (C1, C2, C3) "
            "con disponibilidades de 5.000, 7.000 y 4.000 GPU-horas respectivamente.\n\n"
            "Política de aislamiento de datos: por contrato de confidencialidad, cada cliente "
            "debe recibir TODA su carga de procesamiento de UN ÚNICO clúster "
            "(no se permite dividir los trabajos entre clústeres). "
            "El beneficio neto por GPU-hora asignada del clúster i al cliente j es Bij.\n\n"
            "Formule el MIP paramétrico que maximiza el beneficio total neto, definiendo "
            "variables continuas xij (GPU-horas asignadas del clúster i al cliente j) y "
            "variables binarias zij = 1 si el cliente j es atendido por el clúster i."
        ),
        "data_table": None,
        "domain": "logistics", "type": "MIP", "difficulty": "hard", "ra_ids": [4, 5],
        "hints": [
            {"order": 1, "text": "La variable binaria zij = 1 indica que el cliente j recibe TODA su carga del clúster i."},
            {"order": 2, "text": "Todo-o-nada: xij = Qj·zij (si zij=1, el cliente j recibe Qj GPU-horas del clúster i; si no, recibe cero)."},
            {"order": 3, "text": "Cada cliente puede ser atendido por a lo más un clúster: Sum_i zij <= 1 para cada j."},
        ],
        "reference_solution": {
            "variables": "xij = GPU-horas asignadas del clúster i al cliente j\nzij = 1 si el cliente j es atendido por el clúster i, 0 si no",
            "objective": "Max Z = Sum_i Sum_j Bij·xij",
            "constraints": "Sum_j xij <= Si  para todo i  (disponibilidad: S1=5.000, S2=7.000, S3=4.000 GPU-hr)\nxij = Qj·zij  para todo i,j  (todo-o-nada: asignación completa o cero)\nSum_i zij <= 1  para todo j  (un cliente es atendido por a lo más un clúster)\nxij >= 0, zij en {0,1}",
        },
    },
    {
        "title": "Expansión de capacidad en data centers – CloudExpand",
        "description": (
            "CloudExpand opera tres data centers (DC1: Iquique, DC2: San Antonio, "
            "DC3: Puerto Montt) cuyas capacidades actuales de almacenamiento y cómputo "
            "en rack-units se muestran en la tabla. La demanda proyectada para el próximo "
            "año aumentará en un 20% respecto a la demanda actual asignada a cada DC.\n\n"
            "Para satisfacer esta mayor demanda, cada data center puede expandir su capacidad. "
            "Expandir un DC implica un costo fijo de inversión en infraestructura "
            "(construcción, equipamiento base) y un costo variable por rack-unit adicional "
            "habilitado. Si un DC no se expande, no incurre en costo fijo ni variable. "
            "El ingreso neto por rack-unit operativo es $10.000/año.\n\n"
            "Formule el MIP que determina qué data centers expandir (yi en {0,1}) y cuánta "
            "capacidad adicional habilitar (ui rack-units >= 0) para maximizar el beneficio "
            "neto total (ingresos por rack-units operativos menos costos de expansión)."
        ),
        "data_table": {
            "headers": ["Data Center", "Cap. actual (ru)", "Costo fijo expansión ($M)", "Costo variable ($/ru)", "Demanda actual (ru)"],
            "rows": [
                ["DC1 – Iquique", "5.000", "1.000", "1.000", "4.000"],
                ["DC2 – San Antonio", "8.000", "1.800", "3.000", "7.000"],
                ["DC3 – Puerto Montt", "6.000", "1.000", "1.800", "5.500"],
            ],
        },
        "domain": "logistics", "type": "MIP", "difficulty": "hard", "ra_ids": [4, 5],
        "hints": [
            {"order": 1, "text": "Define yi = 1 si se expande el DC i (binaria) y ui = rack-units adicionales habilitados (continua >= 0)."},
            {"order": 2, "text": "Restricción de enlace: ui <= M·yi (solo se puede habilitar capacidad adicional si se invierte en la expansión)."},
        ],
        "reference_solution": {
            "variables": "xi = rack-units operativos en el DC i tras la expansión\nui = rack-units adicionales habilitados en DC i,  ui >= 0\nyi = 1 si se expande el DC i, 0 si no,  yi en {0,1}",
            "objective": "Max Z = 10.000·Sum_i xi - Sum_i(Fi·yi + Vi·ui)",
            "constraints": "xi <= Capi + ui  para todo i  (capacidad disponible tras expansión)\nui <= M·yi  para todo i  (expansión solo si se invierte)\nxi = 1,2·Di  para todo i  (satisfacer demanda proyectada: +20%)\nui >= 0, yi en {0,1}",
        },
    },
    # ── NLP MEDIUM ─────────────────────────────────────────────────────────────
    {
        "title": "Minimización de desviaciones respecto a metas de SLA – CloudAPI",
        "description": (
            "CloudAPI gestiona tres servicios en la nube con metas de disponibilidad mensual "
            "expresadas en número de instancias activas: "
            "meta1=100 instancias (API REST), meta2=150 instancias (WebSocket), "
            "meta3=80 instancias (gRPC).\n\n"
            "El número real de instancias asignadas a cada servicio (xi) puede diferir de la "
            "meta, tanto por exceso (sobreaprovisionamiento) como por déficit (incumplimiento "
            "de SLA). En ambos casos, el costo de desviación es $5 por unidad de desvío. "
            "La capacidad total del clúster permite asignar como máximo 320 instancias en total.\n\n"
            "Formule el modelo de optimización que minimiza el costo total de desviación "
            "respecto a las metas de SLA. Introduzca las variables auxiliares necesarias para "
            "tratar el valor absoluto, e identifique el tipo de modelo resultante "
            "(LP, MIP o NLP) justificando la respuesta."
        ),
        "data_table": None,
        "domain": "production", "type": "NLP", "difficulty": "medium", "ra_ids": [1, 2, 3, 5],
        "hints": [
            {"order": 1, "text": "La desviación |xi - metai| no es diferenciable. Linealízala con variables auxiliares di+ (exceso) y di- (déficit)."},
            {"order": 2, "text": "Define: xi - metai = di+ - di-, con di+, di- >= 0. Entonces |xi - metai| = di+ + di-."},
        ],
        "reference_solution": {
            "variables": "xi = instancias asignadas al servicio i (i=1,2,3)\ndi+ = instancias sobre la meta del servicio i (exceso)\ndi- = instancias bajo la meta del servicio i (déficit)",
            "objective": "Min Z = 5·Sum_i(di+ + di-)",
            "constraints": "xi - metai = di+ - di-  para todo i  (definición de desviación)\nx1 + x2 + x3 <= 320  (capacidad total del clúster)\ndi+, di- >= 0;  xi >= 0  para todo i\nTipo: LP (la linealización del valor absoluto convierte el modelo en un LP)",
        },
    },
    # ── NLP HARD ───────────────────────────────────────────────────────────────
    {
        "title": "Despacho óptimo de carga en servidores heterogéneos – DataCentro",
        "description": (
            "DataCentro opera tres servidores heterogéneos (Srv1, Srv2, Srv3) para procesar "
            "una carga total de trabajos de cómputo. El costo de operación de cada servidor "
            "crece cuadráticamente con la carga asignada Pi [jobs/hr]:\n"
            "  C1(P1) = 0,002·P1^2 + 2·P1 + 10  [$/hr]\n"
            "  C2(P2) = 0,003·P2^2 + 1,5·P2 + 8  [$/hr]\n"
            "  C3(P3) = 0,001·P3^2 + 3·P3 + 12  [$/hr]\n\n"
            "La demanda total del sistema es de 400 jobs/hr y debe ser atendida en su "
            "totalidad (igualdad estricta, sin pérdida de trabajos). Cada servidor tiene "
            "límites de carga operativa seguros: Srv1 entre 50 y 200 jobs/hr; "
            "Srv2 entre 30 y 150 jobs/hr; Srv3 entre 80 y 300 jobs/hr.\n\n"
            "Los coeficientes de las funciones de costo se detallan en la tabla. "
            "Formule el modelo que minimiza el costo total de operación e identifique "
            "el tipo de modelo, justificando por qué es NLP."
        ),
        "data_table": {
            "headers": ["Servidor", "a ($/job^2·hr)", "b ($/job·hr)", "c ($/hr)", "Pmin (jobs/hr)", "Pmax (jobs/hr)"],
            "rows": [
                ["Srv1", "0,002", "2", "10", "50", "200"],
                ["Srv2", "0,003", "1,5", "8", "30", "150"],
                ["Srv3", "0,001", "3", "12", "80", "300"],
            ],
        },
        "domain": "energy", "type": "NLP", "difficulty": "hard", "ra_ids": [1, 2, 3, 5],
        "hints": [
            {"order": 1, "text": "Las funciones de costo son cuadráticas en Pi => la función objetivo total es no lineal (NLP)."},
            {"order": 2, "text": "La restricción de balance de carga es de igualdad estricta: P1 + P2 + P3 = 400 (toda la demanda debe ser procesada)."},
        ],
        "reference_solution": {
            "variables": "Pi = carga asignada al servidor i [jobs/hr]  (i=1,2,3)",
            "objective": "Min Z = 0,002P1^2 + 2P1 + 10 + 0,003P2^2 + 1,5P2 + 8 + 0,001P3^2 + 3P3 + 12",
            "constraints": "P1 + P2 + P3 = 400  (balance total de carga, igualdad estricta)\n50 <= P1 <= 200  (límites operativos Srv1)\n30 <= P2 <= 150  (límites operativos Srv2)\n80 <= P3 <= 300  (límites operativos Srv3)\nTipo: NLP convexo (objetivo cuadrático convexo, restricciones lineales)",
        },
    },
    {
        "title": "Minimización de varianza en asignación de ancho de banda – BandwidthOpt",
        "description": (
            "Un sistema de gestión de redes debe distribuir un presupuesto normalizado de "
            "ancho de banda entre tres servicios críticos (x1, x2, x3), de forma que la "
            "asignación total sea exactamente 1 unidad (es decir, el 100% del ancho de banda "
            "disponible se distribuye entre los tres servicios, con xi >= 0).\n\n"
            "Para garantizar equidad y estabilidad en el sistema, se desea minimizar la "
            "variabilidad de la asignación. Esto equivale a minimizar la norma euclídea al "
            "cuadrado del vector de asignación: ||x||^2 = x1^2 + x2^2 + x3^2.\n\n"
            "Formule el modelo de optimización no lineal (NLP) e identifique sus propiedades "
            "estructurales: tipo de función objetivo, tipo de restricciones y convexidad del problema."
        ),
        "data_table": None,
        "domain": "generic", "type": "NLP", "difficulty": "hard", "ra_ids": [1, 2, 5],
        "hints": [
            {"order": 1, "text": "La norma euclídea al cuadrado ||x||^2 = x1^2 + x2^2 + x3^2 es una función cuadrática convexa."},
            {"order": 2, "text": "El problema tiene una restricción de igualdad (presupuesto) y restricciones de no negatividad (todas lineales)."},
        ],
        "reference_solution": {
            "variables": "xi = fracción de ancho de banda asignada al servicio i (i=1,2,3),  xi >= 0",
            "objective": "Min Z = x1^2 + x2^2 + x3^2  (norma euclídea al cuadrado)",
            "constraints": "x1 + x2 + x3 = 1  (presupuesto normalizado de ancho de banda)\nx1, x2, x3 >= 0\nTipo: NLP convexo (objetivo cuadrático convexo, restricciones lineales de igualdad y no negatividad)",
        },
    },
    # ── MIP HARD – MODELO INDEXADO COMPLETO ────────────────────────────────────
    {
        "title": "Producción multi-datacenter multi-período de servicios cloud – TechServe",
        "description": (
            "TechServe planifica el aprovisionamiento de tres tipos de servicios gestionados "
            "— Compute (C), Storage (S) y Network (N) — en dos data centers: DC1 (Santiago) "
            "y DC2 (Antofagasta). La planificación abarca 3 períodos mensuales "
            "(t=1: Enero, t=2: Febrero, t=3: Marzo).\n\n"
            "Índices y conjuntos:\n"
            "  I = {1,2}: data centers (i=1: DC1-Santiago, i=2: DC2-Antofagasta)\n"
            "  J = {C,S,N}: servicios (Compute, Storage, Network)\n"
            "  T = {1,2,3}: períodos mensuales\n\n"
            "Parámetros del modelo:\n"
            "  cij [$/u]: costo de aprovisionar el servicio j en el data center i\n"
            "  rij [GPU-hr/u]: GPU-horas requeridas por unidad del servicio j en el DC i\n"
            "  Capi [GPU-hr/mes]: capacidad máxima de GPU-horas del DC i por período "
            "(Cap1=120, Cap2=100)\n"
            "  fi [$/mes]: costo fijo de operación del DC i si está activo ese período "
            "(f1=200, f2=150)\n"
            "  hj [$/u/mes]: costo de mantener en inventario una unidad del servicio j\n"
            "  djt [u]: demanda del servicio j en el período t (debe satisfacerse exactamente)\n"
            "  Ij0 = 0: inventario inicial de cada servicio (cero para todo j)\n\n"
            "Decisión de operación: si el DC i no opera en el período t, no puede aprovisionar "
            "ninguna unidad ese mes. Operar tiene un costo fijo fi independiente del volumen.\n\n"
            "Balance de inventario: Ij,t-1 + Sum_i xijt - Ijt = djt para todo j en J, t en T, "
            "con Ij0=0.\n\n"
            "Los valores numéricos de cij, rij, hj y djt se encuentran en la tabla adjunta.\n\n"
            "Se pide: Formule el MIP que minimiza el costo total (aprovisionamiento + inventario "
            "+ operación de DCs), definiendo explícitamente:\n"
            "  1. Conjuntos de índices\n"
            "  2. Parámetros (notación indexada y unidades)\n"
            "  3. Variables de decisión (continuas y binarias, con dominio y cuantificador para todo)\n"
            "  4. Función objetivo en notación de sumatoria (Sum) sobre los conjuntos definidos\n"
            "  5. Restricciones, indicando para todo i en I, para todo j en J, para todo t en T"
        ),
        "data_table": {
            "headers": ["Parámetro", "Compute (C)", "Storage (S)", "Network (N)"],
            "rows": [
                ["DC1 – Costo aprov. ($/u)", "8", "12", "10"],
                ["DC2 – Costo aprov. ($/u)", "10", "9", "11"],
                ["DC1 – GPU-hr requeridas (hr/u)", "2", "3", "1"],
                ["DC2 – GPU-hr requeridas (hr/u)", "1", "2", "3"],
                ["Costo inventario ($/u/mes)", "1", "2", "1,5"],
                ["Demanda Enero (unid.)", "20", "15", "25"],
                ["Demanda Febrero (unid.)", "30", "20", "25"],
                ["Demanda Marzo (unid.)", "25", "18", "30"],
            ],
        },
        "domain": "production", "type": "MIP", "difficulty": "hard", "ra_ids": [1, 2, 3, 4, 5],
        "hints": [
            {"order": 1, "text": "Define 3 conjuntos de índices: I={1,2} para DCs, J={C,S,N} para servicios, T={1,2,3} para meses. La variable de aprovisionamiento es tridimensional: xijt."},
            {"order": 2, "text": "Restricción de capacidad con enlace: Sum_j rij·xijt <= Capi·yit para todo i en I, t en T. Si yit=0, el DC no puede aprovisionar (Capi actúa como big-M)."},
            {"order": 3, "text": "Balance de inventario: Ij,t-1 + Sum_i xijt - Ijt = djt para todo j en J, t en T, con Ij0=0."},
        ],
        "reference_solution": {
            "variables": (
                "Conjuntos:\n"
                "I = {1,2}: data centers (DC1-Santiago, DC2-Antofagasta)\n"
                "J = {C,S,N}: servicios (Compute, Storage, Network)\n"
                "T = {1,2,3}: períodos (Enero, Febrero, Marzo)\n\n"
                "Parámetros:\n"
                "cij: costo de aprovisionar 1 unidad del servicio j en DC i ($/u)\n"
                "rij: GPU-horas por unidad del servicio j en DC i (GPU-hr/u)\n"
                "Capi: capacidad en GPU-horas del DC i por período\n"
                "djt: demanda del servicio j en período t (unidades)\n"
                "hj: costo de inventario del servicio j ($/u/mes)\n"
                "fi: costo fijo de operación del DC i por período ($)\n\n"
                "Variables de decisión:\n"
                "xijt >= 0: unidades del servicio j aprovisionadas en DC i en período t  para todo i en I, j en J, t en T\n"
                "Ijt >= 0: inventario del servicio j al final del período t  para todo j en J, t en T\n"
                "yit en {0,1}: 1 si DC i opera en período t, 0 si no  para todo i en I, t en T"
            ),
            "objective": "Min Z = Sum_i Sum_j Sum_t cij·xijt  +  Sum_j Sum_t hj·Ijt  +  Sum_i Sum_t fi·yit",
            "constraints": (
                "Sum_j rij·xijt <= Capi·yit   para todo i en I, t en T  (capacidad GPU-hr y enlace con operación)\n"
                "Ij,t-1 + Sum_i xijt - Ijt = djt   para todo j en J, t en T  (balance de inventario, Ij0=0)\n"
                "xijt >= 0   para todo i en I, j en J, t en T\n"
                "Ijt >= 0   para todo j en J, t en T\n"
                "yit en {0,1}   para todo i en I, t en T\n"
                "Modelo: MIP (variables continuas + binarias, restricciones lineales)"
            ),
        },
    },
]


def seed_exercises(db: Session, teacher_id) -> None:
    # Elimina todos los ejercicios sembrados manualmente antes de re-insertar,
    # para que los cambios de enunciado y contexto queden reflejados en la BD.
    db.query(Exercise).filter(Exercise.ai_generated == False).delete()
    db.commit()

    for ex_data in EXERCISES:
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
    print(f"✓ {len(EXERCISES)} ejercicios sembrados en contexto tech")
