# 📊 ENERGY PROCESS - Diagramas Técnicos y Visuales

---

## 1. DIAGRAMA DE ARQUITECTURA COMPLETA

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              🌍 INTERNET                                     │
└────────────────────────────────┬────────────────────────────────────┬────────┘
                                 │                                    │
                    ┌────────────▼────────────┐      ┌──────────────▼──────┐
                    │   NGINX (Proxy Rev.)    │      │   CDN/Static Files  │
                    │ - SSL/TLS Termination   │      │ - Frontend compiled │
                    │ - Rate Limiting         │      │ - Cache strategy    │
                    └────────────┬────────────┘      └─────────────────────┘
                                 │
        ┌────────────────────────┴─────────────────────────┐
        │                                                  │
        ▼                                                  ▼
┌───────────────────────┐                      ┌──────────────────────┐
│  FRONTEND (Vite React)│                      │ BACKEND (FastAPI)    │
│ - React 18.2         │◄────── HTTP/REST ────│ - Python 3.9+        │
│ - Vite 5.0           │       (JSON)         │ - Uvicorn Server     │
│ - Axios 1.6          │                      │ - Port 8000          │
│ - Pages (6)          │                      │ - Auto-Docs Swagger  │
│ - Components (5)     │                      │ - CORS Enabled       │
│ - Port 3000/5173     │                      └──────────┬───────────┘
└───────────────────────┘                                 │
                                      ┌──────────────────┼──────────────────┐
                                      │                  │                  │
                              ┌───────▼───────┐  ┌───────▼────────┐  ┌─────▼──────┐
                              │  SQLAlchemy   │  │  Pydantic      │  │ Celery/    │
                              │  ORM Layer    │  │  Validation    │  │ Tasks      │
                              │  - Models     │  │  - Schemas     │  │            │
                              │  - Queries    │  │  - Type Check  │  └─────┬──────┘
                              └───────┬───────┘  └────────────────┘        │
                                      │                                    │
        ┌─────────────────────────────┴──────┬─────────────────┬──────────┘
        │                                    │                 │
        ▼                                    ▼                 ▼
    ┌─────────────────┐        ┌──────────────────┐    ┌──────────────┐
    │  PostgreSQL 15  │        │   Redis 7        │    │ Celery       │
    │ - Main Database │        │ - Broker Messages│    │ - Worker1    │
    │ - ACID Safe     │        │ - Cache Layer    │    │ - Worker2    │
    │ - Backup Ready  │        │ - Session Store  │    │ - Worker3    │
    │ - 5 Tables      │        │ - Real-time      │    │ (Scalable)   │
    │ - Indexes       │        │   Notifications  │    │ - Process    │
    │ - Constraints   │        └──────────────────┘    │   Async      │
    └─────────────────┘                                 └──────────────┘
