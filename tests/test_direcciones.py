import pytest 
from models.direcciones import validar_direccion_data

def test_direccion_valida():
    data = {
        "tipo_direccion": "Principal",
        "correo_electronico": "test@mail.com",
        "telefono_principal": "0991234567",
        "telefono_secundario": "042345678",
        "codigo_postal": "090112"
    }
    try:
        validar_direccion_data(data)
        assert True
    except ValueError:
        assert False

def test_correo_invalido():
    data = {
        "tipo_direccion": "Envío",
        "correo_electronico": "bad_email",
        "telefono_principal": "0991234567"
    }
    with pytest.raises(ValueError):
        validar_direccion_data(data)

def test_registrar_direccion_principal_exitosa():
    from models.direcciones import crear_direccion
    from models.clientes import crear_cliente

    # Crear cliente sin direcciones
    cliente = {
        "nombres": "Marco",
        "apellidos": "Salinas",
        "tipo_documento": "Cédula",
        "numero_documento": "1707122170",
        "tipo_cliente": "Natural",
        "razon_social": "",
        "estado": "Activo",
        "observaciones": ""
    }
    cliente_id = crear_cliente(cliente)

    direccion = {
        "codigo_direccion": "DIR100",
        "calle_principal": "Av. Colón",
        "calle_secundaria": "6 de Diciembre",
        "numero_casa": "N12-34",
        "barrio": "La Mariscal",
        "ciudad": "Quito",
        "provincia": "Pichincha",
        "zona": "Urbana",
        "codigo_postal": "170517",
        "correo_electronico": "marco.salinas@example.com",
        "telefono_principal": "0987654321",
        "telefono_secundario": "",
        "referencia": "Frente al hotel Hilton",
        "tipo_direccion": "Principal",
        "instrucciones_envio": "Tocar timbre",
        "cliente_id": cliente_id
    }

    direccion_id = crear_direccion(direccion)
    assert isinstance(direccion_id, int)

def test_direccion_principal_duplicada():
    from models.direcciones import crear_direccion
    from models.clientes import crear_cliente
    cliente = {
        "nombres": "Laura",
        "apellidos": "Vega",
        "tipo_documento": "Cédula",
        "numero_documento": "1704710308",
        "tipo_cliente": "Natural",
        "razon_social": "",
        "estado": "Activo",
        "observaciones": ""
    }
    cliente_id = crear_cliente(cliente)

    direccion_base = {
        "calle_principal": "Av. Amazonas",
        "calle_secundaria": "Juan León Mera",
        "numero_casa": "N23-56",
        "barrio": "El Jardín",
        "ciudad": "Quito",
        "provincia": "Pichincha",
        "zona": "Urbana",
        "codigo_postal": "170150",
        "correo_electronico": "laura@example.com",
        "telefono_principal": "0999999999",
        "telefono_secundario": "",
        "referencia": "Frente a parque",
        "tipo_direccion": "Principal",
        "instrucciones_envio": "Llamar al llegar",
        "cliente_id": cliente_id
    }

    direccion1 = {**direccion_base, "codigo_direccion": "DIR200"}
    crear_direccion(direccion1)

    direccion2 = {**direccion_base, "codigo_direccion": "DIR201"}

    with pytest.raises(ValueError) as exc_info:
        crear_direccion(direccion2)

    assert "ya tiene una dirección principal" in str(exc_info.value).lower()

import pytest

def test_correo_invalido_en_direccion():
    from models.direcciones import crear_direccion
    from models.clientes import crear_cliente

    cliente_id = crear_cliente({
        "nombres": "Kevin",
        "apellidos": "Paredes",
        "tipo_documento": "Cédula",
        "numero_documento": "1702103720",
        "tipo_cliente": "Natural",
        "razon_social": "",
        "estado": "Activo",
        "observaciones": ""
    })

    direccion = {
        "codigo_direccion": "DIR300",
        "calle_principal": "Av. 10 de Agosto",
        "calle_secundaria": "El Inca",
        "numero_casa": "S12-78",
        "barrio": "Centro Norte",
        "ciudad": "Quito",
        "provincia": "Pichincha",
        "zona": "Urbana",
        "codigo_postal": "170112",
        "correo_electronico": "correo@@mal",  # inválido
        "telefono_principal": "0912345678",
        "telefono_secundario": "",
        "referencia": "Junto al parqueadero",
        "tipo_direccion": "Principal",
        "instrucciones_envio": "No tocar bocina",
        "cliente_id": cliente_id
    }

    with pytest.raises(ValueError) as exc_info:
        crear_direccion(direccion)

    assert "correo" in str(exc_info.value).lower()

