# ⚡ ENERGY PROCESS - Quick Reference & FAQ

---

## 🎯 QUICK START (5 minutos)

### Opción 1: Docker (Recomendado)

```bash
# 1. Clonar y navegar
git clone <repo> && cd Energy_Process

# 2. Crear .env (opcional)
cat > .env << EOF
POSTGRES_USER=postgres
POSTGRES_PASSWORD=0823
POSTGRES_DB=energy_process
EOF

# 3. Iniciar servicios
docker-compose up -d

# 4. Esperar 30 segundos

# 5. Acceder
Frontend:     http://localhost:3000
API Docs:     http://localhost:8000/docs
Backend:      http://localhost:8000
```

### Opción 2: Local Dev

```bash
# Terminal 1 - Backend
cd backend && python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 2 - Worker (si tienes Redis local)
cd backend
celery -A app.celery_app worker -l info

# Terminal 3 - Frontend
cd frontend && npm install && npm run dev
```

---

## 📚 DOCUMENTACIÓN POR TEMA

### Para Presentación (5-10 min)
→ Lee: `GUIA_PRESENTACION.md`
- Resumen ejecutivo
- Stack tecnológico
- Características principales
- Flujo de procesamiento simplificado

### Para Comprensión Técnica (30-60 min)
→ Lee: `README_COMPLETO.md`
- Arquitectura completa
- Estructura de carpetas
- Descripción de cada módulo
- APIs REST
- Modelos de datos

### Para Diagramas Visuales
→ Lee: `DIAGRAMAS_TECNICOS.md`
- Arquitectura de sistema
- Flujo de datos
- Estructura de carpetas visual
- Estados de archivo
- Timeline de procesamiento
- Comparativa antes/después

### Esta documento (Quick Reference)
→ `QUICK_REFERENCE.md`
- Comandos útiles
- Endpoints API rápido
- Preguntas frecuentes
- Troubleshooting

---

## 🔧 COMANDOS ÚTILES

### Docker Compose

```bash
# Ver estado de servicios
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f backend      # Backend
docker-compose logs -f worker       # Worker Celery
docker-compose logs -f postgres     # BD
docker-compose logs -f              # Todo

# Reiniciar servicios
docker-compose restart backend
docker-compose restart worker
docker-compose restart

# Detener todo
docker-compose down

# Detener y limpiar volúmenes
docker-compose down -v

# Ejecutar comando en contenedor
docker-compose exec backend bash
docker-compose exec postgres psql -U postgres -d energy_process

# Ver recursos (CPU, RAM)
docker stats
```

### Base de Datos (PostgreSQL)

```bash
# Conectar directamente
psql postgresql://postgres:0823@localhost:5432/energy_process

# Queries útiles
# Ver archivos procesados
SELECT id, nombre_archivo, estado, registros_exitosos, registros_con_error 
FROM archivo_procesado ORDER BY fecha_carga DESC LIMIT 10;

# Ver registros de energía
SELECT * FROM energia_excedentaria WHERE cups_cliente = 'ES1234567890';

# Ver errores de un archivo
SELECT linea_archivo, tipo_error, descripcion 
FROM registro_errores WHERE archivo_id = 1;

# Contar registros por tipo de error
SELECT tipo_error, COUNT(*) as cantidad 
FROM registro_errores GROUP BY tipo_error;

# Estadísticas generales
SELECT 
  COUNT(DISTINCT archivo_id) as total_archivos,
  COUNT(*) as total_registros,
  COUNT(CASE WHEN tipo_error = 'cliente_inexistente' THEN 1 END) as cups_invalidos
FROM energia_excedentaria;
```

### Celery (Task Queue)

```bash
# Ver tareas activas
celery -A app.celery_app inspect active

# Ver tareas en cola
celery -A app.celery_app inspect reserved

# Ver tareas programadas
celery -A app.celery_app inspect scheduled

# Purgar cola (¡cuidado!)
celery -A app.celery_app purge

# Reiniciar worker
celery -A app.celery_app control shutdown
celery -A app.celery_app worker -l info  # Iniciar de nuevo

# Ver stats del worker
celery -A app.celery_app inspect stats
```

### Redis

```bash
# Conectar a Redis
redis-cli

# Comandos útiles
PING                        # Test conexión
KEYS *                      # Ver todas las claves
KEYS "celery*"              # Ver tareas Celery
GET <key>                   # Ver valor de clave
TTL <key>                   # Ver tiempo de expiración
FLUSHDB                     # Limpiar BD (¡cuidado!)
INFO                        # Ver estadísticas
```