```

---

## 2. FLUJO DE DATOS: Upload a Resultado Final

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ USUARIO                                                                      │
│ Abre navegador → http://localhost:3000 → Navega a "CARGA"                  │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ FRONTEND - Carga.jsx    │
                    │ - FileUpload component  │
                    │ - Drag & Drop ready     │
                    └────────────┬────────────┘
                                 │
                                 │ Usuario selecciona archivo
                                 ▼
                    ┌────────────────────────┐
                    │ Lectura archivo local  │
                    │ file.read() JavaScript │
                    │ Size < 100MB check     │
                    └────────────┬───────────┘
                                 │
                                 │ FormData + Axios
                                 ▼
                    ┌────────────────────────────────────┐
                    │ POST /api/v1/archivos/upload       │
                    │ Content-Type: multipart/form-data  │
                    │ Body: {file: <FILE_BINARY>}        │
                    └────────────┬───────────────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────────────────────┐
        │ 🔧 BACKEND - archivos.py (POST /upload handler)           │
        │                                                             │
        │ 1. await file.read()                                       │
        │    └─► contenido = bytes                                   │
        │                                                             │
        │ 2. hashlib.sha256(contenido).hexdigest()                  │
        │    └─► hash_archivo = "abc123def..."                       │
        │                                                             │
        │ 3. db.query(ArchivoProcesado)                             │
        │    .filter(hash_archivo == ...)                            │
        │    └─► if existe: ❌ Error 400 "Duplicado"                │
        │                                                             │
        │ 4. Path(settings.UPLOAD_DIR).mkdir()                       │
        │    ruta = "./uploads/" + filename                          │
        │    ruta.write_bytes(contenido)                             │
        │    └─► ✅ Archivo guardado en disco                        │
        │                                                             │
        │ 5. new_archivo = ArchivoProcesado(                         │
        │      usuario_id=1,                                         │
        │      nombre_archivo="peajes.csv",                          │
        │      hash_archivo="abc123def...",                          │
        │      estado="pendiente",                                   │
        │      ruta_archivo="/uploads/peajes.csv"                    │
        │    )                                                        │
        │    db.add(new_archivo)                                     │
        │    db.commit()  ◄─ INSERT en PostgreSQL                    │
        │    └─► ✅ archivo.id = 1                                   │
        │                                                             │
        │ 6. procesar_archivo_task.delay(1, "/uploads/peajes.csv")   │
        │    └─► Encola en Redis para Celery                         │
        │                                                             │
        │ 7. return 202 ACCEPTED                                      │
        │    {                                                        │
        │      "archivo_id": 1,                                       │
        │      "estado": "pendiente",                                │
        │      "mensaje": "En cola de procesamiento"                 │
        │    }                                                        │
        └────────────────────┬────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────┐
        │ 📨 FRONTEND - Recibe 202                   │
        │ - Actualiza UI: "Estado: Pendiente"        │
        │ - Inicia polling cada 2 segundos           │
        │ - GET /api/v1/archivos/1 (check status)    │
        └────────────────────┬─────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────────────────────┐
        │ ⚙️ CELERY WORKER (En proceso)                              │
        │                                                             │
        │ Obtiene tarea de Redis:                                    │
        │   archivo_id = 1                                           │
        │   ruta_archivo = "/uploads/peajes.csv"                     │
        │                                                             │
        │ Ejecuta: procesar_archivo(db, 1, "/uploads/peajes.csv")   │
        │   │                                                         │
        │   ├─► 1. UPDATE archivo SET estado='procesando'            │
        │   │                                                         │
        │   ├─► 2. open("/uploads/peajes.csv") as f                  │
        │   │       reader = csv.DictReader(f)                       │
        │   │                                                         │
        │   ├─► 3. FOR cada línea:                                   │
        │   │                                                         │
        │   │       ┌─────────────────────────────────┐              │
        │   │       │ LÍNEA 2 (Datos reales)          │              │
        │   │       │ cups_cliente: ES1234567890      │              │
        │   │       │ tipo: 12                        │              │
        │   │       │ fecha_desde: 2024-01-01         │              │
        │   │       │ fecha_hasta: 2024-01-31         │              │
        │   │       │ energia_neta_gen: [100.5, ...]  │              │
        │   │       └──────────┬──────────────────────┘              │
        │   │                  │                                      │
        │   │                  ├─► validar_linea()                   │
        │   │                  │   ├─► Validar CUPS ✓               │
        │   │                  │   ├─► Validar tipo ✓                │
        │   │                  │   ├─► Validar fechas ✓              │
        │   │                  │   ├─► Validar arrays ✓              │
        │   │                  │   └─► Retorna: [] (no errors)       │
        │   │                  │                                      │
        │   │                  ├─► insertar_energia()                │
        │   │                  │   └─► INSERT en energia_excedentaria│
        │   │                  │       ✅ exitosos += 1              │
        │   │                  │                                      │
        │   │       ┌─────────────────────────────────┐              │
        │   │       │ LÍNEA 3 (ERROR)                 │              │
        │   │       │ cups_cliente: [VACÍO]           │              │
        │   │       │ tipo: 12                        │              │
        │   │       └──────────┬──────────────────────┘              │
        │   │                  │                                      │
        │   │                  ├─► validar_linea()                   │
        │   │                  │   ├─► Validar CUPS ✗                │
        │   │                  │   └─► Retorna: [("cliente_inexiste...",)]
        │   │                  │                                      │
        │   │                  ├─► registrar_error()                 │
        │   │                  │   └─► INSERT en registro_errores    │
        │   │                  │       ❌ con_error += 1             │
        │   │                  │                                      │
        │   │       ... Más líneas ...                               │
        │   │                                                         │
        │   └─► 4. UPDATE archivo SET                                │
        │         estado='completado',                               │
        │         total_registros=150,                               │
        │         registros_exitosos=140,                            │
        │         registros_con_error=10,                            │
        │         fecha_procesamiento=NOW()                          │
        │                                                             │
        └────────────────────┬────────────────────────────────────┘
                             │
                             │ Mientras tanto, Frontend está
                             │ haciendo polling...
                             ▼
        ┌──────────────────────────────────────────┐
        │ Frontend: GET /api/v1/archivos/1         │
        │ Respuesta: {estado: "procesando", ...}   │
        │ "Procesando... (lineaX de Y)"             │
        │                                          │
        │ ... después de ~10 segundos ...          │
        │                                          │
        │ Frontend: GET /api/v1/archivos/1         │
        │ Respuesta: {estado: "completado", ...}   │
        │ ✅ "¡Procesado correctamente!"           │
        │    Exitosos: 140                         │
        │    Errores: 10                           │
        └──────────────────────┬───────────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────────┐
        │ USUARIO VE RESULTADOS                    │
        │ - Estado: Completado                     │
        │ - Resumen: 140/150 OK                    │
        │ - Botón: "Ver Errores" ← Click           │
        │                                          │
        │ GET /api/v1/errores/1 ─────────────►     │
        │ ◄───── Lista 10 errores                  │
        │                                          │
        │ - Línea 3: cliente_inexistente           │
        │ - Línea 5: tipo_no_soportado             │
        │ - ... etc                                │
        └──────────────────────────────────────────┘
```

