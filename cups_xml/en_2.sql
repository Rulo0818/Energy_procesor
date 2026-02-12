-- Dump completo de la base de datos energy_process con tablas adicionales
-- Creado: 8 de febrero de 2026

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
-- SET xmloption content;
SET client_min_messages = warning;

-- ============================================================================
-- CREACIÓN DE EXTENSIONES
-- ============================================================================

-- CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;

-- COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';

-- ============================================================================
-- CREAR TABLAS
-- ============================================================================

-- Tabla: usuario
CREATE TABLE public.usuario (
    id integer NOT NULL,
    username character varying(100) NOT NULL UNIQUE,
    email character varying(255) NOT NULL UNIQUE,
    password_hash character varying(255) NOT NULL,
    nombre_completo character varying(255) NOT NULL,
    rol character varying(20) DEFAULT 'operador'::character varying NOT NULL,
    activo boolean DEFAULT true,
    fecha_registro timestamp without time zone DEFAULT now() NOT NULL,
    ultima_sesion timestamp without time zone,
    CONSTRAINT ck_rol CHECK (((rol)::text = ANY ((ARRAY['admin'::character varying, 'operador'::character varying, 'consultor'::character varying])::text[])))
);

DROP TABLE IF EXISTS public.usuario;
CREATE TABLE public.usuario (
    id integer NOT NULL,
    username character varying(100) NOT NULL UNIQUE,
    email character varying(255) NOT NULL UNIQUE,
    password_hash character varying(255) NOT NULL,
    nombre_completo character varying(255) NOT NULL,
    rol character varying(20) DEFAULT 'operador'::character varying NOT NULL,
    activo boolean DEFAULT true,
    fecha_registro timestamp without time zone DEFAULT now() NOT NULL,
    ultima_sesion timestamp without time zone,
    CONSTRAINT ck_rol CHECK (((rol)::text = ANY ((ARRAY['admin'::character varying, 'operador'::character varying, 'consultor'::character varying])::text[])))
);

CREATE SEQUENCE public.usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.usuario_id_seq OWNED BY public.usuario.id;

ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);

-- Tabla: cliente
CREATE TABLE public.cliente (
    id integer NOT NULL,
    cups character varying(20) NOT NULL UNIQUE,
    nombre_cliente character varying(255) NOT NULL,
    email character varying(255),
    telefono character varying(20),
    direccion text,
    municipio character varying(100),
    provincia character varying(100),
    codigo_postal character varying(5),
    activo boolean DEFAULT true,
    fecha_registro timestamp without time zone DEFAULT now() NOT NULL,
    fecha_actualizacion timestamp without time zone DEFAULT now() NOT NULL
);

CREATE SEQUENCE public.cliente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.cliente_id_seq OWNED BY public.cliente.id;

ALTER TABLE ONLY public.cliente ALTER COLUMN id SET DEFAULT nextval('public.cliente_id_seq'::regclass);

-- Tabla: tipo_autoconsumo
CREATE TABLE public.tipo_autoconsumo (
    codigo integer NOT NULL,
    descripcion character varying(255) NOT NULL,
    activo boolean DEFAULT true,
    CONSTRAINT ck_tipos_validos CHECK ((codigo = ANY (ARRAY[12, 41, 42, 43, 51])))
);

-- Tabla: archivo_procesado (MODIFICADA)
CREATE TABLE public.archivo_procesado (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    nombre_archivo character varying(255) NOT NULL,
    hash_archivo character(64) NOT NULL,
    fecha_carga timestamp without time zone DEFAULT now() NOT NULL,
    fecha_procesamiento timestamp without time zone,
    estado character varying(20) DEFAULT 'pendiente'::character varying NOT NULL,
    total_registros integer DEFAULT 0,
    registros_exitosos integer DEFAULT 0,
    registros_con_error integer DEFAULT 0,
    ruta_archivo text,
    CONSTRAINT ck_estado CHECK (((estado)::text = ANY ((ARRAY['pendiente'::character varying, 'procesando'::character varying, 'completado'::character varying, 'error'::character varying])::text[])))
);