### Migraciones (Alembic)

```bash
# Crear nueva migración
alembic revision --autogenerate -m "Add new column"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1

# Ver historial
alembic history

# Ver estado actual
alembic current

# Upgrade a versión específica
alembic upgrade ae1027a6f9a
```

### Tests

```bash
# Ejecutar todos los tests
pytest

# Test específico
pytest tests/test_api_endpoints.py -v

# Con coverage
pytest --cov=app tests/

# Mostrar prints
pytest -s

# Tests en paralelo
pytest -n auto
```

---

## 🌐 ENDPOINTS API RÁPIDO

### Archivos

```bash
# Subir archivo
curl -X POST http://localhost:8000/api/v1/archivos/upload \
  -F "file=@peajes.csv"

# Listar archivos
curl http://localhost:8000/api/v1/archivos?limit=10

# Estado archivo
curl http://localhost:8000/api/v1/archivos/1
```

### Energía

```bash
# Todos los registros
curl http://localhost:8000/api/v1/energia

# Con filtros
curl "http://localhost:8000/api/v1/energia?cups=ES1234567890&tipo_autoconsumo=12"

# Por rango de fechas
curl "http://localhost:8000/api/v1/energia?fecha_desde=2024-01-01&fecha_hasta=2024-01-31"
```

### Errores

```bash
# Todos los errores
curl http://localhost:8000/api/v1/errores

# Errores archivo específico
curl http://localhost:8000/api/v1/errores/1
```

### Estadísticas

```bash
# Resumen
curl http://localhost:8000/api/v1/stats
```

### Documentación

```bash
# Swagger UI
http://localhost:8000/docs

# ReDoc
http://localhost:8000/redoc

# OpenAPI JSON
http://localhost:8000/openapi.json
```

---

## ❓ PREGUNTAS FRECUENTES

### **P: ¿Cuánto tarda en procesarse un archivo?**

**R:** Depende del tamaño:
- 100 registros: 0.5-1 segundo
- 1,000 registros: 5-10 segundos
- 10,000 registros: 30-60 segundos

Incluye: validación, inserción en BD, y transacciones ACID.

---

### **P: ¿Qué pasa si subo el mismo archivo dos veces?**

**R:** El sistema lo detecta por SHA256 hash:
1. Calcula hash del archivo
2. Busca en BD si ya existe
3. Si existe: Retorna error 400 "Archivo duplicado"
4. No se procesa ni se guarda

Esto previene duplicados de datos.

---

### **P: ¿Puedo cancelar un procesamiento en curso?**

**R:** Sí, pero hay limitaciones:

```bash
# Opción 1: Purgar toda la cola Celery
celery -A app.celery_app purge

# Opción 2: Cancelar tarea específica
celery -A app.celery_app revoke <task_id>

# Nota: Los registros ya insertados quedan en BD
# El estado del archivo quedará en "procesando"
```

---

### **P: ¿Qué formatos de archivo soporta?**

**R:** Actualmente:
- ✅ **CSV** (implementado)
- ⏳ **XML** (pendiente)
- ⏳ **TXT** (pendiente)

Para XML y TXT falta implementar parsers adicionales en `procesador_service.py`

---

### **P: ¿Dónde se guardan los archivos?**

**R:** En la carpeta configurada en `.env`:
```python
UPLOAD_DIR = "./uploads"  # Backend/uploads
```

Con Docker Compose:
- Los archivos se guardan en volumen `uploads_data`
- Persisten incluso si se reinicia el contenedor

---

### **P: ¿Qué pasa si la BD se cae durante procesamiento?**

**R:** Malas noticias:
1. Registros parcialmente insertados quedan en BD
2. Archivo queda en estado "procesando" indefinidamente
3. Se pierden los registros no committeados

**Solución:**
- Celery reintentos automáticos (configurable)
- Monitoreo de BD con health checks
- Backups regulares

---

### **P: ¿Es necesario Redis para que funcione?**

**R:** No es obligatorio:
- Si Redis está **disponible**: Celery encola tareas asincronamente
- Si Redis **no funciona**: El sistema procesa de forma sincrónica en el API

