"""Tests unitarios de parsing y validación de líneas."""

import pytest
from app.services.procesador_service import validar_linea
from app.utils.validators import TIPOS_AUTOCONSUMO_VALIDOS


def _row_valido():
    return {
        "cups_cliente": "ES0021000000000001AA",
        "instalacion_gen": "GEN001",
        "tipo_autoconsumo": "41",
        "fecha_desde_1": "2024-01-01",
        "fecha_hasta_1": "2024-01-31",
        "energia_neta_gen_1": "100.5",
        "energia_neta_gen_2": "95.3",
        "energia_neta_gen_3": "102.1",
        "energia_neta_gen_4": "98.7",
        "energia_neta_gen_5": "105.2",
        "energia_neta_gen_6": "99.8",
        "energia_autoconsumida_1": "50.0",
        "energia_autoconsumida_2": "48.0",
        "energia_autoconsumida_3": "51.0",
        "energia_autoconsumida_4": "49.5",
        "energia_autoconsumida_5": "52.0",
        "energia_autoconsumida_6": "50.5",
        "pago_tda_1": "10.50",
        "pago_tda_2": "9.80",
        "pago_tda_3": "10.20",
        "pago_tda_4": "9.90",
        "pago_tda_5": "10.75",
        "pago_tda_6": "10.00",
    }


def test_validar_linea_correcta(db_session):
    """Línea válida no genera errores."""
    row = _row_valido()
    errores = validar_linea(row, 2, db_session)
    assert len(errores) == 0


def test_tipo_autoconsumo_invalido(db_session):
    """Tipo autoconsumo no soportado genera error tipo_no_soportado."""
    row = _row_valido()
    row["tipo_autoconsumo"] = "99"
    errores = validar_linea(row, 2, db_session)
    assert any(e[0] == "tipo_no_soportado" for e in errores)


def test_cups_inexistente(db_session):
    """CUPS no existente genera error cliente_inexistente (simulado: no empieza por ES)."""
    row = _row_valido()
    row["cups_cliente"] = "XX9999999999999999ZZ"
    errores = validar_linea(row, 2, db_session)
    assert any(e[0] == "cliente_inexistente" for e in errores)


def test_array_incompleto(db_session):
    """Array con menos de 6 valores genera error array_longitud_invalida o formato_invalido."""
    row = _row_valido()
    for i in range(4, 7):
        row.pop(f"energia_neta_gen_{i}", None)
    errores = validar_linea(row, 2, db_session)
    assert any(
        "array_longitud_invalida" in e[0] or "formato_invalido" in e[0]
        for e in errores
    )


def test_fecha_formato_invalido(db_session):
    """Fecha con formato incorrecto genera error fecha_invalida."""
    row = _row_valido()
    row["fecha_desde_1"] = "01/01/2024"
    errores = validar_linea(row, 2, db_session)
    assert any(e[0] == "fecha_invalida" for e in errores)


def test_tipos_validos_constante():
    """Constante TIPOS_AUTOCONSUMO_VALIDOS contiene 12, 41, 42, 43, 51."""
    assert TIPOS_AUTOCONSUMO_VALIDOS == {12, 41, 42, 43, 51}
