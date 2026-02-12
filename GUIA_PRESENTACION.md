# 🔋 ENERGY PROCESS - Guía Ejecutiva para Presentación

**Sistema de Procesamiento de Energía Excedentaria**

---

## 📊 RESUMEN EJECUTIVO (5 minutos)

### ¿Qué es Energy Process?

Es una **plataforma web completa** que automatiza el procesamiento de archivos de energía excedentaria de instalaciones de autoconsumo. Permite cargar, validar, procesar y consultar datos de generación de energía de forma rápida y confiable.

### Problema que Resuelve

- ❌ **Antes**: Procesamiento manual de archivos → errores, tiempo → demoras
- ✅ **Ahora**: Automático, validado, auditable, escalable

### Tecnología Stack

```
BACKEND          FRONTEND         INFRAESTRUCTURA
┌─────────────┐  ┌─────────────┐  ┌─────────────────┐
│ FastAPI     │  │ React 18.2  │  │ Docker Compose  │
│ Python 3.9+ │  │ Vite 5.0    │  │ PostgreSQL 15   │
│ SQLAlchemy  │  │ Axios       │  │ Redis 7         │
│ Celery 5.3  │  │ CSS Puro    │  │ Nginx (proxy)   │
│ Pydantic    │  │             │  │ Alembic (ORM)   │
└─────────────┘  └─────────────┘  └─────────────────┘
```

---

## 🎯 CARACTERÍSTICAS PRINCIPALES

### 1️⃣ Carga de Archivos
- ✅ Soporta **CSV, XML, TXT** (actualmente CSV implementado)
- ✅ **Detección de duplicados** por hash SHA256
- ✅ Interfaz **drag & drop** intuitiva
- ✅ Validaciones en **tiempo real**

### 2️⃣ Procesamiento Automático
- ✅ **Asincrónico** con Celery (no bloquea la API)
- ✅ Procesa **línea por línea** con validaciones
- ✅ **Registro detallado** de errores
- ✅ Transaccional con rollback automático

### 3️⃣ Validaciones Exhaustivas
- ✅ **CUPS** (Código Único Punto Suministro)
- ✅ **Tipos de Autoconsumo** {12, 41, 42, 43, 51}
- ✅ **Fechas** en formato YYYY-MM-DD
- ✅ **Arrays numéricos** exactamente 6 valores (P1-P6)
- ✅ **Números decimales** convertibles

### 4️⃣ Consultas Flexibles
- ✅ Búsqueda por **CUPS**
- ✅ Filtro por **rango de fechas**
- ✅ Filtro por **tipo de autoconsumo**
- ✅ Combinación de filtros

### 5️⃣ Análisis de Errores
- ✅ Visualización por **archivo**
- ✅ Detalle de **línea, tipo, descripción**
- ✅ Datos originales para auditoría
- ✅ Exportable para análisis

### 6️⃣ Dashboard y Estadísticas
- ✅ **Resumen** de procesamiento
- ✅ Gráficos de **éxito/error**
- ✅ Historial de **archivos**
- ✅ KPIs de rendimiento

---

## 🏗️ ARQUITECTURA VISUAL

```
                        🌐 USUARIO
                       (Navegador)
                            │
                            │ HTTP
                            ▼
      ┌─────────────────────────────────────────────┐
      │         🎨 FRONTEND (React Vite)            │
      │  ┌──────────────────────────────────────┐  │
      │  │ Pages:                               │  │
      │  │ • Home        • Dashboard             │  │
      │  │ • Carga       • Consulta              │  │
      │  │ • Archivos    • Usuarios (comentado) │  │
      │  └──────────────────────────────────────┘  │
      └─────────────────────────────────────────────┘
                            │
                       REST API
                            │
      ┌─────────────────────────────────────────────────┐
      │  🔧 BACKEND (FastAPI + Python)                  │
      │  ┌──────────────────────────────────────────┐  │
      │  │ Rutas HTTP:                              │  │
      │  │ • POST   /api/v1/archivos/upload         │  │
      │  │ • GET    /api/v1/archivos                │  │
      │  │ • GET    /api/v1/energia (con filtros)   │  │
      │  │ • GET    /api/v1/errores                 │  │
      │  │ • GET    /api/v1/stats                   │  │
      │  └──────────────────────────────────────────┘  │
      │                                                 │
      │  ┌──────────────────────────────────────────┐  │
      │  │ Servicios:                               │  │
      │  │ • Procesador (parsing, validación)       │  │
      │  │ • Archivo (gestión, deduplicación)       │  │
      │  │ • Validadores (CUPS, fechas, etc)        │  │
      │  └──────────────────────────────────────────┘  │
      └─────────────────────────────────────────────────┘
                    │         │          │
         ┌──────────┼─────────┼──────────┐
         │          │         │          │
         ▼          ▼         ▼          ▼
      ┌─────┐   ┌──────┐  ┌──────┐  ┌─────────────┐
      │PostgreSQL│ Redis  │ Redis  │ Celery Worker
      │  (Data)  │(Broker)│(Cache) │ (Async)
      └─────┘   └──────┘  └──────┘  └─────────────┘
```