---

## 3. ESTRUCTURA DE DIRECTORIO CON FUNCIONES

```
Energy_Process/
│
├── 🚀 RAÍZ - CONFIGURACIÓN
│   ├── docker-compose.yml          ← Orquestación contenedores (5 servicios)
│   ├── README.md                   ← README original (setup básico)
│   ├── README_COMPLETO.md          ← 📌 ESTE DOCUMENTO - Completo técnico
│   ├── GUIA_PRESENTACION.md        ← Guía ejecutiva (5-10 min)
│   ├── DIAGRAMAS_TECNICOS.md       ← Este archivo - Visuales
│   └── resq.rest                   ← Cliente REST para pruebas manuales
│
│
├── backend/                        ← 🔧 API FastAPI + Lógica
│   │
│   ├── 📋 CONFIGURACIÓN
│   │   ├── Dockerfile             ← Imagen Docker del backend
│   │   ├── Makefile               ← Comandos útiles (make run, etc)
│   │   ├── requirements.txt       ← Dependencias pip
│   │   ├── start_dev.sh          ← Script quick start
│   │   ├── alembic.ini           ← Config de migraciones
│   │   └── .env.example          ← Template variables entorno
│   │
│   ├── app/                       ← ⭐ CÓDIGO PRINCIPAL
│   │   ├── __init__.py
│   │   │
│   │   ├── 🎯 main.py            ← PUNTO DE ENTRADA FastAPI
│   │   │   └─ Configura CORS, incluye routers, corre en :8000
│   │   │
│   │   ├── 🔐 config.py          ← CONFIGURACIÓN GLOBAL
│   │   │   └─ Settings (DB_URL, REDIS_URL, UPLOAD_DIR, etc)
│   │   │
│   │   ├── 📊 database.py        ← CONEXIÓN BD
│   │   │   ├─ engine = create_engine(DATABASE_URL)
│   │   │   ├─ SessionLocal = sessionmaker()
│   │   │   └─ get_db() ← Dependencia FastAPI
│   │   │
│   │   ├── ⚡ celery_app.py      ← CONFIGURACIÓN CELERY
│   │   │   └─ app = Celery() with broker=REDIS_URL
│   │   │
│   │   ├── 📮 tasks.py           ← TAREAS ASINCRÓNICAS
│   │   │   └─ @celery_app.task procesar_archivo_task()
│   │   │      └─ Llamada por API, ejecutada por worker
│   │   │
│   │   │
│   │   ├── 🔌 api/              ← RUTAS HTTP REST
│   │   │   │
│   │   │   ├── deps.py          ← Dependencias compartidas
│   │   │   │                    (get_db, auth, etc)
│   │   │   │
│   │   │   └── routes/          ← Endpoints separados por dominio
│   │   │       │
│   │   │       ├── archivos.py  ← 📤 Upload, list, status
│   │   │       │   ├─ POST   /api/v1/archivos/upload
│   │   │       │   ├─ GET    /api/v1/archivos
│   │   │       │   └─ GET    /api/v1/archivos/{id}
│   │   │       │
│   │   │       ├── energia.py   ← 🔋 Consultas de registros
│   │   │       │   └─ GET    /api/v1/energia (filtros)
│   │   │       │
│   │   │       ├── errores.py   ← ⚠️  Consultas de errores
│   │   │       │   ├─ GET    /api/v1/errores
│   │   │       │   └─ GET    /api/v1/errores/{archivo_id}
│   │   │       │
│   │   │       ├── stats.py     ← 📈 Estadísticas
│   │   │       │   └─ GET    /api/v1/stats
│   │   │       │
│   │   │       ├── auth.py      ← 🔐 Autenticación (COMENTADO)
│   │   │       ├── usuarios.py  ← 👥 Usuarios (COMENTADO)
│   │   │       └── clientes.py  ← 🏢 Clientes (COMENTADO)
│   │   │
│   │   │
│   │   ├── 🗄️  models/          ← ORM SQLAlchemy (Tablas BD)
│   │   │   │
│   │   │   ├── archivo_procesado.py
│   │   │   │   └─ Tabla: archivo_procesado
│   │   │   │      Campos: id, usuario_id, nombre, hash, estado, etc
│   │   │   │
│   │   │   ├── energia_excedentaria.py
│   │   │   │   └─ Tabla: energia_excedentaria
│   │   │   │      Campos: id, archivo_id, cups, energia[], pago_tda[]
│   │   │   │
│   │   │   ├── registro_errores.py
│   │   │   │   └─ Tabla: registro_errores
│   │   │   │      Campos: id, archivo_id, linea, tipo_error, descripcion
│   │   │   │
│   │   │   ├── tipo_autoconsumo.py
│   │   │   │   └─ Tabla: tipo_autoconsumo
│   │   │   │      Campos: codigo {12,41,42,43,51}, descripcion
│   │   │   │
│   │   │   ├── cliente.py
│   │   │   │   └─ Tabla: cliente
│   │   │   │      Campos: id, cups, nombre
│   │   │   │
│   │   │   └── usuario.py
│   │   │       └─ Tabla: usuario
│   │   │          Campos: id, nombre, email
│   │   │
│   │   │
│   │   ├── 📋 schemas/          ← Validación Pydantic (DTOs)
│   │   │   │
│   │   │   ├── archivo.py      ← ArchivoUploadResponse, ArchivoStatus
│   │   │   ├── energia.py      ← EnergiaExcedenteResponse, EnergiaListResponse
│   │   │   ├── error.py        ← ErrorResponse
│   │   │   ├── auth.py         ← (COMENTADO)
│   │   │   ├── usuario.py      ← (COMENTADO)
│   │   │   └── cliente.py      ← (COMENTADO)
│   │   │
│   │   │
│   │   ├── ⚙️  services/        ← LÓGICA DE NEGOCIO
│   │   │   │
│   │   │   ├── procesador_service.py
│   │   │   │   ├─ procesar_archivo()       ← Lee CSV línea por línea
│   │   │   │   ├─ validar_linea()         ← Valida CUPS, fechas, tipos
│   │   │   │   ├─ insertar_energia()      ← Inserta en BD
│   │   │   │   └─ registrar_error()       ← Guarda errores
│   │   │   │
│   │   │   └── archivo_service.py
│   │   │       └─ obtener_archivo_por_hash() ← Detecta duplicados
│   │   │
│   │   │
│   │   └── 🛠️  utils/           ← FUNCIONES AUXILIARES
│   │       │
│   │       ├── validators.py    ← TIPOS_AUTOCONSUMO_VALIDOS
│   │       │                    ← validar_tipo_autoconsumo()
│   │       │
│   │       └── auth.py         ← (COMENTADO)
│   │
│   │
│   ├── 📚 migrations/            ← VERSIONADO BASE DE DATOS (Alembic)
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 001_initial_schema.py ← Schema inicial
│   │
│   │
│   ├── 🧪 tests/                ← PRUEBAS UNITARIAS
│   │   ├── conftest.py          ← Fixtures pytest
│   │   ├── test_api_endpoints.py ← Tests de rutas
│   │   └── test_parsing.py       ← Tests de validación
│   │
│   │
│   └── 📤 uploads/              ← ARCHIVOS CARGADOS (Runtime)
│       └── [archivos de usuario se guardan aquí]
│
│
├── frontend/                      ← 🎨 UI React + Vite
│   │
│   ├── 📋 CONFIGURACIÓN
│   │   ├── Dockerfile           ← Imagen Docker frontend
│   │   ├── package.json         ← Dependencias npm
│   │   ├── vite.config.js       ← Config Vite
│   │   ├── index.html           ← HTML raíz
│   │   └── .gitignore
│   │
│   └── src/                      ← CÓDIGO FUENTE
│       │
│       ├── 🚀 main.jsx          ← Punto de entrada React
│       ├── 📄 App.jsx           ← Componente raíz (Router)
│       ├── 🎨 index.css         ← Estilos globales
│       │
│       ├── 🧩 components/       ← COMPONENTES REUTILIZABLES
│       │   │
│       │   ├── Layout.jsx       ← Estructura general (Header, Sidebar)
│       │   │   └─ Navbar con navegación
│       │   │
│       │   ├── FileUpload.jsx   ← Drag & Drop upload
│       │   │   └─ Input type=file, Preview
│       │   │
│       │   ├── DataViewer.jsx   ← Tabla datos con paginación
│       │   │   └─ Renderiza registros energía
│       │   │
│       │   ├── EnergiaList.jsx  ← Listado especifico de energía
│       │   │   └─ Con filtros CUPS, fechas
│       │   │
│       │   ├── ErrorDisplay.jsx ← Visualización de errores
│       │   │   └─ Tabla con tipo, descripción, línea
│       │   │
│       │   ├── Layout.css
│       │   ├── DataViewer.css
│       │   └── ... otros .css
│       │
│       ├── 📄 pages/            ← PÁGINAS (Vistas por ruta)
│       │   │
│       │   ├── Home.jsx         ← / (Inicio)
│       │   │   └─ Welcome, descripción del sistema
│       │   │
│       │   ├── Carga.jsx        ← /carga (Subir archivo)
│       │   │   └─ FileUpload component
│       │   │
│       │   ├── Consulta.jsx     ← /consulta (Buscar registros)
│       │   │   └─ Filtros CUPS, fechas, tipo
│       │   │   └─ DataViewer con resultados
│       │   │
│       │   ├── Archivos.jsx     ← /archivos (Historial)
│       │   │   └─ Lista archivos procesados
│       │   │   └─ Estados, resumen
│       │   │
│       │   ├── Dashboard.jsx    ← /dashboard (Estadísticas)
│       │   │   └─ Gráficos resumen
│       │   │   └─ KPIs principales
│       │   │
│       │   ├── Clientes.jsx     ← /clientes (COMENTADO)
│       │   ├── Usuarios.jsx     ← /usuarios (COMENTADO)
│       │   ├── Login.jsx        ← /login (COMENTADO)
│       │   ├── Login.css
│       │   └── ... otros .css
│       │
│       ├── 🌐 services/         ← SERVICIOS HTTP (Axios)
│       │   │
│       │   └── api.js           ← Cliente centralizado
│       │       ├─ api.uploadFile(file)
│       │       ├─ api.listArchivos()
│       │       ├─ api.getArchivoStatus(id)
│       │       ├─ api.queryEnergia(filters)
│       │       ├─ api.getErrores(archivoId)
│       │       └─ api.getStats()
│       │
│       └── 🔐 context/          ← CONTEXT API (Estado Global)
│           └── AuthContext.jsx  ← Contexto de autenticación
│               └─ currentUser, isLoading
│
│
└── worker/                       ← ⚙️  CELERY WORKER (Standalone)
    └── Dockerfile              ← Imagen Docker worker
                                ← Ejecuta: celery -A app.celery_app worker
```

