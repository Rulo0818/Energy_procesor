"""Procesamiento de archivos de peajes: parsing, validaciones y persistencia."""

import json
import os
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from sqlalchemy.orm import Session

from app.models import ArchivoProcesado, EnergiaExcedentaria, RegistroErrores
from app.utils.validators import TIPOS_AUTOCONSUMO_VALIDOS


def validar_cups_existe(cups: str, db: Session) -> bool:
    """
    Verifica si CUPS existe. Simulado: CUPS que empiezan por 'ES' y len >= 10.
    Ajustar según tabla clientes real.
    """
    return bool(cups and cups.startswith("ES") and len(cups) >= 10)


def validar_linea(
    row: dict[str, Any], num_linea: int, db: Session
) -> list[tuple[str, str]]:
    """
    Valida una línea del archivo.
    Retorna lista de (tipo_error, descripcion). Lista vacía si es válida.
    """
    errores: list[tuple[str, str]] = []

    cups = (row.get("cups_cliente") or "").strip()
    if not cups or not validar_cups_existe(cups, db):
        errores.append(
            ("cliente_inexistente", f"CUPS {cups or '(vacío)'} no encontrado en sistema")
        )

    try:
        tipo = int(row.get("tipo_autoconsumo", 0))
        if tipo not in TIPOS_AUTOCONSUMO_VALIDOS:
            errores.append(
                (
                    "tipo_no_soportado",
                    f"Tipo autoconsumo {tipo} no válido. Permitidos: {sorted(TIPOS_AUTOCONSUMO_VALIDOS)}",
                )
            )
    except (ValueError, TypeError):
        errores.append(("formato_invalido", "Tipo autoconsumo no es un número entero"))

    try:
        fecha_desde_str = (row.get("fecha_desde_1") or "").strip()
        fecha_hasta_str = (row.get("fecha_hasta_1") or "").strip()
        datetime.strptime(fecha_desde_str, "%Y-%m-%d")
        datetime.strptime(fecha_hasta_str, "%Y-%m-%d")
    except ValueError:
        errores.append(
            ("fecha_invalida", "Formato de fecha incorrecto (esperado YYYY-MM-DD)")
        )

    for campo in ["energia_neta_gen", "energia_autoconsumida", "pago_tda"]:
        valores = []
        for i in range(1, 7):
            key = f"{campo}_{i}"
            try:
                val = row.get(key, "0")
                valores.append(Decimal(str(val).strip()) if val else Decimal("0"))
            except (InvalidOperation, TypeError):
                errores.append(
                    ("formato_invalido", f"Valor inválido en {key}: {row.get(key)}")
                )
                break
        if len(valores) != 6:
            errores.append(
                (
                    "array_longitud_invalida",
                    f"Campo {campo} debe tener exactamente 6 valores (P1-P6)",
                )
            )

    return errores


def insertar_energia(
    db: Session, archivo_id: int, linea: int, row: dict[str, Any]
) -> None:
    """Inserta un registro de energía validado."""
    energia_neta = [
        Decimal(str(row.get(f"energia_neta_gen_{i}", 0)).strip() or "0")
        for i in range(1, 7)
    ]
    energia_auto = [
        Decimal(str(row.get(f"energia_autoconsumida_{i}", 0)).strip() or "0")
        for i in range(1, 7)
    ]
    pago = [
        Decimal(str(row.get(f"pago_tda_{i}", 0)).strip() or "0") for i in range(1, 7)
    ]

    registro = EnergiaExcedentaria(
        archivo_id=archivo_id,
        linea_archivo=linea,
        cups_cliente=(row["cups_cliente"] or "").strip(),
        instalacion_gen=(row.get("instalacion_gen") or "").strip(),
        fecha_desde=datetime.strptime(
            (row.get("fecha_desde_1") or "").strip(), "%Y-%m-%d"
        ).date(),
        fecha_hasta=datetime.strptime(
            (row.get("fecha_hasta_1") or "").strip(), "%Y-%m-%d"
        ).date(),
        tipo_autoconsumo=int(row["tipo_autoconsumo"]),
        energia_neta_gen=energia_neta,
        energia_autoconsumida=energia_auto,
        pago_tda=pago,
    )
    db.add(registro)
    db.commit()


def registrar_error(
    db: Session,
    archivo_id: int,
    linea: int,
    tipo: str,
    desc: str,
    datos: str | None = None,
) -> None:
    """Registra un error en la BD."""
    error = RegistroErrores(
        archivo_id=archivo_id,
        linea_archivo=linea,
        tipo_error=tipo,
        descripcion=desc,
        datos_linea=datos,
    )
    db.add(error)
    db.commit()


def procesar_archivo(db: Session, archivo_id: int, ruta_archivo: str) -> None:
    """
    Procesa archivo de peajes línea por línea.
    Usa primer valor de fechas, valida arrays de 6, tipos {12,41,42,43,51}, CUPS.
    """
    archivo = db.query(ArchivoProcesado).filter(ArchivoProcesado.id == archivo_id).first()
    if not archivo:
        raise ValueError(f"Archivo {archivo_id} no encontrado")

    archivo.estado = "procesando"
    archivo.fecha_procesamiento = datetime.utcnow()
    db.commit()

    exitosos = 0
    con_error = 0
    total = 0

    if not os.path.exists(ruta_archivo):
        archivo.estado = "error"
        db.commit()
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")

    try:
        import csv

        with open(ruta_archivo, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for num_linea, row in enumerate(reader, start=2):
                total += 1
                row = {k.strip(): v for k, v in row.items() if k}
                errores = validar_linea(row, num_linea, db)

                if errores:
                    for tipo_err, desc in errores:
                        registrar_error(
                            db, archivo_id, num_linea, tipo_err, desc, json.dumps(row)
                        )
                    con_error += 1
                else:
                    try:
                        insertar_energia(db, archivo_id, num_linea, row)
                        exitosos += 1
                    except Exception as e:
                        registrar_error(
                            db,
                            archivo_id,
                            num_linea,
                            "inconsistencia_numerica",
                            f"Error al insertar: {e!s}",
                            json.dumps(row),
                        )
                        con_error += 1

        archivo.estado = "completado"
        archivo.total_registros = total
        archivo.registros_exitosos = exitosos
        archivo.registros_con_error = con_error
        db.commit()
    except Exception:
        archivo.estado = "error"
        db.commit()
        raise