---

## 📈 FLUJO DE PROCESAMIENTO

### Paso a Paso (Simplificado)

```
1. USUARIO SUBE ARCHIVO
   └─► POST /api/v1/archivos/upload
       └─► Frontend carga archivo CSV

2. BACKEND RECIBE
   ├─► Calcula SHA256 (hash único)
   ├─► Verifica que no sea duplicado
   ├─► Guarda en carpeta uploads/
   └─► Crea registro en base de datos

3. SE ENCOLA TAREA
   ├─► Se envía a Redis (cola de tareas)
   └─► API retorna 202 "En procesamiento"

4. WORKER CELERY PROCESA
   ├─► Obtiene archivo
   ├─► Lee línea por línea (CSV)
   └─► Para cada línea:
       ├─► VALIDAR
       │   ├─► CUPS válido? ✓ o ✗
       │   ├─► Tipo en {12,41,42,43,51}? ✓ o ✗
       │   ├─► Fechas YYYY-MM-DD? ✓ o ✗
       │   ├─► Arrays con 6 valores? ✓ o ✗
       │   └─► Números válidos? ✓ o ✗
       │
       ├─► Si hay ERROR
       │   └─► Registra en tabla "registro_errores"
       │
       └─► Si OK
           └─► Inserta en tabla "energia_excedentaria"

5. FINALIZACIÓN
   ├─► Actualiza estado archivo a "completado"
   ├─► Guarda: total registros, exitosos, con error
   └─► Usuario puede consultar resultados
```

---

## 🗂️ ESTRUCTURA CONCEPTUAL

### Base de Datos (5 tablas principales)

```
┌────────────────────────────┐
│    archivo_procesado       │  ◄─ Archivo subido
│  - id (PK)                 │
│  - nombre_archivo          │
│  - hash_archivo (UNIQUE)   │
│  - estado (pendiente/...)  │
│  - registros_exitosos      │
│  - registros_con_error     │
└────────┬─────────┬─────────┘
         │ 1:N     │ 1:N
         ▼         ▼
    ┌──────────┐  ┌──────────────────────┐
    │ energia_ │  │ registro_errores     │  ◄─ Errores por línea
    │excedent. │  │  - linea_archivo     │
    │          │  │  - tipo_error        │
    │ ARRAY    │  │  - descripcion       │
    │ [6 vals] │  │  - datos_linea (JSON)
    └──────────┘  └──────────────────────┘
         │
         │ N:1
         ▼
    ┌──────────────┐      ┌──────────────────┐
    │   cliente    │◄─────│ tipo_autoconsumo │
    │ - cups       │      │ - codigo {12..51}
    │ - nombre     │      │ - descripcion    │
    └──────────────┘      └──────────────────┘
```

---

## 🎯 CLASIFICACIÓN DE CUPS

### ¿Qué es?
**CUPS** = Código Único de Punto de Suministro (20-22 caracteres)

### Estructura
```
ES 1234 12 12 X 1234567890 A
├─ País: ES (España)
├─ Distribuidora: 4 dígitos
├─ Provincia: 2 dígitos
├─ Municipio: 2 dígitos
├─ Consumidor: 1 letra
├─ Suministro: 10 dígitos
└─ Control: 1 letra (A-J)
```

### Validación
| Validación | Status | Requisito |
|-----------|--------|-----------|
| Formato | ✓ | Comienza con "ES" |
| Longitud | ✓ | >= 10 caracteres |
| Existencia | ⚠️ | En tabla cliente (futuro) |
| Dígito control | ⚠️ | Según algoritmo official |

### Error Típico
```
Línea 5 del archivo:
  CUPS: "ES9999999999"
  Error: "CUPS ES9999999999 no encontrado en sistema"
  Tipo: cliente_inexistente
```

---

## 🔄 PROCESAMIENTO DE ARCHIVOS CSV

### Formato Esperado

**Cabecera requerida:**
```csv
cups_cliente,instalacion_gen,fecha_desde_1,fecha_hasta_1,tipo_autoconsumo,
energia_neta_gen_1,energia_neta_gen_2,energia_neta_gen_3,energia_neta_gen_4,energia_neta_gen_5,energia_neta_gen_6,
energia_autoconsumida_1,energia_autoconsumida_2,energia_autoconsumida_3,energia_autoconsumida_4,energia_autoconsumida_5,energia_autoconsumida_6,
pago_tda_1,pago_tda_2,pago_tda_3,pago_tda_4,pago_tda_5,pago_tda_6
```

