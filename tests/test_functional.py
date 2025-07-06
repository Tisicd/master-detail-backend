import os
import pytest
import requests
from datetime import datetime

BASE_URL = "http://localhost:5000" if os.getenv('ENV') == 'local' else "http://3.227.43.87:5000"

class TestFuncionalidades:
    def test_maestro_detalle(self, cliente_id):
        """
        Prueba funcional completa del flujo maestro-detalle
        """
        # 1. Crear dirección
        direccion_data = {
            "codigo_direccion": "DIR_FUNC_TEST",
            "calle_principal": "Av. Funcional",
            "numero_casa": "456",
            "barrio": "Funcional Barrio",
            "ciudad": "Guayaquil",
            "provincia": "Guayas",
            "zona": "Urbana",
            "correo_electronico": "funcional@test.com",
            "telefono_principal": "0987654321",
            "tipo_direccion": "Principal",
            "cliente_id": cliente_id
        }
        response = requests.post(f"{BASE_URL}/api/direcciones", json=direccion_data)
        assert response.status_code == 201
        direccion_id = response.json()['direccion_id']

        # 2. Verificar que el cliente tiene la dirección
        response = requests.get(f"{BASE_URL}/api/clientes/{cliente_id}/direcciones")
        assert response.status_code == 200
        direcciones = response.json()['data']
        assert len(direcciones) == 1
        assert direcciones[0]['id'] == direccion_id

        # 3. Verificar campos obligatorios
        bad_data = direccion_data.copy()
        bad_data.pop('calle_principal')
        response = requests.post(f"{BASE_URL}/api/direcciones", json=bad_data)
        assert response.status_code == 400

    def test_campos_requeridos(self):
        """
        Prueba que los campos requeridos en el DEF sean validados
        """
        # Cliente sin campos obligatorios
        bad_cliente = {
            "codigo": "TEST002",
            "tipo_cliente": "Natural"
        }
        response = requests.post(f"{BASE_URL}/api/clientes", json=bad_cliente)
        assert response.status_code == 400
        assert 'nombres' in response.json().get('message', '')
        assert 'apellidos' in response.json().get('message', '')
        assert 'tipo_documento' in response.json().get('message', '')
        assert 'numero_documento' in response.json().get('message', '')

        # Dirección sin campos obligatorios
        bad_direccion = {
            "codigo_direccion": "DIR_BAD",
            "cliente_id": 1
        }
        response = requests.post(f"{BASE_URL}/api/direcciones", json=bad_direccion)
        assert response.status_code == 400
        assert 'calle_principal' in response.json().get('message', '')
        assert 'numero_casa' in response.json().get('message', '')
        assert 'barrio' in response.json().get('message', '')
        assert 'ciudad' in response.json().get('message', '')
        assert 'provincia' in response.json().get('message', '')
        assert 'zona' in response.json().get('message', '')
        assert 'correo_electronico' in response.json().get('message', '')
        assert 'telefono_principal' in response.json().get('message', '')
        assert 'tipo_direccion' in response.json().get('message', '')