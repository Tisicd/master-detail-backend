import pytest
import requests
import yaml
import os

BASE_URL = "http://localhost:5000" if os.getenv('ENV') == 'local' else "http://3.227.43.87:5000"

# Cargar especificación Swagger
#with open('swagger.yml', 'r') as f:
#    swagger_spec = yaml.safe_load(f)

# Pruebas para el endpoint de clientes
class TestClientesAPI:
    def test_get_clientes(self):
        """
        Test para validar el endpoint GET /api/clientes
        """
        response = requests.get(f"{BASE_URL}/api/clientes")
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
        assert 'count' in data
        assert 'data' in data
        assert isinstance(data['data'], list)

    def test_create_cliente(self):
        """
        Test para validar el endpoint POST /api/clientes
        """
        test_cliente = {
            "codigo": "TEST001",
            "nombres": "Test",
            "apellidos": "Cliente",
            "tipo_documento": "Cédula",
            "numero_documento": "9999999999",
            "tipo_cliente": "Natural",
            "estado": "Activo"
        }
        response = requests.post(f"{BASE_URL}/api/clientes", json=test_cliente)
        assert response.status_code == 201
        data = response.json()
        assert 'status' in data
        assert 'message' in data
        assert 'cliente_id' in data

# Pruebas para el endpoint de direcciones
class TestDireccionesAPI:
    def test_create_direccion(self, cliente_id):
        """
        Test para validar el endpoint POST /api/direcciones
        """
        test_direccion = {
            "codigo_direccion": "DIR_TEST",
            "calle_principal": "Av. Test",
            "numero_casa": "123",
            "barrio": "Test Barrio",
            "ciudad": "Quito",
            "provincia": "Pichincha",
            "zona": "Urbana",
            "correo_electronico": "test@test.com",
            "telefono_principal": "0999999999",
            "tipo_direccion": "Principal",
            "cliente_id": cliente_id
        }
        response = requests.post(f"{BASE_URL}/api/direcciones", json=test_direccion)
        assert response.status_code == 201
        data = response.json()
        assert 'status' in data
        assert 'message' in data
        assert 'direccion_id' in data
        return data['direccion_id']

    def test_get_direcciones_cliente(self, cliente_id):
        """
        Test para validar el endpoint GET /api/clientes/<id>/direcciones
        """
        response = requests.get(f"{BASE_URL}/api/clientes/{cliente_id}/direcciones")
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
        assert 'count' in data
        assert 'data' in data
        assert isinstance(data['data'], list)

# Fixture para crear un cliente de prueba
@pytest.fixture
def cliente_id():
    test_cliente = {
        "codigo": "TEST001",
        "nombres": "Test",
        "apellidos": "Cliente",
        "tipo_documento": "Cédula",
        "numero_documento": "9999999999",
        "tipo_cliente": "Natural",
        "estado": "Activo"
    }
    response = requests.post(f"{BASE_URL}/api/clientes", json=test_cliente)
    return response.json()['cliente_id']

# Fixture para limpiar datos después de las pruebas
@pytest.fixture(autouse=True)
def cleanup(request, cliente_id):
    def remove_test_data():
        # Eliminar direcciones de prueba
        response = requests.get(f"{BASE_URL}/api/clientes/{cliente_id}/direcciones")
        if response.status_code == 200:
            for direccion in response.json()['data']:
                requests.delete(f"{BASE_URL}/api/direcciones/{direccion['id']}")
        # Eliminar cliente de prueba
        requests.delete(f"{BASE_URL}/api/clientes/{cliente_id}")
    request.addfinalizer(remove_test_data)