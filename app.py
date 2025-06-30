from flask import Flask, jsonify, request
from flask_cors import CORS
from models.clientes import (
    obtener_todos_los_clientes,
    crear_cliente,
    obtener_cliente_por_id,
    actualizar_cliente,
    eliminar_cliente
)
from models.direcciones import (
    obtener_direcciones_por_cliente,
    crear_direccion,
    eliminar_direccion,
    actualizar_direccion
)

from models.ventas import obtener_ventas

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({"message": "API Master-Detail Online"})

# 🔹 GET: Lista de clientes
@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    try:
        clientes = obtener_todos_los_clientes()
        return jsonify({"status": "success", "clientes": clientes})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 🔹 POST: Crear cliente
@app.route('/api/clientes', methods=['POST'])
def post_cliente():
    try:
        data = request.json
        nuevo_id = crear_cliente(data)
        return jsonify({"status": "success", "cliente_id": nuevo_id}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 🔹 GET: Obtener cliente por ID
@app.route('/api/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    try:
        cliente = obtener_cliente_por_id(cliente_id)
        if cliente:
            return jsonify({"status": "success", "cliente": cliente})
        else:
            return jsonify({"status": "error", "message": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 🔹 PUT: Actualizar cliente
@app.route('/api/clientes/<int:cliente_id>', methods=['PUT'])
def put_cliente(cliente_id):
    try:
        data = request.json
        actualizar_cliente(cliente_id, data)
        return jsonify({"status": "success", "message": "Cliente actualizado"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 🔹 DELETE: Eliminar cliente
@app.route('/api/clientes/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    try:
        eliminar_cliente(cliente_id)
        return jsonify({"status": "success", "message": "Cliente eliminado"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
# 🔹 Obtener direcciones por cliente
@app.route('/api/clientes/<int:cliente_id>/direcciones', methods=['GET'])
def get_direcciones_cliente(cliente_id):
    try:
        direcciones = obtener_direcciones_por_cliente(cliente_id)
        return jsonify({
            "status": "success",
            "direcciones": direcciones
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 🔹 Crear nueva dirección
@app.route('/api/direcciones', methods=['POST'])
def post_direccion():
    data = request.json
    try:
        nueva_id = crear_direccion(data)
        return jsonify({
            "status": "success",
            "message": "Dirección creada",
            "direccion_id": nueva_id
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 🔹 Actualizar dirección
@app.route('/api/direcciones/<int:id>', methods=['PUT'])
def put_direccion(id):
    data = request.json
    try:
        actualizar_direccion(id, data)
        return jsonify({
            "status": "success",
            "message": "Dirección actualizada"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 🔹 Eliminar dirección
@app.route('/api/direcciones/<int:id>', methods=['DELETE'])
def delete_direccion(id):
    try:
        eliminar_direccion(id)
        return jsonify({
            "status": "success",
            "message": "Dirección eliminada"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/sales', methods=['GET'])
def get_sales():
    try:
        ventas = obtener_ventas()
        return jsonify({"status": "success", "sales": ventas})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