Esto está manejado en `archivos.py`:
```python
def _encolar_o_procesar_sync(archivo_id, ruta_archivo):
    try:
        procesar_archivo_task.delay(...)  # Async con Celery
    except Exception:
        procesar_archivo(db, archivo_id, ruta_archivo)  # Sync
```

---

### **P: ¿Cómo agrego un nuevo tipo de autoconsumo?**

**R:** 3 pasos:

1. **Actualizar validador** (`backend/app/utils/validators.py`):
```python
TIPOS_AUTOCONSUMO_VALIDOS = {12, 41, 42, 43, 51, 99}  # Agregar 99
```

2. **Agregar en BD** (migración Alembic):
```sql
INSERT INTO tipo_autoconsumo (codigo, descripcion, activo) 
VALUES (99, 'Nuevo tipo', true);
```

3. **Actualizar constraint BD**:
```sql
ALTER TABLE tipo_autoconsumo 
DROP CONSTRAINT ck_tipos_validos;

ALTER TABLE tipo_autoconsumo 
ADD CONSTRAINT ck_tipos_validos 
CHECK (codigo IN (12, 41, 42, 43, 51, 99));
```

---

### **P: ¿Cómo exporto datos a Excel?**

**R:** Actualmente no hay endpoint directo. Opciones:

1. **Via API**: Obtén JSON y convierte con librería Python
```python
import pandas as pd
import requests

resp = requests.get("http://localhost:8000/api/v1/energia")
df = pd.json_normalize(resp.json()['registros'])
df.to_excel("energía.xlsx", index=False)
```

2. **Directo BD**: Query SQL + pgadmin export

3. **Agregar endpoint**: Backend endpoint GET /api/v1/energia/export/excel

---

### **P: ¿Cómo auténtico usuarios?**

**R:** Actualmente **sin autenticación**. Implementación pendiente:

En `backend/app/api/routes/auth.py` (comentado) hay esqueleto:
```python
# - JWT tokens
# - Login endpoint
# - Refresh tokens
# - Logout
```

Pasos para implementar:
1. Descomentar rutas en `auth.py`
2. Implementar `utils/auth.py` con JWT
3. Agregar middleware en `main.py`
4. Actualizar `archivos.py` para usar usuario autenticado

---

### **P: ¿Cómo delego tareas a múltiples workers?**

**R:** Docker Compose ya está preparado:

```yaml
# docker-compose.yml actual
worker:
  ...
  command: celery -A app.celery_app worker -l info
```

Para escalar:
```bash
# Crear 3 workers (en Docker)
docker-compose up -d --scale worker=3

# Ver estado
docker-compose ps

# Con Kubernetes automático
```

---

### **P: ¿Cómo monitorieau mi sistema en producción?**

**R:** Opciones:

1. **Prometheus + Grafana**
   - Métricas de CPU, RAM, request count
   - Dashboards en vivo

2. **ELK Stack** (Elasticsearch, Logstash, Kibana)
   - Logs centralizados
   - Búsqueda y análisis

3. **Sentry**
   - Captura errores automáticos
   - Alertas

4. **DataDog / New Relic**
   - Monitoreo integral
   - Pero de pago

Configuración recomendada (development → production):
```python
# app/main.py
if settings.ENVIRONMENT == "production":
    # Agregar middleware de monitoreo
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", handle_metrics)
```

---

### **P: ¿Cuál es el límite máximo de registros por archivo?**

**R:** Teóricamente **ilimitado**, limitaciones prácticas:

| Factor | Límite |
|--------|--------|
| Tamaño archivo | 100 MB (configurable) |
| Memoria RAM | Depende servidor |
| Tiempo procesamiento | ~ 1 minuto por 10k registros |
| BD storage | Depende PostgreSQL |

**Recomendación**: < 100k registros por archivo para mejor rendimiento.

---

### **P: ¿Cómo genero un reporte de errores?**

**R:** SQL query + export:

```sql
-- Errores por tipo
SELECT 
  tipo_error,
  COUNT(*) as cantidad,
  COUNT(*) * 100.0 / (SELECT COUNT(*) FROM registro_errores) as porcentaje
FROM registro_errores
GROUP BY tipo_error
ORDER BY cantidad DESC;

-- Errores por archivo
SELECT 
  a.id,
  a.nombre_archivo,
  COUNT(e.id) as total_errores
FROM archivo_procesado a
LEFT JOIN registro_errores e ON a.id = e.archivo_id
WHERE a.estado = 'completado'
GROUP BY a.id
ORDER BY total_errores DESC;
```