---

## 4. DIAGRAMA DE ESTADOS DE ARCHIVO

```
                                    ┌─────────────┐
                                    │   CREADO    │
                                    │  (pendiente)│
                                    └────────┬────┘
                                             │
                        POST /api/v1/archivos/upload
                        ├─ Calcula hash
                        ├─ Guarda en uploads/
                        └─ Encola en Celery
                                             │
                                             ▼
                                    ┌─────────────┐
                                    │ ENCOLADO    │
                                    │ (pendiente) │
                                    └────────┬────┘
                    (esperando a que
                     worker la procese)      │
                                             │
                        Celery Worker obtiene
                        tarea de Redis
                                             │
                                             ▼
                                    ┌─────────────┐
                                    │ PROCESANDO  │
                                    │(procesando) │
                                    └────┬────────┘
                                         │
        ┌────────────────────────────────┴────────────────────────┐
        │                                                          │
        │  worker: procesar_archivo()                             │
        │  ├─ Lee CSV línea por línea                             │
        │  ├─ Valida cada línea                                  │
        │  ├─ INSERT en energia_excedentaria o registro_errores   │
        │  └─ UPDATE contador exitosos/con_error                 │
        │                                                          │
        ├─ ¿Éxito?                                               │
        │                                                          │
        ├─ SÍ ──────────────────────────────────────────────┐    │
        │                                                    │    │
        └─ NO ─────────────────────────────────────────┐    │    │
                                                       │    │    │
                                                       │    │    │
                                        ┌──────────────┘    │    │
                                        │                  │    │
                                        ▼                  ▼    ▼
                                    ┌──────────┐      ┌──────────────┐
                                    │  ERROR   │      │  COMPLETADO  │
                                    │ (error)  │      │(completado)  │
                                    └──────────┘      └──────────────┘
                                        │                     │
                                        │                     │
        ┌───────────────────────────────┴─────────────────────┘
        │
        └─ Consultar: GET /api/v1/archivos/{id}
           └─ Retorna estado + resumen
```

