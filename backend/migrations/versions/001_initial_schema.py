"""Initial schema: archivo_procesado, tipo_autoconsumo, energia_excedentaria, registro_errores.

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.create_table(
        "archivo_procesado",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre_archivo", sa.String(255), nullable=False),
        sa.Column("hash_archivo", sa.String(64), nullable=False),
        sa.Column("fecha_carga", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("fecha_procesamiento", sa.DateTime(), nullable=True),
        sa.Column("estado", sa.String(20), nullable=False, server_default="pendiente"),
        sa.Column("total_registros", sa.Integer(), server_default="0", nullable=True),
        sa.Column("registros_exitosos", sa.Integer(), server_default="0", nullable=True),
        sa.Column("registros_con_error", sa.Integer(), server_default="0", nullable=True),
        sa.Column("ruta_archivo", sa.Text(), nullable=True),
        sa.Column("usuario_carga", sa.String(100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("hash_archivo", name="uq_hash"),
        sa.CheckConstraint(
            "estado IN ('pendiente', 'procesando', 'completado', 'error')",
            name="ck_estado",
        ),
    )
    op.create_index("idx_archivo_nombre", "archivo_procesado", ["nombre_archivo"], unique=False)
    op.create_index("idx_archivo_fecha_carga", "archivo_procesado", ["fecha_carga"], unique=False)
    op.create_index("idx_archivo_estado", "archivo_procesado", ["estado"], unique=False)

    op.create_table(
        "tipo_autoconsumo",
        sa.Column("codigo", sa.Integer(), nullable=False),
        sa.Column("descripcion", sa.String(255), nullable=False),
        sa.Column("activo", sa.Boolean(), server_default="true", nullable=True),
        sa.PrimaryKeyConstraint("codigo"),
    )
    op.execute("""
        INSERT INTO tipo_autoconsumo (codigo, descripcion, activo) VALUES
        (12, 'Autoconsumo tipo 12', true),
        (41, 'Autoconsumo tipo 41', true),
        (42, 'Autoconsumo tipo 42', true),
        (43, 'Autoconsumo tipo 43', true),
        (51, 'Autoconsumo tipo 51', true)
        ON CONFLICT (codigo) DO NOTHING
    """)

    op.create_table(
        "energia_excedentaria",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("archivo_id", sa.Integer(), nullable=False),
        sa.Column("linea_archivo", sa.Integer(), nullable=False),
        sa.Column("cups_cliente", sa.String(20), nullable=False),
        sa.Column("instalacion_gen", sa.String(50), nullable=False),
        sa.Column("fecha_desde", sa.Date(), nullable=False),
        sa.Column("fecha_hasta", sa.Date(), nullable=False),
        sa.Column("tipo_autoconsumo", sa.Integer(), nullable=False),
        sa.Column("energia_neta_gen", sa.ARRAY(sa.Numeric(12, 3)), nullable=False),
        sa.Column("energia_autoconsumida", sa.ARRAY(sa.Numeric(12, 3)), nullable=False),
        sa.Column("pago_tda", sa.ARRAY(sa.Numeric(12, 2)), nullable=False),
        sa.Column("fecha_creacion", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["archivo_id"], ["archivo_procesado.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tipo_autoconsumo"], ["tipo_autoconsumo.codigo"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("archivo_id", "cups_cliente", "instalacion_gen", "fecha_desde", name="uq_archivo_cups_instalacion"),
        sa.CheckConstraint("fecha_hasta >= fecha_desde", name="ck_fechas_validas"),
    )
    op.create_index("idx_energia_cups", "energia_excedentaria", ["cups_cliente"], unique=False)
    op.create_index("idx_energia_fechas", "energia_excedentaria", ["fecha_desde", "fecha_hasta"], unique=False)
    op.create_index("idx_energia_tipo", "energia_excedentaria", ["tipo_autoconsumo"], unique=False)
    op.create_index("idx_energia_archivo", "energia_excedentaria", ["archivo_id"], unique=False)

    op.create_table(
        "registro_errores",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("archivo_id", sa.Integer(), nullable=False),
        sa.Column("linea_archivo", sa.Integer(), nullable=False),
        sa.Column("tipo_error", sa.String(50), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=False),
        sa.Column("datos_linea", sa.Text(), nullable=True),
        sa.Column("fecha_registro", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["archivo_id"], ["archivo_procesado.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint(
            "tipo_error IN ("
            "'cliente_inexistente', 'tipo_no_soportado', 'formato_invalido', "
            "'archivo_duplicado', 'inconsistencia_numerica', "
            "'array_longitud_invalida', 'fecha_invalida')",
            name="ck_tipo_error",
        ),
    )
    op.create_index("idx_error_archivo", "registro_errores", ["archivo_id"], unique=False)
    op.create_index("idx_error_tipo", "registro_errores", ["tipo_error"], unique=False)
    op.create_index("idx_error_linea", "registro_errores", ["archivo_id", "linea_archivo"], unique=False)


def downgrade() -> None:
    op.drop_index("idx_error_linea", "registro_errores")
    op.drop_index("idx_error_tipo", "registro_errores")
    op.drop_index("idx_error_archivo", "registro_errores")
    op.drop_table("registro_errores")
    op.drop_index("idx_energia_archivo", "energia_excedentaria")
    op.drop_index("idx_energia_tipo", "energia_excedentaria")
    op.drop_index("idx_energia_fechas", "energia_excedentaria")
    op.drop_index("idx_energia_cups", "energia_excedentaria")
    op.drop_table("energia_excedentaria")
    op.drop_table("tipo_autoconsumo")
    op.drop_index("idx_archivo_estado", "archivo_procesado")
    op.drop_index("idx_archivo_fecha_carga", "archivo_procesado")
    op.drop_index("idx_archivo_nombre", "archivo_procesado")
    op.drop_table("archivo_procesado")