CREATE SEQUENCE public.archivo_procesado_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.archivo_procesado_id_seq OWNED BY public.archivo_procesado.id;

ALTER TABLE ONLY public.archivo_procesado ALTER COLUMN id SET DEFAULT nextval('public.archivo_procesado_id_seq'::regclass);

-- Tabla: energia_excedentaria (MODIFICADA)
CREATE TABLE public.energia_excedentaria (
    id integer NOT NULL,
    archivo_id integer NOT NULL,
    cliente_id integer NOT NULL,
    linea_archivo integer NOT NULL,
    instalacion_gen character varying(50) NOT NULL,
    fecha_desde date NOT NULL,
    fecha_hasta date NOT NULL,
    tipo_autoconsumo integer NOT NULL,
    energia_neta_gen numeric(12,3)[] NOT NULL,
    energia_autoconsumida numeric(12,3)[] NOT NULL,
    pago_tda numeric(12,2)[] NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_energia_autoconsumida_len CHECK ((array_length(energia_autoconsumida, 1) = 24)),
    CONSTRAINT ck_energia_neta_gen_len CHECK ((array_length(energia_neta_gen, 1) = 24)),
    CONSTRAINT ck_fechas_validas CHECK ((fecha_hasta >= fecha_desde)),
    CONSTRAINT ck_pago_tda_len CHECK ((array_length(pago_tda, 1) = 24))
);

CREATE SEQUENCE public.energia_excedentaria_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.energia_excedentaria_id_seq OWNED BY public.energia_excedentaria.id;

ALTER TABLE ONLY public.energia_excedentaria ALTER COLUMN id SET DEFAULT nextval('public.energia_excedentaria_id_seq'::regclass);

-- Tabla: registro_errores
CREATE TABLE public.registro_errores (
    id integer NOT NULL,
    archivo_id integer NOT NULL,
    linea_archivo integer NOT NULL,
    tipo_error character varying(50) NOT NULL,
    descripcion text NOT NULL,
    datos_linea text,
    fecha_registro timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_tipo_error CHECK (((tipo_error)::text = ANY ((ARRAY['cliente_inexistente'::character varying, 'tipo_no_soportado'::character varying, 'formato_invalido'::character varying, 'archivo_duplicado'::character varying, 'inconsistencia_numerica'::character varying, 'array_longitud_invalida'::character varying, 'fecha_invalida'::character varying])::text[])))
);

CREATE SEQUENCE public.registro_errores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.registro_errores_id_seq OWNED BY public.registro_errores.id;

ALTER TABLE ONLY public.registro_errores ALTER COLUMN id SET DEFAULT nextval('public.registro_errores_id_seq'::regclass);

-- ============================================================================
-- AGREGAR CONSTRAINTS (PRIMARY KEYS)
-- ============================================================================

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.tipo_autoconsumo
    ADD CONSTRAINT tipo_autoconsumo_pkey PRIMARY KEY (codigo);

ALTER TABLE ONLY public.archivo_procesado
    ADD CONSTRAINT archivo_procesado_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.energia_excedentaria
    ADD CONSTRAINT energia_excedentaria_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.registro_errores
    ADD CONSTRAINT registro_errores_pkey PRIMARY KEY (id);

-- ============================================================================
-- AGREGAR UNIQUE CONSTRAINTS
-- ============================================================================

ALTER TABLE ONLY public.archivo_procesado
    ADD CONSTRAINT uq_hash UNIQUE (hash_archivo);

ALTER TABLE ONLY public.archivo_procesado
    ADD CONSTRAINT uq_nombre_fecha UNIQUE (nombre_archivo, fecha_carga);

ALTER TABLE ONLY public.energia_excedentaria
    ADD CONSTRAINT uq_archivo_cups_instalacion UNIQUE (archivo_id, cliente_id, instalacion_gen, fecha_desde);

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT uq_cliente_cups UNIQUE (cups);