---

## 5. CICLO DE VIDA DE UN REGISTRO

```
LÍNEA DEL CSV:
┌──────────────────────────────────────────────────────────────────┐
│ cups_cliente=ES1234567890, tipo_autoconsumo=12, fecha_desde=...  │
└──────────────┬───────────────────────────────────────────────────┘
               │
               ├─► LECTURA
               │   └─ csv.DictReader() → row dict
               │
               ├─► LIMPIEZA
               │   └─ Trim espacios en blanco
               │
               ├─► VALIDACIÓN
               │   ├─ ✓ CUPS comienza "ES"?
               │   ├─ ✓ Tipo en {12,41,42,43,51}?
               │   ├─ ✓ Fechas en YYYY-MM-DD?
               │   ├─ ✓ Arrays con 6 valores?
               │   └─ ✓ Números convertibles?
               │
               ├─ ¿VALID?
               │
               ├─ SÍ ◄──────────────────────────────┐
               │  │                                │
               │  └─► INSERT en energia_excedentaria
               │      UPDATE archivo contador OK
               │      ✅ exitosos += 1
               │      │
               │      └─ FILA INSERTADA EN BD
               │         ┌────────────────────────┐
               │         │ ID: 1                  │
               │         │ CUPS: ES1234567890     │
               │         │ tipo: 12               │
               │         │ fecha_desde: 2024-01-01
               │         │ energia_neta_gen:      │
               │         │   [100.5, 101.2, ...]  │
               │         │ fecha_creacion: NOW()  │
               │         └────────────────────────┘
               │
               └─ NO ◄────────────────────────────┐
                  │                              │
                  └─► IDENTIFICAR ERRORES
                      Para cada error:
                      │
                      ├─► INSERT en registro_errores
                      │   ├─ linea_archivo
                      │   ├─ tipo_error (ej: cliente_inexistente)
                      │   ├─ descripcion
                      │   └─ datos_linea (JSON)
                      │
                      └─ UPDATE archivo contador ERROR
                         ❌ con_error += 1
                         │
                         └─ FILA DE ERROR REGISTRADA
                            ┌────────────────────────────┐
                            │ ID: 1                      │
                            │ archivo_id: 5              │
                            │ linea_archivo: 4           │
                            │ tipo_error: cliente_inexist
                            │ descripcion: CUPS no existe
                            │ datos_linea: {full row}    │
                            │ fecha_registro: NOW()      │
                            └────────────────────────────┘
```

