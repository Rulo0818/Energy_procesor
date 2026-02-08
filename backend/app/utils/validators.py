"""Validadores CUPS, tipos de autoconsumo, etc."""

TIPOS_AUTOCONSUMO_VALIDOS = {12, 41, 42, 43, 51}


def validar_tipo_autoconsumo(tipo: int) -> bool:
    """Comprueba si el tipo de autoconsumo es válido."""
    return tipo in TIPOS_AUTOCONSUMO_VALIDOS