-- ============================================================================
-- CREAR ÍNDICES
-- ============================================================================

CREATE INDEX idx_archivo_estado ON public.archivo_procesado USING btree (estado);
CREATE INDEX idx_archivo_fecha_carga ON public.archivo_procesado USING btree (fecha_carga DESC);
CREATE INDEX idx_archivo_nombre ON public.archivo_procesado USING btree (nombre_archivo);
CREATE INDEX idx_archivo_usuario ON public.archivo_procesado USING btree (usuario_id);

CREATE INDEX idx_energia_archivo ON public.energia_excedentaria USING btree (archivo_id);
CREATE INDEX idx_energia_cliente ON public.energia_excedentaria USING btree (cliente_id);
CREATE INDEX idx_energia_fechas ON public.energia_excedentaria USING btree (fecha_desde, fecha_hasta);
CREATE INDEX idx_energia_tipo ON public.energia_excedentaria USING btree (tipo_autoconsumo);
CREATE INDEX idx_energia_instalacion ON public.energia_excedentaria USING btree (instalacion_gen);

CREATE INDEX idx_error_archivo ON public.registro_errores USING btree (archivo_id);
CREATE INDEX idx_error_tipo ON public.registro_errores USING btree (tipo_error);
CREATE INDEX idx_error_linea ON public.registro_errores USING btree (archivo_id, linea_archivo);

CREATE INDEX idx_cliente_activo ON public.cliente USING btree (activo);
CREATE INDEX idx_cliente_municipio ON public.cliente USING btree (municipio);

CREATE INDEX idx_usuario_activo ON public.usuario USING btree (activo);
CREATE INDEX idx_usuario_rol ON public.usuario USING btree (rol);

-- ============================================================================
-- AGREGAR FOREIGN KEYS
-- ============================================================================

ALTER TABLE ONLY public.archivo_procesado
    ADD CONSTRAINT archivo_procesado_usuario_id_fkey 
    FOREIGN KEY (usuario_id) REFERENCES public.usuario(id) ON DELETE RESTRICT;

ALTER TABLE ONLY public.energia_excedentaria
    ADD CONSTRAINT energia_excedentaria_archivo_id_fkey 
    FOREIGN KEY (archivo_id) REFERENCES public.archivo_procesado(id) ON DELETE CASCADE;

ALTER TABLE ONLY public.energia_excedentaria
    ADD CONSTRAINT energia_excedentaria_cliente_id_fkey 
    FOREIGN KEY (cliente_id) REFERENCES public.cliente(id) ON DELETE RESTRICT;

ALTER TABLE ONLY public.energia_excedentaria
    ADD CONSTRAINT energia_excedentaria_tipo_autoconsumo_fkey 
    FOREIGN KEY (tipo_autoconsumo) REFERENCES public.tipo_autoconsumo(codigo);

ALTER TABLE ONLY public.registro_errores
    ADD CONSTRAINT registro_errores_archivo_id_fkey 
    FOREIGN KEY (archivo_id) REFERENCES public.archivo_procesado(id) ON DELETE CASCADE;

-- ============================================================================
-- INSERTAR DATOS INICIALES
-- ============================================================================

-- Insertar tipos de autoconsumo
INSERT INTO public.tipo_autoconsumo (codigo, descripcion, activo) VALUES
(12, 'Autoconsumo tipo 12', true),
(41, 'Autoconsumo tipo 41', true),
(42, 'Autoconsumo tipo 42', true),
(43, 'Autoconsumo tipo 43', true),
(51, 'Autoconsumo tipo 51', true)
ON CONFLICT (codigo) DO NOTHING;

-- ============================================================================
-- INSERTAR USUARIOS
-- ============================================================================