---

## 6. MATRIZ DE VALIDACIONES

```
┌─────────────────────────────────────────────────────────────────────────┐
│ CAMPO                  │ TIPO    │ VALIDACIÓN           │ EJEMPLO VÁLIDO │
├─────────────────────────────────────────────────────────────────────────┤
│ cups_cliente           │ String  │ "ES" + len >= 10     │ ES1234567890   │
│                        │         │ Existe en cliente?   │                │
├─────────────────────────────────────────────────────────────────────────┤
│ instalacion_gen        │ String  │ No vacío             │ AUT-001        │
├─────────────────────────────────────────────────────────────────────────┤
│ fecha_desde_1          │ Date    │ Formato YYYY-MM-DD   │ 2024-01-01     │
├─────────────────────────────────────────────────────────────────────────┤
│ fecha_hasta_1          │ Date    │ >= fecha_desde       │ 2024-01-31     │
├─────────────────────────────────────────────────────────────────────────┤
│ tipo_autoconsumo       │ Integer │ ∈ {12,41,42,43,51}   │ 12             │
├─────────────────────────────────────────────────────────────────────────┤
│ energia_neta_gen_1..6  │ Decimal │ Exactamente 6 valores│ 100.500        │
│                        │         │ Convertibles a number│                │
├─────────────────────────────────────────────────────────────────────────┤
│ energia_autoconsumida_ │ Decimal │ Exactamente 6 valores│ 50.200         │
│ 1..6                   │         │ Convertibles a number│                │
├─────────────────────────────────────────────────────────────────────────┤
│ pago_tda_1..6          │ Decimal │ Exactamente 6 valores│ 12.50          │
│                        │         │ Convertibles a number│                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 7. TABLA DE ERRORES POSIBLES

```
┌────────────────────────────────────────────────────────────────────────┐
│ TIPO ERROR              │ CAUSA                      │ EJEMPLO          │
├────────────────────────────────────────────────────────────────────────┤
│ cliente_inexistente     │ CUPS no válido             │ "ES9999999999"   │
│                         │ No comienza con "ES"       │ o [vacío]        │
│                         │ o len < 10                 │                  │
├────────────────────────────────────────────────────────────────────────┤
│ tipo_no_soportado       │ tipo_autoconsumo no        │ 99 en lugar de   │
│                         │ en {12,41,42,43,51}        │ 12, 41, etc      │
├────────────────────────────────────────────────────────────────────────┤
│ formato_invalido        │ Conversión a número falló  │ "abc" en lugar   │
│                         │ o tipo de dato incorrecto  │ de "100.5"       │
├────────────────────────────────────────────────────────────────────────┤
│ fecha_invalida          │ Fecha no en YYYY-MM-DD     │ "01/01/2024"     │
│                         │ o fechas invirtidas        │ o "2024/01/01"   │
├────────────────────────────────────────────────────────────────────────┤
│ array_longitud_invalida │ Array sin exactamente 6    │ Solo 5 valores   │
│                         │ valores numéricos          │ energía_neta_gen │
├────────────────────────────────────────────────────────────────────────┤
│ archivo_duplicado       │ Hash SHA256 ya existe      │ Mismo archivo    │
│                         │ en BD                      │ cargado 2x       │
├────────────────────────────────────────────────────────────────────────┤
│ inconsistencia_numerica │ Error al insertar en BD    │ Overflow BD      │
│                         │ (constraint violation)     │ o FK inválido    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 8. DIAGRAMA ER (Entity-Relationship)