**Datos de ejemplo:**
```csv
ES1234567890,AUT-001,2024-01-01,2024-01-31,12,100.5,101.2,99.8,102.1,100.9,101.3,50.2,49.8,51.1,50.5,50.9,49.6,12.50,12.45,12.78,12.63,12.72,12.40
ES1111111111,AUT-002,2024-01-01,2024-01-31,41,110.0,112.5,108.3,113.2,111.1,112.0,60.0,62.0,55.0,65.0,58.0,61.0,14.50,15.00,13.50,16.00,14.50,15.20
```

### Tipos de Autoconsumo

| Código | Descripción | Modalidad |
|--------|-------------|-----------|
| **12** | Autoconsumo sin excedentes | - |
| **41** | Autoconsumo con excedentes | Compensación |
| **42** | Autoconsumo con excedentes | Venta |
| **43** | Autoconsumo con excedentes | Almacenamiento |
| **51** | Consumo propios con generación | - |

### Validaciones por Campo

| Campo | Tipo | Validación | Ejemplo OK | Ejemplo ERROR |
|-------|------|-----------|-----------|---------------|
| `cups_cliente` | String | Comienza "ES", len >= 10 | ES1234567890 | 1234567890 |
| `instalacion_gen` | String | No vacío | AUT-001 | (vacío) |
| `fecha_desde_1` | Date | YYYY-MM-DD | 2024-01-01 | 01/01/2024 |
| `fecha_hasta_1` | Date | >= fecha_desde | 2024-01-31 | 2023-12-31 |
| `tipo_autoconsumo` | Int | En {12,41,42,43,51} | 12 | 99 |
| `energia_neta_gen_1..6` | Decimal | 6 valores numéricos | 100.5 | abc |
| `energia_autoconsumida_1..6` | Decimal | 6 valores numéricos | 50.2 | - |
| `pago_tda_1..6` | Decimal | 6 valores numéricos | 12.50 | - |

### Errores Registrados

```
┌─────────────────────────────────────────────────────────┐
│ TIPO_ERROR              │ DESCRIPCIÓN                     │
├─────────────────────────────────────────────────────────┤
│ cliente_inexistente     │ CUPS no encontrado              │
│ tipo_no_soportado       │ Tipo autoconsumo inválido       │
│ formato_invalido        │ Formato datos incorrecto        │
│ fecha_invalida          │ Fecha no en YYYY-MM-DD          │
│ array_longitud_invalida │ Array sin exactamente 6 valores │
│ archivo_duplicado       │ Hash SHA256 repetido            │
│ inconsistencia_numerica │ Error al insertar en BD         │
└─────────────────────────────────────────────────────────┘
```

### Ejemplo de Procesamiento

```
Archivo: peajes_enero_2024.csv
Total líneas: 150

Línea  1 (Header):     [IGNORADA]
Línea  2:              ✅ OK          → Insertado
Línea  3:              ✅ OK          → Insertado
Línea  4:              ❌ CUPS vacío  → Registro error "cliente_inexistente"
Línea  5:              ✅ OK          → Insertado
...
Línea 150:             ❌ Tipo 99     → Registro error "tipo_no_soportado"

Resumen Final:
  • Total registros: 149 (sin header)
  • Exitosos: 142
  • Con error: 7
  • Tiempo: 8.2 segundos
```

---

## 🌐 RUTAS API (Resumen Rápido)

### Archivos

```bash
# Upload
POST /api/v1/archivos/upload
Content-Type: multipart/form-data

# List
GET /api/v1/archivos?limit=20

# Status
GET /api/v1/archivos/{id}
```

### Energía

```bash
# Consulta con filtros
GET /api/v1/energia \
  ?cups=ES1234567890 \
  &fecha_desde=2024-01-01 \
  &fecha_hasta=2024-01-31 \
  &tipo_autoconsumo=12
```

### Errores

```bash
# Todos
GET /api/v1/errores

# Por archivo
GET /api/v1/errores/{archivo_id}
```

### Estadísticas

```bash
GET /api/v1/stats
→ {
    "total_archivos": 10,
    "archivos_completados": 9,
    "total_registros": 5000,
    "registros_exitosos": 4850,
    "registros_con_error": 150
  }
```

---

## 🛠️ TECNOLOGÍAS EXPLICADAS

### Backend

**FastAPI**
- Framework web moderno y muy rápido
- Genera documentación automática (Swagger)
- Validación automática con Pydantic
- Type hints para seguridad