INSERT INTO public.usuario (username, email, password_hash, nombre_completo, rol, activo)
VALUES 
('admin', 'admin@energy-process.local', 'admin123', 'Administrador Sistema', 'admin', true),
('sitko', 'sitko@energy-process.local', 'sitko123', 'Sitko Operador', 'operador', true),
('juan.garcia', 'juan.garcia@energy-process.local', 'juan123', 'Juan García López', 'operador', true),
('maria.lopez', 'maria.lopez@energy-process.local', 'maria123', 'María López Rodríguez', 'operador', true),
('consultor.energy', 'consultor@energy-process.local', 'consul123', 'Consultor Energético', 'consultor', true)
ON CONFLICT (username) DO NOTHING;

-- ============================================================================
-- INSERTAR CLIENTES
-- ============================================================================

INSERT INTO public.cliente (cups, nombre_cliente, email, telefono, direccion, municipio, provincia, codigo_postal, activo)
VALUES 
('ES0031405004ZZ8T0Z', 'Empresa Solar Madrid S.L.', 'contacto@solarmadrid.es', '914567890', 'Calle Principal 123', 'Madrid', 'Madrid', '28001', true),
('ES0031405004ZZ8T0Y', 'Generadora Sostenible SPA', 'info@generadora.es', '916234567', 'Avenida Central 456', 'Madrid', 'Madrid', '28002', true),
('ES0031405004ZZ8T0X', 'Energía Renovable Iberia', 'admin@energia-renovable.es', '918901234', 'Calle Verde 789', 'Madrid', 'Madrid', '28003', true),
('ES0031405004ZZ8T0W', 'Autoconsumo Plus SL', 'contacto@autoconsumplus.es', '912345678', 'Plaza Mayor 321', 'Madrid', 'Madrid', '28004', true),
('ES0031405004ZZ8T0V', 'GreenPower Soluciones', 'info@greenpower.es', '913456789', 'Paseo del Prado 654', 'Madrid', 'Madrid', '28005', true),
('ES0031405004ZZ8T0U', 'Instalaciones Fotovoltaicas España', 'venta@instalaciones-fv.es', '914567890', 'Calle del Comercio 987', 'Madrid', 'Madrid', '28006', true),
('ES0031405004ZZ8T0T', 'Solar Energía Industrial', 'industrial@solarenergia.es', '915678901', 'Polígono Industrial 12', 'Madrid', 'Madrid', '28007', true),
('ES0031405004ZZ8T0S', 'Distribuidora de Energía Solar', 'dist@energiasolar.es', '916789012', 'Avenida del Futuro 345', 'Madrid', 'Madrid', '28008', true),
('ES0031405004ZZ8T0R', 'Proyecto Verde Energías', 'contacto@proyectoverde.es', '917890123', 'Calle Sostenible 678', 'Madrid', 'Madrid', '28009', true),
('ES0031405004ZZ8T0Q', 'NextGen Fotovoltaica', 'info@nextgen-fv.es', '918901234', 'Carrera de la Energía 111', 'Madrid', 'Madrid', '28010', true)
ON CONFLICT (cups) DO NOTHING;

-- ============================================================================
-- INSERTAR ARCHIVOS PROCESADOS (PRUEBA)
-- ============================================================================

INSERT INTO public.archivo_procesado (usuario_id, nombre_archivo, hash_archivo, fecha_carga, fecha_procesamiento, estado, total_registros, registros_exitosos, registros_con_error, ruta_archivo)
SELECT 
    u.id,
    'carga_energia_enero_2025.xml',
    'e1c4d8f9a7b2c3d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c',
    NOW() - INTERVAL '5 days',
    NOW() - INTERVAL '4 days',
    'completado',
    3,
    3,
    0,
    '/uploads/carga_energia_enero_2025.xml'
FROM public.usuario u WHERE u.username = 'sitko'
ON CONFLICT (hash_archivo) DO NOTHING;

