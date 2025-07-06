from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger

from models.clientes import (
    obtener_todos_los_clientes,
    crear_cliente,
    obtener_cliente_por_id,
    actualizar_cliente,
    eliminar_cliente
)
from models.direcciones import (
    obtener_direcciones_por_cliente,
    obtener_direccion_por_id,
    crear_direccion,
    actualizar_direccion,
    eliminar_direccion
)

app = Flask(__name__)
CORS(app)

# Configuración de Swagger
app.config['SWAGGER'] = {
    'title': 'API de Gestión de Clientes y Direcciones',
    'uiversion': 3,
    'description': 'Documentación API para el sistema de gestión de clientes y direcciones',
    'specs_route': '/api/docs/'
}
swagger = Swagger(app)

@app.route('/')
def index():
    return jsonify({"message": "API Master-Detail Online"})

# ==============================================
# RUTAS PARA CLIENTES
# ==============================================

@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    """
    Obtener todos los clientes
    ---
    tags:
      - Clientes
    responses:
      200:
        description: Lista de clientes
        schema:
          type: object
          properties:
            status:
              type: string
            count:
              type: integer
            data:
              type: array
              items:
                type: object
    """
    try:
        clientes = obtener_todos_los_clientes()
        return jsonify({
            "status": "success",
            "count": len(clientes),
            "data": clientes
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al obtener clientes: {str(e)}"
        }), 500

@app.route('/api/clientes', methods=['POST'])
def post_cliente():
    """
    Crear un nuevo cliente
    ---
    tags:
      - Clientes
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - codigo
            - nombres
            - apellidos
            - tipo_documento
            - numero_documento
            - tipo_cliente
          properties:
            codigo:
              type: string
            nombres:
              type: string
            apellidos:
              type: string
            tipo_documento:
              type: string
              enum: [Cédula, RUC]
            numero_documento:
              type: string
            tipo_cliente:
              type: string
              enum: [Natural, Jurídico]
            razon_social:
              type: string
            estado:
              type: string
              enum: [Activo, Inactivo]
            observaciones:
              type: string
    responses:
      201:
        description: Cliente creado
      400:
        description: Error de datos
      500:
        description: Error interno
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No se proporcionaron datos"
            }), 400

        nuevo_id = crear_cliente(data)
        return jsonify({
            "status": "success",
            "message": "Cliente creado exitosamente",
            "cliente_id": nuevo_id
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al crear cliente: {str(e)}"
        }), 500

@app.route('/api/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    try:
        cliente = obtener_cliente_por_id(cliente_id)
        if cliente:
            return jsonify({
                "status": "success",
                "data": cliente
            })
        return jsonify({
            "status": "error",
            "message": "Cliente no encontrado"
        }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al obtener cliente: {str(e)}"
        }), 500

@app.route('/api/clientes/<int:cliente_id>', methods=['PUT'])
def put_cliente(cliente_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No se proporcionaron datos para actualizar"
            }), 400

        actualizar_cliente(cliente_id, data)
        return jsonify({
            "status": "success",
            "message": "Cliente actualizado exitosamente"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al actualizar cliente: {str(e)}"
        }), 500

@app.route('/api/clientes/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    try:
        eliminar_cliente(cliente_id)
        return jsonify({
            "status": "success",
            "message": "Cliente eliminado exitosamente"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al eliminar cliente: {str(e)}"
        }), 500

# ==============================================
# RUTAS PARA DIRECCIONES
# ==============================================

@app.route('/api/clientes/<int:cliente_id>/direcciones', methods=['GET'])
def get_direcciones_cliente(cliente_id):
    """
    Obtener todas las direcciones de un cliente
    ---
    tags:
      - Direcciones
    parameters:
      - name: cliente_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Lista de direcciones del cliente
      404:
        description: Cliente no encontrado
    """
    try:
        direcciones = obtener_direcciones_por_cliente(cliente_id)
        return jsonify({
            "status": "success",
            "count": len(direcciones),
            "data": direcciones
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al obtener direcciones: {str(e)}"
        }), 500

@app.route('/api/direcciones/<int:direccion_id>', methods=['GET'])
def get_direccion(direccion_id):
    try:
        direccion = obtener_direccion_por_id(direccion_id)
        if direccion:
            return jsonify({
                "status": "success",
                "data": direccion
            })
        return jsonify({
            "status": "error",
            "message": "Dirección no encontrada"
        }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al obtener dirección: {str(e)}"
        }), 500

@app.route('/api/direcciones', methods=['POST'])
def post_direccion():
    """
    Crear nueva dirección para un cliente
    ---
    tags:
      - Direcciones
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - codigo_direccion
            - calle_principal
            - numero_casa
            - barrio
            - ciudad
            - provincia
            - zona
            - correo_electronico
            - telefono_principal
            - tipo_direccion
            - cliente_id
          properties:
            codigo_direccion:
              type: string
            calle_principal:
              type: string
            calle_secundaria:
              type: string
            numero_casa:
              type: string
            barrio:
              type: string
            ciudad:
              type: string
            provincia:
              type: string
            zona:
              type: string
              enum: [Urbana, Rural]
            codigo_postal:
              type: string
            correo_electronico:
              type: string
            telefono_principal:
              type: string
            telefono_secundario:
              type: string
            referencia:
              type: string
            tipo_direccion:
              type: string
              enum: [Principal, Facturación, Envío, Oficina, Otro]
            instrucciones_envio:
              type: string
            cliente_id:
              type: integer
    responses:
      201:
        description: Dirección creada
      400:
        description: Datos incompletos o inválidos
      500:
        description: Error interno
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No se proporcionaron datos"
            }), 400

        nueva_id = crear_direccion(data)
        return jsonify({
            "status": "success",
            "message": "Dirección creada exitosamente",
            "direccion_id": nueva_id
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al crear dirección: {str(e)}"
        }), 500

@app.route('/api/direcciones/<int:direccion_id>', methods=['PUT'])
def put_direccion(direccion_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No se proporcionaron datos para actualizar"
            }), 400

        actualizar_direccion(direccion_id, data)
        return jsonify({
            "status": "success",
            "message": "Dirección actualizada exitosamente"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al actualizar dirección: {str(e)}"
        }), 500

@app.route('/api/direcciones/<int:direccion_id>', methods=['DELETE'])
def delete_direccion(direccion_id):
    try:
        eliminar_direccion(direccion_id)
        return jsonify({
            "status": "success",
            "message": "Dirección eliminada exitosamente"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al eliminar dirección: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)