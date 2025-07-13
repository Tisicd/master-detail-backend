import pytest
from models.clientes import validar_documento_ecuador
from models.clientes import crear_cliente
from psycopg2 import IntegrityError

def test_cedula_valida():
    assert validar_documento_ecuador("Cédula", "1752863017") is True

def test_cedula_invalida():
    assert validar_documento_ecuador("Cédula", "1234567890") == False
    
def test_ruc_valido():
    assert validar_documento_ecuador("RUC", "1726382888001") is True

def test_ruc_invalido():
    assert validar_documento_ecuador("RUC", "1234567890000") == False

def test_tipo_documento_invalido():
    assert validar_documento_ecuador("Pasaporte", "A123456789") == False

def test_crear_cliente_duplicado():
    data = {
        "nombres": "Juan",
        "apellidos": "Pérez",
        "tipo_documento": "Cédula",
        "numero_documento": "1726382888",
        "tipo_cliente": "Natural",
        "razon_social": "",
        "estado": "Activo",
        "observaciones": ""
    }

    with pytest.raises(ValueError) as exc_info:
        crear_cliente(data)
    
    assert "cliente con ese número de documento" in str(exc_info.value)

def test_crear_cliente_juridico():
    data = {
        "nombres": "Empresa",
        "apellidos": "Ejemplo",
        "tipo_documento": "RUC",
        "numero_documento": "1726382888001",  # RUC válido
        "tipo_cliente": "Jurídico",
        "razon_social": "Ejemplo S.A.",
        "estado": "Activo",
        "observaciones": "Cliente empresarial"
    }

    cliente_id = crear_cliente(data)
    assert isinstance(cliente_id, int)
    assert cliente_id > 0

def test_actualizar_cliente():
    # Primero, crear un cliente
    data = {
        "nombres": "Luis",
        "apellidos": "Andrade",
        "tipo_documento": "Cédula",
        "numero_documento": "1710034065",
        "tipo_cliente": "Natural",
        "razon_social": "",
        "estado": "Activo",
        "observaciones": "Cliente nuevo"
    }

    cliente_id = crear_cliente(data)

    # Luego, actualizar ese cliente
    data_actualizado = data.copy()
    data_actualizado["nombres"] = "Luis Alfredo"
    data_actualizado["observaciones"] = "Cliente actualizado"

    from models.clientes import actualizar_cliente, obtener_cliente_por_id
    actualizar_cliente(cliente_id, data_actualizado)

    cliente = obtener_cliente_por_id(cliente_id)
    assert cliente["nombres"] == "Luis Alfredo"
    assert cliente["observaciones"] == "Cliente actualizado"

def test_eliminar_cliente():
    # Crear cliente a eliminar
    data = {
        "nombres": "Sandra",
        "apellidos": "Lozano",
        "tipo_documento": "Cédula",
        "numero_documento": "1715983928",
        "tipo_cliente": "Natural",
        "razon_social": "",
        "estado": "Activo",
        "observaciones": "Cliente temporal"
    }

    cliente_id = crear_cliente(data)

    from models.clientes import eliminar_cliente, obtener_cliente_por_id
    eliminar_cliente(cliente_id)

    cliente = obtener_cliente_por_id(cliente_id)
    assert cliente is None

def test_tipo_documento_invalido_cliente():
    data = {
        "nombres": "Mario",
        "apellidos": "Bravo",
        "tipo_documento": "Pasaporte",  # Tipo inválido
        "numero_documento": "A123456789",
        "tipo_cliente": "Natural",
        "razon_social": "",
        "estado": "Activo",
        "observaciones": "Intento fallido"
    }

    with pytest.raises(ValueError) as exc_info:
        crear_cliente(data)

    assert "Tipo de documento inválido" in str(exc_info.value)

def test_buscar_cliente_por_nombre():
    from models.clientes import buscar_clientes
    resultados = buscar_clientes({"nombre": "Ana"})
    assert isinstance(resultados, list)
    assert any("Ana" in c["nombre_completo"] for c in resultados)

def test_buscar_cliente_por_documento():
    from models.clientes import buscar_clientes
    resultados = buscar_clientes({"numero_documento": "1790011223001"})
    assert len(resultados) == 1
    assert resultados[0]["numero_documento"] == "1790011223001"

def test_buscar_cliente_por_estado():
    from models.clientes import buscar_clientes
    resultados = buscar_clientes({"estado": "inactivo"})
    assert all(c["estado"].lower() == "inactivo" for c in resultados)