INSERT INTO public.archivo_procesado (usuario_id, nombre_archivo, hash_archivo, fecha_carga, fecha_procesamiento, estado, total_registros, registros_exitosos, registros_con_error, ruta_archivo)
SELECT 
    u.id,
    'registros_febrero_2025.xml',
    'f2d5e9a0b3c4d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d',
    NOW() - INTERVAL '2 days',
    NOW() - INTERVAL '1 day',
    'completado',
    5,
    4,
    1,
    '/uploads/registros_febrero_2025.xml'
FROM public.usuario u WHERE u.username = 'juan.garcia'
ON CONFLICT (hash_archivo) DO NOTHING;

INSERT INTO public.archivo_procesado (usuario_id, nombre_archivo, hash_archivo, fecha_carga, fecha_procesamiento, estado, total_registros, registros_exitosos, registros_con_error, ruta_archivo)
SELECT 
    u.id,
    'datos_marzo_energia.xml',
    'a3b6f0c1d4e5f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1',
    NOW() - INTERVAL '1 day',
    NULL,
    'procesando',
    2,
    0,
    0,
    '/uploads/datos_marzo_energia.xml'
FROM public.usuario u WHERE u.username = 'maria.lopez'
ON CONFLICT (hash_archivo) DO NOTHING;

-- ============================================================================
-- INSERTAR DATOS DE ENERGÍA EXCEDENTARIA
-- ============================================================================

INSERT INTO public.energia_excedentaria (
    archivo_id, cliente_id, linea_archivo, instalacion_gen, fecha_desde, fecha_hasta, 
    tipo_autoconsumo, energia_neta_gen, energia_autoconsumida, pago_tda
)
SELECT
    ap.id,
    c.id,
    1,
    'GEN-MAD-001',
    '2025-01-01'::date,
    '2025-01-31'::date,
    41,
    '{150.25, 155.30, 160.15, 158.45, 162.10, 165.80, 170.25, 168.90, 172.35, 175.60, 171.45, 169.75, 173.20, 176.40, 174.65, 170.30, 167.85, 165.50, 162.20, 158.75, 155.40, 152.15, 150.80, 148.45}'::numeric(12,3)[],
    '{140.10, 145.20, 148.75, 146.30, 150.80, 153.50, 158.10, 156.60, 160.20, 163.40, 159.30, 157.65, 161.00, 164.20, 162.40, 158.15, 155.70, 153.35, 150.10, 146.60, 143.30, 140.05, 138.60, 136.25}'::numeric(12,3)[],
    '{12.50, 13.20, 14.15, 13.85, 14.65, 15.35, 16.10, 15.75, 16.50, 17.25, 16.80, 16.35, 17.00, 17.75, 17.40, 16.90, 16.25, 15.65, 15.00, 14.40, 13.85, 13.25, 12.90, 12.45}'::numeric(12,2)[]
FROM public.archivo_procesado ap
JOIN public.cliente c ON c.cups = 'ES0031405004ZZ8T0Z'
WHERE ap.nombre_archivo = 'carga_energia_enero_2025.xml'
ON CONFLICT (archivo_id, cliente_id, instalacion_gen, fecha_desde) DO NOTHING;

INSERT INTO public.energia_excedentaria (
    archivo_id, cliente_id, linea_archivo, instalacion_gen, fecha_desde, fecha_hasta, 
    tipo_autoconsumo, energia_neta_gen, energia_autoconsumida, pago_tda
)
SELECT
    ap.id,
    c.id,
    2,
    'GEN-MAD-002',
    '2025-01-01'::date,
    '2025-01-31'::date,
    42,
    '{120.50, 125.75, 130.20, 128.65, 135.10, 140.35, 145.60, 142.25, 148.85, 152.40, 149.75, 147.30, 151.95, 156.20, 153.60, 149.15, 145.70, 142.05, 138.55, 135.20, 131.80, 128.45, 125.90, 122.35}'::numeric(12,3)[],
    '{110.30, 115.40, 120.10, 118.45, 125.50, 130.60, 135.75, 132.40, 138.95, 142.50, 139.85, 137.40, 142.05, 146.30, 143.70, 139.25, 135.80, 132.15, 128.65, 125.30, 121.90, 118.55, 116.00, 112.45}'::numeric(12,3)[],
    '{10.25, 10.85, 11.50, 11.20, 12.00, 12.85, 13.60, 13.20, 14.00, 14.75, 14.30, 13.95, 14.60, 15.35, 15.00, 14.50, 13.95, 13.50, 13.05, 12.60, 12.15, 11.75, 11.40, 11.00}'::numeric(12,2)[]
