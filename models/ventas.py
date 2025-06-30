from .db import get_db_connection

def obtener_ventas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            v.id,
            v.fecha,
            c.nombres || ' ' || c.apellidos AS cliente_nombre,
            p.nombre AS producto_nombre,
            v.total
        FROM ventas v
        JOIN clientes c ON v.cliente_id = c.id
        JOIN detalles_venta dv ON dv.venta_id = v.id
        JOIN productos p ON dv.producto_id = p.id
    """)
    columnas = [desc[0] for desc in cur.description]
    ventas = [dict(zip(columnas, fila)) for fila in cur.fetchall()]
    cur.close()
    conn.close()
    return ventas