**SQLAlchemy**
- ORM (Object-Relational Mapping)
- Convierte clases Python en tablas SQL
- Previene SQL injection automáticamente
- Migraciones versionadas con Alembic

**Celery**
- Sistema de tareas asincrónicas
- No bloquea la API principal
- Escala horizontalmente (múltiples workers)
- Persistencia con Redis

**Pydantic**
- Validación de datos con type hints
- Conversión automática de tipos
- Esquemas reutilizables
- Documentación automática

### Frontend

**React**
- Librería de interfaz (UI)
- Componentes reutilizables
- Estado reactivo
- Virtual DOM para rendimiento

**Vite**
- Build tool ultrarrápido
- Dev server con Hot Module Replacement (HMR)
- Optimización automática
- Soporta módulos nativos ES6

**Axios**
- Cliente HTTP para consumir APIs
- Manejo automático de JSON
- Interceptores para auth
- Cancellable requests

### Infraestructura

**Docker & Docker Compose**
- Contenedorización consistente
- Servicios orquestados
- Reproducibilidad garantizada
- Escalable

**PostgreSQL**
- Base de datos relacional robusta
- ACID transactions
- Tipos de datos ricos
- Backup automático

**Redis**
- In-memory data store
- Broker para Celery
- Cache rápido
- Pub/Sub messaging

---

## 📊 EJEMPLO DE DATOS

### Registro Insertado Correctamente

```json
{
  "id": 1,
  "archivo_id": 5,
  "cups_cliente": "ES1234567890",
  "instalacion_gen": "AUT-001",
  "tipo_autoconsumo": 12,
  "fecha_desde": "2024-01-01",
  "fecha_hasta": "2024-01-31",
  "energia_neta_gen": [
    "100.500",
    "101.200",
    "99.800",
    "102.100",
    "100.900",
    "101.300"
  ],
  "energia_autoconsumida": [
    "50.200",
    "49.800",
    "51.100",
    "50.500",
    "50.900",
    "49.600"
  ],
  "pago_tda": [
    "12.50",
    "12.45",
    "12.78",
    "12.63",
    "12.72",
    "12.40"
  ],
  "fecha_creacion": "2024-02-05T10:35:30Z"
}
```

### Error Registrado

```json
{
  "id": 1,
  "archivo_id": 5,
  "linea_archivo": 4,
  "tipo_error": "cliente_inexistente",
  "descripcion": "CUPS ES9999999999 no encontrado en sistema",
  "datos_linea": {
    "cups_cliente": "ES9999999999",
    "instalacion_gen": "AUT-999",
    "fecha_desde_1": "2024-01-01",
    "tipo_autoconsumo": "12",
    "energia_neta_gen_1": "100.5"
  },
  "fecha_registro": "2024-02-05T10:35:31Z"
}
```

---

## 🚀 PUNTOS CLAVE DE LA PRESENTACIÓN

### 1. **Automatización**
   - Elimina procesamiento manual
   - Reduce errores humanos
   - Acelera tiempo de procesamiento

### 2. **Escalabilidad**
   - Múltiples workers Celery
   - PostgreSQL can handle millions of records
   - Stateless API permite load balancing

### 3. **Confiabilidad**
   - Validaciones exhaustivas
   - Registro completo de errores
   - Transacciones ACID
   - Detección de duplicados

### 4. **Usabilidad**
   - Interfaz intuitiva (drag & drop)
   - Búsqueda avanzada
   - Dashboard informativo
   - Documentación automática (Swagger)

### 5. **Mantenibilidad**
   - Código modular y limpio
   - Type hints (Python)
   - Tests automatizados
   - Migraciones versionadas

### 6. **Extensibilidad**
   - Fácil agregar nuevos formatos (XML, JSON)
   - Nuevos validadores
   - Nuevas rutas API
   - Nuevos tipos de autoconsumo

---

## 💡 DIAPOSITIVA FINAL

```
┌──────────────────────────────────────────────────────────┐
│                    ENERGY PROCESS                         │
│                                                            │
│  De la Complejidad Manual → Automatización Inteligente   │
│                                                            │
│  ✅ Archivos procesados: 10+                             │
│  ✅ Registros insertados: 5,000+                         │
│  ✅ Errores detectados: 150+                             │
│  ✅ Tiempo medio: < 10 segundos                          │
│                                                            │
│  Stack Moderno: Python + React + PostgreSQL + Celery    │
│  Deployed: Docker Compose → Ready for Production         │
│                                                            │
│  Siguiente: Autenticación, ML para predicción, BI        │
└──────────────────────────────────────────────────────────┘
```

---

**Fin de la Guía Ejecutiva**
