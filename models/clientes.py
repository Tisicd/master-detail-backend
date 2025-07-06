from .db import get_db_connection

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

# POST /api/clientes
def crear_cliente(data):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO clientes (
            codigo, nombres, apellidos, tipo_documento, numero_documento,
            tipo_cliente, razon_social, estado, observaciones
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        data["codigo"],
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
    cur.execute("""
        UPDATE clientes SET
            codigo = %s,
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
        data["codigo"],
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