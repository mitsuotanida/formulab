# FormuLab — Guía de Inicio Rápido

## Prerrequisitos
- Python 3.12+
- Node.js 20+
- PostgreSQL (local o Railway)
- API key de Anthropic

---

## 1. BACKEND — Configuración local

```bash
cd formulab-backend

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env (copiar y completar)
copy .env.example .env
```

Editar `.env`:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/formulab
ANTHROPIC_API_KEY=sk-ant-...        ← tu clave API de Anthropic
SECRET_KEY=<64 chars hex random>
REFRESH_SECRET_KEY=<64 chars hex random>
CORS_ORIGINS=http://localhost:3000
```

Generar claves secretas:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

```bash
# Crear base de datos
createdb formulab          # o desde pgAdmin

# Ejecutar migraciones
alembic upgrade head

# Cargar datos iniciales (15 ejercicios + badges + cuenta profesor)
python seeds/run_seeds.py

# Iniciar servidor
uvicorn app.main:app --reload
```

Backend disponible en: http://localhost:8000
Documentación API: http://localhost:8000/api/docs

---

## 2. FRONTEND — Configuración local

```bash
cd formulab-frontend

# Instalar dependencias
npm install

# Crear archivo de entorno
copy .env.local.example .env.local
```

`.env.local` ya tiene:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

```bash
# Iniciar servidor de desarrollo
npm run dev
```

Frontend disponible en: http://localhost:3000

---

## 3. Credenciales iniciales

| Campo    | Valor                    |
|----------|--------------------------|
| Email    | mtanidab@gmail.com       |
| Password | FormuLab2026!            |
| Rol      | teacher (profesor)       |

> **Importante:** Cambia la contraseña al primer ingreso desde tu perfil.

---

## 4. Despliegue en Railway

1. Crear cuenta en [railway.app](https://railway.app)
2. Crear nuevo proyecto → "New Project"
3. Agregar **PostgreSQL** como plugin
4. Crear servicio `formulab-backend`:
   - Conectar repositorio o subir directorio `formulab-backend/`
   - Variables de entorno a configurar:
     ```
     DATABASE_URL        ← auto-inyectado desde plugin PostgreSQL
     ANTHROPIC_API_KEY   ← tu clave
     SECRET_KEY          ← 64 chars hex
     REFRESH_SECRET_KEY  ← 64 chars hex
     CORS_ORIGINS        ← https://tu-frontend.up.railway.app
     ```
5. Crear servicio `formulab-frontend`:
   - Conectar directorio `formulab-frontend/`
   - Variables de entorno:
     ```
     NEXT_PUBLIC_API_URL ← https://tu-backend.up.railway.app/api/v1
     ```
6. El `railway.toml` del backend ejecuta automáticamente las migraciones y el seed.

Costo estimado: ~$10-15 USD/mes (plan Hobby).

---

## 5. Estructura del proyecto

```
05_FORMULAB/
├── formulab-backend/       ← FastAPI + PostgreSQL + Claude AI
│   ├── app/               ← Código principal
│   ├── alembic/           ← Migraciones DB
│   └── seeds/             ← Datos iniciales (15 ejercicios + badges)
├── formulab-frontend/      ← Next.js 14 + Tailwind (dark mode)
│   └── app/               ← Páginas de la aplicación
└── INICIO_RAPIDO.md        ← Este archivo
```

---

## 6. Funcionalidades principales

| Función | Descripción |
|---------|-------------|
| **Login/Registro** | Cuentas de estudiante y profesor |
| **Ejercicios** | 15 ejercicios base + generación ilimitada con IA |
| **Formulación** | Editor de texto con notación matemática |
| **Evaluación IA** | Claude evalúa variables, FO y restricciones (0-100 pts) |
| **Gamificación** | XP, 6 niveles (Intern→Principal), 11 badges, streaks |
| **Leaderboard** | Ranking semanal y total |
| **Panel admin** | Heatmap de RAs, exportar CSV, generar ejercicios con IA |
| **Export** | CSV con progreso de todos los estudiantes |