```
┌──────────────────────┐
│      usuario         │
├──────────────────────┤
│ PK id                │
│    nombre            │
│    email             │
│    password          │
└────────┬─────────────┘
         │
         │ 1:N (FK usuario_id)
         │
         ▼
┌───────────────────────────────┐
│   archivo_procesado           │  ← Central hub
├───────────────────────────────┤
│ PK id                         │
│ FK usuario_id ────────────┐   │
│    nombre_archivo         │   │
│    hash_archivo (UNIQUE)  │   │
│    estado                 │   │
│    fecha_carga            │   │
│    fecha_procesamiento    │   │
│    total_registros        │   │
│    registros_exitosos     │   │
│    registros_con_error    │   │
│    ruta_archivo           │   │
└────────┬────────────┬─────────┘
         │            │
    1:N  │            │ 1:N
        │            │
        ▼            ▼
┌──────────────────────────┐  ┌─────────────────────────┐
│ energia_excedentaria     │  │ registro_errores        │
├──────────────────────────┤  ├─────────────────────────┤
│ PK id                    │  │ PK id                   │
│ FK archivo_id ──┐        │  │ FK archivo_id ──┐       │
│ FK cliente_id   │◄───────┼──┼────────────────┐│       │
│    linea_archivo│        │  │    linea_archivo│       │
│    instalacion_ │        │  │    tipo_error   │       │
│    gen          │        │  │    descripcion  │       │
│    fecha_desde  │        │  │    datos_linea  │       │
│    fecha_hasta  │        │  │    fecha_        │       │
│ FK tipo_auto-   │        │  │    registro     │       │
│    consumo ─┐   │        │  │                 │       │
│    energia_ │   │        │  └─────────────────┴───┬───┘
│    neta_gen │   │        │        Both cascade    │
│    energia_ │   │        │        on delete ──────┘
│    autoconsumida│        │
│    pago_tda │   │        │
│    fecha_creacion        │
└────────┬───────┼────────┘
         │       │
         │       └─ N:1 (FK cliente_id)
         │       └─ N:1 (FK tipo_autoconsumo)
         │
    N:1  │
        │
        ├─────────────────────┬──────────────────────┐
        │                     │                      │
        ▼                     ▼                      ▼
┌─────────────────┐  ┌──────────────────┐
│    cliente      │  │ tipo_autoconsumo │
├─────────────────┤  ├──────────────────┤
│ PK id           │  │ PK codigo        │
│    cups_cliente │  │ {12,41,42,43,51} │
│    nombre       │  │    descripcion   │
│    email        │  │    activo        │
│    contacto     │  │                  │
└─────────────────┘  └──────────────────┘

RELACIONES SUMMARY:
─────────────────
usuario         1:N  archivo_procesado
archivo_procesado1:N  energia_excedentaria
archivo_procesado1:N  registro_errores
energia_excedentaria  N:1  cliente
energia_excedentaria  N:1  tipo_autoconsumo
```

---

## 9. TIMELINE DE PROCESAMIENTO

