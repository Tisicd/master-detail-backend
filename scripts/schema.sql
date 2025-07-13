-- Secuencia para generación automática de códigos únicos de cliente
CREATE SEQUENCE IF NOT EXISTS codigo_cliente_seq START 1;

-- Tabla de usuarios (mantenida para autenticación)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL
);

-- Tabla Maestro: Clientes (según especificación)
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    tipo_documento VARCHAR(20) CHECK (tipo_documento IN ('Cédula', 'RUC')) NOT NULL,
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    tipo_cliente VARCHAR(20) CHECK (tipo_cliente IN ('Natural', 'Jurídico')) NOT NULL,
    razon_social VARCHAR(150),
    fecha_registro DATE DEFAULT CURRENT_DATE NOT NULL,
    estado VARCHAR(20) CHECK (estado IN ('Activo', 'Inactivo')) DEFAULT 'Activo' NOT NULL,
    observaciones TEXT
);

-- Tabla Detalle: Direcciones (con campos de contacto movidos aquí)
CREATE TABLE IF NOT EXISTS direcciones (
    id SERIAL PRIMARY KEY,
    codigo_direccion VARCHAR(20) UNIQUE NOT NULL,

    -- Información de ubicación
    calle_principal VARCHAR(150) NOT NULL,
    calle_secundaria VARCHAR(150),
    numero_casa VARCHAR(20) NOT NULL,
    barrio VARCHAR(100) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    provincia VARCHAR(100) NOT NULL,
    zona VARCHAR(20) CHECK (zona IN ('Urbana', 'Rural')) NOT NULL,
    codigo_postal VARCHAR(20),

    -- Información de contacto
    correo_electronico VARCHAR(100) NOT NULL,
    telefono_principal VARCHAR(20) NOT NULL,
    telefono_secundario VARCHAR(20),

    -- Información adicional
    referencia TEXT,
    tipo_direccion VARCHAR(50) CHECK (tipo_direccion IN ('Principal', 'Facturación', 'Envío', 'Oficina', 'Otro')) NOT NULL,
    instrucciones_envio TEXT,

    -- Relación con cliente
    cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    fecha_registro DATE DEFAULT CURRENT_DATE NOT NULL
);