FROM public.archivo_procesado ap
JOIN public.cliente c ON c.cups = 'ES0031405004ZZ8T0Y'
WHERE ap.nombre_archivo = 'carga_energia_enero_2025.xml'
ON CONFLICT (archivo_id, cliente_id, instalacion_gen, fecha_desde) DO NOTHING;

INSERT INTO public.energia_excedentaria (
    archivo_id, cliente_id, linea_archivo, instalacion_gen, fecha_desde, fecha_hasta, 
    tipo_autoconsumo, energia_neta_gen, energia_autoconsumida, pago_tda
)
SELECT
    ap.id,
    c.id,
    3,
    'GEN-MAD-003',
    '2025-01-15'::date,
    '2025-02-14'::date,
    51,
    '{200.00, 205.50, 210.25, 208.75, 215.30, 220.65, 225.90, 222.40, 228.75, 232.50, 229.85, 227.20, 231.95, 236.40, 233.75, 229.30, 225.65, 221.95, 218.35, 214.75, 211.15, 207.60, 204.95, 202.25}'::numeric(12,3)[],
    '{185.50, 190.80, 195.40, 193.95, 200.20, 205.35, 210.50, 207.15, 213.40, 217.20, 214.60, 212.00, 216.75, 221.15, 218.50, 214.10, 210.45, 206.80, 203.20, 199.60, 196.05, 192.50, 189.90, 187.30}'::numeric(12,3)[],
    '{18.50, 19.25, 20.10, 19.75, 20.65, 21.50, 22.35, 21.95, 22.85, 23.75, 23.30, 22.85, 23.60, 24.50, 24.05, 23.50, 22.95, 22.40, 21.85, 21.30, 20.80, 20.30, 19.85, 19.40}'::numeric(12,2)[]
FROM public.archivo_procesado ap
JOIN public.cliente c ON c.cups = 'ES0031405004ZZ8T0X'
WHERE ap.nombre_archivo = 'carga_energia_enero_2025.xml'
ON CONFLICT (archivo_id, cliente_id, instalacion_gen, fecha_desde) DO NOTHING;

-- ============================================================================
-- INSERTAR ERRORES DE PROCESAMIENTO
-- ============================================================================

INSERT INTO public.registro_errores (archivo_id, linea_archivo, tipo_error, descripcion, datos_linea)
SELECT
    ap.id,
    2,
    'formato_invalido',
    'El formato de energía neta generada no es válido. Se esperaba un array de 24 elementos numéricos.',
    'energiaNetaGen: [150.25, 155.30, INVALIDO, 158.45]'
FROM public.archivo_procesado ap
WHERE ap.nombre_archivo = 'registros_febrero_2025.xml'
ON CONFLICT DO NOTHING;

INSERT INTO public.registro_errores (archivo_id, linea_archivo, tipo_error, descripcion, datos_linea)
SELECT
    ap.id,
    4,
    'tipo_no_soportado',
    'Tipo de autoconsumo 99 no es soportado. Tipos válidos: 12, 41, 42, 43, 51',
    'tipoAutoconsumo: 99'
FROM public.archivo_procesado ap
WHERE ap.nombre_archivo = 'registros_febrero_2025.xml'
ON CONFLICT DO NOTHING;

INSERT INTO public.registro_errores (archivo_id, linea_archivo, tipo_error, descripcion, datos_linea)
SELECT
    ap.id,
    5,
    'fecha_invalida',
    'La fecha_hasta es anterior a fecha_desde. Rango de fechas inválido.',
    'fechaDesde: 2025-02-15, fechaHasta: 2025-02-10'
