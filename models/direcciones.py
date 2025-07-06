from .db import get_db_connection

# 🔹 Obtener direcciones de un cliente
def obtener_direcciones_por_cliente(cliente_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            id,
            codigo_direccion,
            calle_principal,
            calle_secundaria,
            numero_casa,
            barrio,
            ciudad,
            provincia,
            zona,
            codigo_postal,
            correo_electronico,
            telefono_principal,
            telefono_secundario,
            referencia,
            tipo_direccion,
            instrucciones_envio,
            TO_CHAR(fecha_registro, 'YYYY-MM-DD') AS fecha_registro
        FROM direcciones
        WHERE cliente_id = %s
        ORDER BY tipo_direccion = 'Principal' DESC, id
    """, (cliente_id,))
    columnas = [desc[0] for desc in cur.description]
    direcciones = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return direcciones

# 🔹 Obtener una dirección específica por ID
def obtener_direccion_por_id(direccion_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            id,
            codigo_direccion,
            calle_principal,
            calle_secundaria,
            numero_casa,
            barrio,
            ciudad,
            provincia,
            zona,
            codigo_postal,
            correo_electronico,
            telefono_principal,
            telefono_secundario,
            referencia,
            tipo_direccion,
            instrucciones_envio,
            TO_CHAR(fecha_registro, 'YYYY-MM-DD') AS fecha_registro,
            cliente_id
        FROM direcciones
        WHERE id = %s
    """, (direccion_id,))
    fila = cur.fetchone()
    if not fila:
        cur.close()
        conn.close()
        return None
    
    columnas = [desc[0] for desc in cur.description]
    direccion = dict(zip(columnas, fila))
    cur.close()
    conn.close()
    return direccion


# 🔹 Crear dirección (ahora con todos los campos en una sola tabla)
def crear_direccion(data):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO direcciones (
            codigo_direccion,
            calle_principal,
            calle_secundaria,
            numero_casa,
            barrio,
            ciudad,
            provincia,
            zona,
            codigo_postal,
            correo_electronico,
            telefono_principal,
            telefono_secundario,
            referencia,
            tipo_direccion,
            instrucciones_envio,
            cliente_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        data["codigo_direccion"],
        data["calle_principal"],
        data.get("calle_secundaria"),
        data["numero_casa"],
        data["barrio"],
        data["ciudad"],
        data["provincia"],
        data["zona"],
        data.get("codigo_postal"),
        data["correo_electronico"],
        data["telefono_principal"],
        data.get("telefono_secundario"),
        data.get("referencia"),
        data["tipo_direccion"],
        data.get("instrucciones_envio"),
        data["cliente_id"]
    ))
    
    direccion_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return direccion_id

# 🔹 Actualizar dirección (todos los campos en una sola operación)
def actualizar_direccion(direccion_id, data):
    conn = get_db_connection()
    cur = conn.cursor()

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
            codigo_postal = %s,
            correo_electronico = %s,
            telefono_principal = %s,
            telefono_secundario = %s,
            referencia = %s,
            tipo_direccion = %s,
            instrucciones_envio = %s
        WHERE id = %s
    """, (
        data["codigo_direccion"],
        data["calle_principal"],
        data.get("calle_secundaria"),
        data["numero_casa"],
        data["barrio"],
        data["ciudad"],
        data["provincia"],
        data["zona"],
        data.get("codigo_postal"),
        data["correo_electronico"],
        data["telefono_principal"],
        data.get("telefono_secundario"),
        data.get("referencia"),
        data["tipo_direccion"],
        data.get("instrucciones_envio"),
        direccion_id
    ))

    conn.commit()
    cur.close()
    conn.close()

# 🔹 Eliminar dirección (ahora no hay detalles que eliminar por separado)
def eliminar_direccion(direccion_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM direcciones WHERE id = %s", (direccion_id,))
    conn.commit()
    cur.close()
    conn.close()