def test_telefono_con_letras():
    from models.direcciones import crear_direccion
    from models.clientes import crear_cliente
    cliente_id = crear_cliente({
        "nombres": "Verónica",
        "apellidos": "Quishpe",
        "tipo_documento": "Cédula",
        "numero_documento": "1715959464",
        "tipo_cliente": "Natural",
        "razon_social": "",
        "estado": "Activo",
        "observaciones": ""
    })

    direccion = {
        "codigo_direccion": "DIR400",
        "calle_principal": "Av. América",
        "calle_secundaria": "La Gasca",
        "numero_casa": "Oe4-56",
        "barrio": "San Carlos",
        "ciudad": "Quito",
        "provincia": "Pichincha",
        "zona": "Urbana",
        "codigo_postal": "170113",
        "correo_electronico": "vero@example.com",
        "telefono_principal": "09abc1234",  # ← inválido
        "telefono_secundario": "",
        "referencia": "Al lado de la iglesia",
        "tipo_direccion": "Principal",
        "instrucciones_envio": "No dejar con vecinos",
        "cliente_id": cliente_id
    }

    with pytest.raises(ValueError) as exc_info:
        crear_direccion(direccion)

    assert "teléfono" in str(exc_info.value).lower()

def test_limite_direcciones_cliente():
    from models.direcciones import crear_direccion
    from models.clientes import crear_cliente
    cliente_id = crear_cliente({
        "nombres": "Daniel",
        "apellidos": "Ríos",
        "tipo_documento": "Cédula",
        "numero_documento": "1751845916",
        "tipo_cliente": "Natural",
        "razon_social": "",
        "estado": "Activo",
        "observaciones": ""
    })

    base_direccion = {
        "calle_principal": "Av. Real Audiencia",
        "calle_secundaria": "La Florida",
        "numero_casa": "M9-56",
        "barrio": "La Roldós",
        "ciudad": "Quito",
        "provincia": "Pichincha",
        "zona": "Urbana",
        "codigo_postal": "170510",
        "correo_electronico": "daniel@example.com",
        "telefono_principal": "0987654321",
        "telefono_secundario": "",
        "referencia": "Cerca al redondel",
        "tipo_direccion": "Otro",
        "instrucciones_envio": "Subir al segundo piso",
        "cliente_id": cliente_id
    }

    # Crear 5 direcciones válidas
    for i in range(5):
        direccion = {**base_direccion, "codigo_direccion": f"DIR50{i}"}
        crear_direccion(direccion)

    # Intentar crear la sexta
    direccion_extra = {**base_direccion, "codigo_direccion": "DIR506"}

    with pytest.raises(ValueError) as exc_info:
        crear_direccion(direccion_extra)

    assert "número máximo de direcciones" in str(exc_info.value).lower()

def test_actualizar_direccion_sin_cambiar_tipo():
    from models.direcciones import crear_direccion, actualizar_direccion
    from models.clientes import crear_cliente, obtener_cliente_por_id
    
    cliente_id = crear_cliente({
        "nombres": "Esteban",
        "apellidos": "Galárraga",
        "tipo_documento": "Cédula",
        "numero_documento": "1756547434",
        "tipo_cliente": "Natural",
        "razon_social": "",
        "estado": "Activo",
        "observaciones": ""
    })

    direccion = {
        "codigo_direccion": "DIR600",
        "calle_principal": "Av. 6 de Diciembre",
        "calle_secundaria": "El Batán",
        "numero_casa": "N34-78",
        "barrio": "El Batán Alto",
        "ciudad": "Quito",
        "provincia": "Pichincha",
        "zona": "Urbana",
        "codigo_postal": "170517",
        "correo_electronico": "esteban@example.com",
        "telefono_principal": "0991122334",
        "telefono_secundario": "",
        "referencia": "Frente al parqueadero",
        "tipo_direccion": "Facturación",
        "instrucciones_envio": "Pedir permiso a guardia",
        "cliente_id": cliente_id
    }

    direccion_id = crear_direccion(direccion)

    # Actualizar ciudad y zona sin tocar tipo_direccion
    direccion_actualizada = {**direccion, "ciudad": "Cuenca", "zona": "Rural"}
    actualizar_direccion(direccion_id, direccion_actualizada)

    # No se espera error
    assert True