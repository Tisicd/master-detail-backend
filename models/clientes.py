from .db import get_db_connection

def validar_documento_ecuador(tipo, numero):
    tipo = tipo.strip().upper()
    numero = numero.strip()

    if not numero.isdigit():
        return False

    if tipo == "CÉDULA":
        return validar_cedula(numero)

    elif tipo == "RUC":
        return validar_ruc_natural(numero)

    return False

def validar_cedula(numero):
    if len(numero) != 10:
        return False

    provincia = int(numero[:2])
    if provincia < 1 or provincia > 24:
        return False

    tercer_digito = int(numero[2])
    if tercer_digito < 0 or tercer_digito > 5:
        return False

    coef = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0

    for i in range(9):
        val = int(numero[i]) * coef[i]
        if val >= 10:
            val -= 9
        suma += val

    residuo = suma % 10
    verificador = 0 if residuo == 0 else 10 - residuo

    return int(numero[9]) == verificador

def validar_ruc_natural(numero):
    if len(numero) != 13:
        return False

    if numero[10:] == "000":
        return False

    return validar_cedula(numero[:10])



# GET /api/clientes
def obtener_todos_los_clientes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            c.id, 
            c.codigo, 
            CONCAT(c.nombres, ' ', c.apellidos) AS nombre_completo,
            c.tipo_documento,
            c.numero_documento,
            c.tipo_cliente,
            c.razon_social,
            TO_CHAR(c.fecha_registro, 'YYYY-MM-DD') AS fecha_registro,
            c.estado,
            c.observaciones,

            -- Datos de contacto desde dirección principal
            d.telefono_principal,
            d.telefono_secundario,
            d.correo_electronico

        FROM clientes c
        LEFT JOIN direcciones d ON d.cliente_id = c.id AND d.tipo_direccion = 'Principal'
        ORDER BY c.id
    """)
    columnas = [desc[0] for desc in cur.description]
    clientes = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return clientes

# Inicializa la secuencia para códigos de cliente si no existe
def inicializar_secuencia_codigo_cliente():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'codigo_cliente_seq') THEN
                CREATE SEQUENCE codigo_cliente_seq START 1;
            END IF;
        END
        $$;
    """)
    conn.commit()
    cur.close()
    conn.close()

# Generador de código único para clientes
def generar_codigo_cliente():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT nextval('codigo_cliente_seq')")
    num = cur.fetchone()[0]
    cur.close()
    conn.close()
    return f"CLI{num:03d}"

# POST /api/clientes
def crear_cliente(data):
    conn = get_db_connection()
    cur = conn.cursor()

    if data["tipo_documento"] not in ("Cédula", "RUC"):
        cur.close()
        conn.close()
        raise ValueError("Tipo de documento inválido.")

    if not validar_documento_ecuador(data["tipo_documento"], data["numero_documento"]):
        cur.close()
        conn.close()
        raise ValueError(f"{data['tipo_documento']} inválido.")


# Validar número de documento único
    cur.execute("SELECT id FROM clientes WHERE numero_documento = %s", (data["numero_documento"],))
    if cur.fetchone():
        cur.close()
        conn.close()    
        raise ValueError("Ya existe un cliente con ese número de documento.")

# Generar código único para el nuevo cliente
    codigo_generado = generar_codigo_cliente()

    cur.execute("""
        INSERT INTO clientes (
            codigo, nombres, apellidos, tipo_documento, numero_documento,
            tipo_cliente, razon_social, estado, observaciones
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        codigo_generado,
        data["nombres"],
        data["apellidos"],
        data["tipo_documento"],
        data["numero_documento"],
        data["tipo_cliente"],
        data.get("razon_social"),
        data.get("estado", "Activo"),
        data.get("observaciones", "")
    ))

    nuevo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return nuevo_id

# GET /api/clientes/<id>
def obtener_cliente_por_id(cliente_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            id, 
            codigo, 
            nombres,
            apellidos,
            tipo_documento,
            numero_documento,
            tipo_cliente,
            razon_social,
            TO_CHAR(fecha_registro, 'YYYY-MM-DD') AS fecha_registro,
            estado,
            observaciones
        FROM clientes
        WHERE id = %s
    """, (cliente_id,))
    fila = cur.fetchone()
    columnas = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return dict(zip(columnas, fila)) if fila else None

# PUT /api/clientes/<id>
def actualizar_cliente(cliente_id, data):
    conn = get_db_connection()
    cur = conn.cursor()

    if data["tipo_documento"] not in ("Cédula", "RUC"):
        cur.close()
        conn.close()
        raise ValueError("Tipo de documento inválido.")

    if not validar_documento_ecuador(data["tipo_documento"], data["numero_documento"]):
        cur.close()
        conn.close()
        raise ValueError(f"{data['tipo_documento']} inválido.")

    cur.execute("""
    SELECT id FROM clientes 
    WHERE numero_documento = %s AND id != %s
    """, (data["numero_documento"], cliente_id))
    if cur.fetchone():
        cur.close()
        conn.close()
        raise ValueError("Ya existe otro cliente con ese número de documento.")

    cur.execute("""
        UPDATE clientes SET
            nombres = %s,
            apellidos = %s,
            tipo_documento = %s,
            numero_documento = %s,
            tipo_cliente = %s,
            razon_social = %s,
            estado = %s,
            observaciones = %s
        WHERE id = %s
    """, (
        data["nombres"],
        data["apellidos"],
        data["tipo_documento"],
        data["numero_documento"],
        data["tipo_cliente"],
        data.get("razon_social"),
        data.get("estado", "Activo"),
        data.get("observaciones", ""),
        cliente_id
    ))
    conn.commit()
    cur.close()
    conn.close()

# DELETE /api/clientes/<id>
def eliminar_cliente(cliente_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
    conn.commit()
    cur.close()
    conn.close()

# GET /api/clientes/buscar
def buscar_clientes(filtros):
    conn = get_db_connection()
    cur = conn.cursor()

    base_query = """
        SELECT 
            c.id, c.codigo,
            CONCAT(c.nombres, ' ', c.apellidos) AS nombre_completo,
            c.tipo_documento, c.numero_documento,
            c.tipo_cliente, c.razon_social,
            TO_CHAR(c.fecha_registro, 'YYYY-MM-DD') AS fecha_registro,
            c.estado, c.observaciones
        FROM clientes c
        WHERE 1=1
    """
    params = []

    if "nombre" in filtros:
        base_query += " AND (LOWER(c.nombres) LIKE %s OR LOWER(c.apellidos) LIKE %s)"
        search_term = f"%{filtros['nombre'].lower()}%"
        params.extend([search_term, search_term])

    if "numero_documento" in filtros:
        base_query += " AND c.numero_documento = %s"
        params.append(filtros["numero_documento"])

    if "estado" in filtros:
        base_query += " AND LOWER(c.estado) = %s"
        params.append(filtros["estado"].lower())

    base_query += " ORDER BY c.id"

    cur.execute(base_query, tuple(params))
    columnas = [desc[0] for desc in cur.description]
    resultados = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return resultados