O via API + procesamiento:
```bash
curl http://localhost:8000/api/v1/errores | jq '.' > errores.json
```

---

### **P: ¿Cómo backupeo la BD?**

**R:** PostgreSQL backup:

```bash
# Backup completo (dump)
docker-compose exec postgres pg_dump -U postgres energy_process > backup.sql

# Restaurar
docker-compose exec -T postgres psql -U postgres energy_process < backup.sql

# Backup automatizado (cron)
0 2 * * * docker-compose -f /ruta/docker-compose.yml exec -T postgres \
  pg_dump -U postgres energy_process > /backups/db_$(date +\%Y\%m\%d).sql
```

---

### **P: ¿Cómo agrego validaciones personalizadas?**

**R:** Crear función en `backend/app/utils/validators.py`:

```python
def validar_campo_personalizado(valor: str) -> bool:
    """Tu lógica aquí"""
    return True or False

# Luego usar en procesador_service.py
def validar_linea(row, num_linea, db):
    errores = []
    
    if not validar_campo_personalizado(row.get("campo")):
        errores.append(("validacion_personalizada", "Descripción error"))
    
    return errores
```

También agregar constraint BD (opcional):
```sql
ALTER TABLE tipo_autoconsumo 
ADD CONSTRAINT ck_campo_valido CHECK (campo ~ '^[0-9]{3}$');
```

---

### **P: ¿Cómo testeo localmente sin Docker?**

**R:** Setup local completo:

```bash
# 1. PostgreSQL local
brew install postgresql  # o: apt install postgresql

# 2. Redis local
brew install redis  # o: apt install redis

# 3. Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 4. Worker
celery -A app.celery_app worker -l info

# 5. Frontend
cd frontend
npm install
npm run dev
```

Requisitos `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/energy_test
REDIS_URL=redis://localhost:6379/0
```

---

### **P: ¿Qué IDE recomiendan?**

**R:** Opciones:

| IDE | Lenguaje | Características |
|-----|----------|-----------------|
| **VS Code** | Python + JS | ✅ Ligero, extensiones, debug |
| **PyCharm** | Python | ✅ Profesional, autocompletar |
| **WebStorm** | JS/React | ✅ JS avanzado |
| **Vim** | Todo | ✅ Rápido, curva aprendizaje |

**Recomendación**: VS Code + Python Extension + Prettier

---

## 🆘 TROUBLESHOOTING

### Problema: `ModuleNotFoundError: No module named 'fastapi'`

**Solución:**
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Problema: `Connection refused (PostgreSQL)`

**Solución:**
```bash
# Ver si PostgreSQL está corriendo
docker-compose ps

# Iniciar si no está
docker-compose up -d postgres

# Esperar 10 segundos

# Reiniciar backend
docker-compose restart backend
```

### Problema: `Redis connection timeout`

**Solución:**
```bash
# Ver si Redis está corriendo
docker-compose ps redis

# Si no está
docker-compose up -d redis

# Probar conexión
docker-compose exec redis redis-cli PING
```

### Problema: `CORS error` (401, 403)

**Solución:**
```python
# backend/app/config.py
CORS_ORIGINS = "http://localhost:3000,http://localhost:5173,http://localhost"

# Y reiniciar backend
docker-compose restart backend
```

### Problema: `Port already in use (port 8000)`

**Solución:**
```bash
# Encontrar proceso
lsof -i :8000  # macOS/Linux
netstat -ano | grep :8000  # Windows

# Matar proceso
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# O cambiar puerto en docker-compose.yml
# ports: ["9000:8000"]
```

### Problema: `Worker no procesa archivos`

**Diagnóstico:**
```bash
# Ver si worker está activo
celery -A app.celery_app inspect active

# Ver tareas en cola
celery -A app.celery_app inspect reserved

# Ver errores del worker
docker-compose logs -f worker

# Reiniciar worker
docker-compose restart worker
```

---

## 📞 SOPORTE

- **Documentación**: Lee `README_COMPLETO.md`
- **Diagramas**: Ver `DIAGRAMAS_TECNICOS.md`
- **Código**: Comenta el código fuente
- **Issues**: Crear en GitHub
- **Questions**: Contactar al equipo

---

**Última actualización**: Febrero 2026
