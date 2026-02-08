"""Tests de integración de endpoints API."""

import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO


@pytest.fixture
def csv_content():
    """Contenido CSV mínimo con cabecera."""
    return b"""cups_cliente,instalacion_gen,tipo_autoconsumo,fecha_desde_1,fecha_hasta_1,energia_neta_gen_1,energia_neta_gen_2,energia_neta_gen_3,energia_neta_gen_4,energia_neta_gen_5,energia_neta_gen_6,energia_autoconsumida_1,energia_autoconsumida_2,energia_autoconsumida_3,energia_autoconsumida_4,energia_autoconsumida_5,energia_autoconsumida_6,pago_tda_1,pago_tda_2,pago_tda_3,pago_tda_4,pago_tda_5,pago_tda_6
ES0021000000000001AA,GEN001,41,2024-01-01,2024-01-31,120.5,115.3,125.8,118.2,122.9,119.7,60.2,58.1,62.4,59.5,61.8,60.0,12.50,11.80,13.20,12.10,12.75,12.30
"""


def test_consulta_energia_sin_resultados(client):
    """GET /api/v1/energia?cups=NOEXISTE retorna 200 con lista vacía."""
    response = client.get("/api/v1/energia?cups=NOEXISTE")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["registros"] == []


def test_consulta_energia_sin_filtros(client):
    """GET /api/v1/energia sin params retorna 200."""
    response = client.get("/api/v1/energia")
    assert response.status_code == 200
    assert "total" in response.json()
    assert "registros" in response.json()


def test_root(client):
    """GET / retorna servicio y docs."""
    response = client.get("/")
    assert response.status_code == 200
    assert "docs" in response.json()