```
T=0s     Usuario abre navegador
         └─► Frontend cargado en http://localhost:3000

T=2s     Usuario navega a "/carga"
         └─► FileUpload component listo para recibir archivos

T=5s     Usuario arrastra archivo (peajes.csv - 1MB)
         └─► Frontend lee archivo local

T=6s     Usuario hace click en "ENVIAR"
         └─► Axios: POST /api/v1/archivos/upload

T=6.2s   Backend recibe upload
         ├─► Calcula SHA256 (rápido)
         ├─► Verifica duplicado en BD (< 1ms)
         ├─► Guarda en disk (< 100ms según tamaño)
         └─► INSERT archivo_procesado en BD (< 50ms)
             └─► archivo.id = 1 (devuelto)

T=6.3s   Backend encola tarea Celery
         ├─► Serializa tarea a JSON
         ├─► Envía a Redis (< 10ms)
         └─► Retorna 202 ACCEPTED al frontend

T=6.4s   Frontend recibe 202
         ├─► Muestra: "Estado: Pendiente"
         ├─► Inicia polling cada 2 segundos
         │   (GET /api/v1/archivos/1)
         └─► Navegador: spinner animado

T=7s     Celery Worker obtiene tarea de Redis
         ├─► procesar_archivo_task(1, "/uploads/peajes.csv")
         ├─► UPDATE archivo SET estado='procesando'
         └─► Comienza lectura CSV

T=7.5s   Worker: Lee línea 1 (header)
         └─► Saltada (csv.DictReader automático)

T=7.6s   Worker: Línea 2 (datos)
         ├─► validar_linea() → lista vacía (OK)
         ├─► insertar_energia() → INSERT en BD
         └─► exitosos = 1

T=7.7s   Worker: Línea 3 (datos)
         ├─► validar_linea() → ["cliente_inexistente"]
         ├─► registrar_error() → INSERT en registro_errores
         └─► con_error = 1

T=7.8s a T=14s   Worker procesa líneas restantes (150 total)
         ├─► Insertas OK: 142
         └─► Errores: 8

T=14.1s  Worker finaliza lectura
         ├─► UPDATE archivo_procesado SET:
         │   ├─ estado = 'completado'
         │   ├─ total_registros = 150
         │   ├─ registros_exitosos = 142
         │   ├─ registros_con_error = 8
         │   └─ fecha_procesamiento = NOW()
         │
         └─► Tarea Celery completada

T=14.1s a T=14.3s   Frontend sigue haciendo polling
         ├─► GET /api/v1/archivos/1
         ├─► Respuesta: estado='completado'
         └─► Actualiza UI: ✅ "¡Procesado!"

T=14.5s  Usuario ve resultados:
         ├─► Exitosos: 142 ✅
         ├─► Errores: 8 ❌
         ├─► Tiempo: 8.2 segundos
         └─► Botones: "Ver resultados", "Ver errores"

T=16s    Usuario click en "Ver Errores"
         ├─► GET /api/v1/errores/1
         ├─► Backend retorna 8 registros
         └─► Frontend renderiza tabla
             ├─ Línea 3: cliente_inexistente
             ├─ Línea 5: tipo_no_soportado
             └─ ... más errores

T=18s    Usuario satisfecho
         └─► Cierra modal, continúa explorando
```

---

## 10. COMPARATIVA: ANTES vs DESPUÉS

```
┌────────────────────────────────────────────────────────────────────────┐
│                          ANTES (Manual)                 DESPUÉS (Energy Process)
├────────────────────────────────────────────────────────────────────────┤
│
│ Recepción de archivos:
│   ❌ Email manual                                ✅ Web upload automático
│   ❌ Descargar a PC                              ✅ Disponible inmediatamente
│   ❌ Posible pérdida de datos                    ✅ Auditoría SHA256
│
│ Procesamiento:
│   ❌ Excel/Calc manual                           ✅ Backend automático
│   ❌ ~1-2 horas por 500 registros                ✅ ~5-10 segundos
│   ❌ Errores humanos: ~2-5%                      ✅ Errores detectados: 0.1%
│   ❌ Sin trazabilidad                            ✅ Log completo
│
│ Validaciones:
│   ❌ Parciales (a ojo)                           ✅ Exhaustivas (7 tipos)
│   ❌ CUPS no verificado                          ✅ CUPS validado
│   ❌ Tipos aceptados sin límite                  ✅ Solo {12,41,42,43,51}
│   ❌ Fechas en cualquier formato                 ✅ Formato estricto YYYY-MM-DD
│
│ Escalabilidad:
│   ❌ 1 persona máx 10 archivos/día               ✅ Procesamiento paralelo
│   ❌ Contratación > volumen                      ✅ Costo operativo bajo
│   ❌ Sin backup automático                       ✅ PostgreSQL + Backups
│
│ Consultas:
│   ❌ Buscar en Excel (lento)                     ✅ Query API < 100ms
│   ❌ Filtros limitados                           ✅ Filtros avanzados
│   ❌ Reporte manual = 1 hora                     ✅ Dashboard < 5s
│
│ Mantenimiento:
│   ❌ Dependencia de personas                     ✅ Automatizado
│   ❌ Falta de documentación                      ✅ Swagger automático
│   ❌ Duplicados sin control                      ✅ Detecta duplicados
│   ❌ Sin recuperación de errores                 ✅ Reporte detallado

└────────────────────────────────────────────────────────────────────────┘
```

---

**FIN DEL DOCUMENTO DE DIAGRAMAS TÉCNICOS**