FROM public.archivo_procesado ap
WHERE ap.nombre_archivo = 'registros_febrero_2025.xml'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- ASIGNAR PERMISOS A USUARIO sitko
-- ============================================================================

GRANT ALL PRIVILEGES ON DATABASE energy_process TO sitko;
GRANT ALL ON SCHEMA public TO sitko;
GRANT ALL ON ALL TABLES IN SCHEMA public TO sitko;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO sitko;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO sitko;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO sitko;

-- ============================================================================
-- INFORMACIÓN DE ESTRUCTURA
-- ============================================================================

/*
TABLAS CREADAS:
===============

1. usuario
   - id (PK, INT)
   - username (VARCHAR, UNIQUE)
   - email (VARCHAR, UNIQUE)
   - password_hash (VARCHAR)
   - nombre_completo (VARCHAR)
   - rol (VARCHAR: admin, operador, consultor)
   - activo (BOOLEAN)
   - fecha_registro (TIMESTAMP)
   - ultima_sesion (TIMESTAMP)

2. cliente
   - id (PK, INT)
   - cups (VARCHAR, UNIQUE)
   - nombre_cliente (VARCHAR)
   - email (VARCHAR)
   - telefono (VARCHAR)
   - direccion (TEXT)
   - municipio (VARCHAR)
   - provincia (VARCHAR)
   - codigo_postal (VARCHAR)
   - activo (BOOLEAN)
   - fecha_registro (TIMESTAMP)
   - fecha_actualizacion (TIMESTAMP)

3. tipo_autoconsumo
   - codigo (PK, INT: 12, 41, 42, 43, 51)
   - descripcion (VARCHAR)
   - activo (BOOLEAN)

4. archivo_procesado (MODIFICADA)
   - id (PK, INT)
   - usuario_id (FK → usuario.id)
   - nombre_archivo (VARCHAR)
   - hash_archivo (CHAR 64)
   - fecha_carga (TIMESTAMP)
   - fecha_procesamiento (TIMESTAMP)
   - estado (VARCHAR: pendiente, procesando, completado, error)
   - total_registros (INT)
   - registros_exitosos (INT)
   - registros_con_error (INT)
   - ruta_archivo (TEXT)

5. energia_excedentaria (MODIFICADA)
   - id (PK, INT)
   - archivo_id (FK → archivo_procesado.id)
   - cliente_id (FK → cliente.id)
   - linea_archivo (INT)
   - instalacion_gen (VARCHAR)
   - fecha_desde (DATE)
   - fecha_hasta (DATE)
   - tipo_autoconsumo (FK → tipo_autoconsumo.codigo)
   - energia_neta_gen (NUMERIC ARRAY[24])
   - energia_autoconsumida (NUMERIC ARRAY[24])
   - pago_tda (NUMERIC ARRAY[24])
   - fecha_creacion (TIMESTAMP)

6. registro_errores
   - id (PK, INT)
   - archivo_id (FK → archivo_procesado.id)
   - linea_archivo (INT)
   - tipo_error (VARCHAR)
   - descripcion (TEXT)
   - datos_linea (TEXT)
   - fecha_registro (TIMESTAMP)

CAMBIOS PRINCIPALES:
====================
✓ Agregadas tablas usuario y cliente
✓ Modificada archivo_procesado con FK a usuario
✓ Modificada energia_excedentaria con FK a cliente
✓ Actualizado array_length a 24 horas (en lugar de 6)
✓ Agregados índices para optimizar búsquedas
✓ Usuarios por defecto: admin, sitko
✓ Permisos asignados a sitko

USUARIOS POR DEFECTO:
=====================
Username: admin
Email: admin@energy-process.local
Contraseña: admin123
Rol: admin

Username: sitko
Email: sitko@energy-process.local
Contraseña: sitko123
Rol: operador
*/
