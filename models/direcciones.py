from .db import get_db_connection

# 🔹 Obtener direcciones de un cliente
def obtener_direcciones_por_cliente(cliente_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            d.id,
            d.codigo_direccion,
            d.calle_principal,
            d.calle_secundaria,
            d.numero_casa,
            d.barrio,
            d.ciudad,
            d.provincia,
            d.zona,
            d.tipo_direccion,
            dd.referencia,
            dd.codigo_postal,
            dd.instrucciones_envio,
            dd.observaciones,
            TO_CHAR(dd.fecha_registro_direccion, 'YYYY-MM-DD') AS fecha_registro
        FROM direcciones d
        LEFT JOIN detalles_direccion dd ON dd.direccion_id = d.id
        WHERE d.cliente_id = %s
    """, (cliente_id,))
    columnas = [desc[0] for desc in cur.description]
    direcciones = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return direcciones

# 🔹 Crear dirección
def crear_direccion(data):
    conn = get_db_connection()
    cur = conn.cursor()

    # Insertar en direcciones
    cur.execute("""
        INSERT INTO direcciones (
            codigo_direccion, calle_principal, calle_secundaria, numero_casa, barrio,
            ciudad, provincia, zona, tipo_direccion, cliente_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        data["codigo_direccion"],
        data["calle_principal"],
        data.get("calle_secundaria"),
        data.get("numero_casa"),
        data.get("barrio"),
        data["ciudad"],
        data["provincia"],
        data.get("zona"),
        data["tipo_direccion"],
        data["cliente_id"]
    ))
    direccion_id = cur.fetchone()[0]

    # Insertar detalles
    cur.execute("""
        INSERT INTO detalles_direccion (
            direccion_id, referencia, codigo_postal,
            instrucciones_envio, observaciones, cliente_id
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        direccion_id,
        data.get("referencia"),
        data.get("codigo_postal"),
        data.get("instrucciones_envio"),
        data.get("observaciones"),
        data["cliente_id"]
    ))

    conn.commit()
    cur.close()
    conn.close()
    return direccion_id

# 🔹 Eliminar dirección (y detalles por cascade)
def eliminar_direccion(direccion_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM direcciones WHERE id = %s", (direccion_id,))
    conn.commit()
    cur.close()
    conn.close()

# 🔹 Actualizar dirección (y detalles)
def actualizar_direccion(direccion_id, data):
    conn = get_db_connection()
    cur = conn.cursor()

    # Actualizar tabla direcciones
    cur.execute("""
        UPDATE direcciones SET
            codigo_direccion = %s,
            calle_principal = %s,
            calle_secundaria = %s,
            numero_casa = %s,
            barrio = %s,
            ciudad = %s,
            provincia = %s,
            zona = %s,
            tipo_direccion = %s
        WHERE id = %s
    """, (
        data["codigo_direccion"],
        data["calle_principal"],
        data.get("calle_secundaria"),
        data.get("numero_casa"),
        data.get("barrio"),
        data["ciudad"],
        data["provincia"],
        data.get("zona"),
        data["tipo_direccion"],
        direccion_id
    ))

    # Actualizar detalles_direccion
    cur.execute("""
        UPDATE detalles_direccion SET
            referencia = %s,
            codigo_postal = %s,
            instrucciones_envio = %s,
            observaciones = %s
        WHERE direccion_id = %s
    """, (
        data.get("referencia"),
        data.get("codigo_postal"),
        data.get("instrucciones_envio"),
        data.get("observaciones"),
        direccion_id
    ))

    conn.commit()
    cur.close()
    conn.close()
