from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.api.deps import get_db
from app.models import Cliente, EnergiaExcedentaria
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse, ClienteWithStats

router = APIRouter()


@router.get("/", response_model=List[ClienteResponse])
def get_clientes(
    skip: int = 0,
    limit: int = 100,
    activo: bool = None,
    municipio: str = None,
    provincia: str = None,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de clientes con paginación y filtros opcionales
    """
    query = db.query(Cliente)
    
    if activo is not None:
        query = query.filter(Cliente.activo == activo)
    
    if municipio:
        query = query.filter(Cliente.municipio.ilike(f"%{municipio}%"))
    
    if provincia:
        query = query.filter(Cliente.provincia.ilike(f"%{provincia}%"))
    
    clientes = query.offset(skip).limit(limit).all()
    return clientes


@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Obtener un cliente específico por ID
    """
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {cliente_id} no encontrado"
        )
    return cliente


@router.get("/cups/{cups}", response_model=ClienteResponse)
def get_cliente_by_cups(cups: str, db: Session = Depends(get_db)):
    """
    Obtener un cliente por su CUPS
    """
    cliente = db.query(Cliente).filter(Cliente.cups == cups).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con CUPS {cups} no encontrado"
        )
    return cliente


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo cliente
    """
    # Verificar si el CUPS ya existe
    existing_cups = db.query(Cliente).filter(Cliente.cups == cliente.cups).first()
    if existing_cups:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El CUPS {cliente.cups} ya está registrado"
        )
    
    # Crear nuevo cliente
    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un cliente existente
    """
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {cliente_id} no encontrado"
        )
    
    # Actualizar solo los campos proporcionados
    update_data = cliente.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cliente, field, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un cliente (soft delete - marcar como inactivo)
    """
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {cliente_id} no encontrado"
        )
    
    # Soft delete: marcar como inactivo
    db_cliente.activo = False
    db.commit()
    return None


@router.get("/stats/resumen")
def get_clientes_stats(db: Session = Depends(get_db)):
    """
    Obtener estadísticas de clientes
    """
    total = db.query(Cliente).count()
    activos = db.query(Cliente).filter(Cliente.activo == True).count()
    por_provincia = db.query(
        Cliente.provincia, 
        func.count(Cliente.id)
    ).group_by(Cliente.provincia).all()
    
    return {
        "total": total,
        "activos": activos,
        "inactivos": total - activos,
        "por_provincia": {prov: count for prov, count in por_provincia if prov}
    }


@router.get("/{cliente_id}/energia", response_model=ClienteWithStats)
def get_cliente_with_energia(cliente_id: int, db: Session = Depends(get_db)):
    """
    Obtener cliente con estadísticas de energía
    """
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {cliente_id} no encontrado"
        )
    
    # Obtener estadísticas de energía
    registros = db.query(EnergiaExcedentaria).filter(
        EnergiaExcedentaria.cliente_id == cliente_id
    ).all()
    
    total_registros = len(registros)
    
    # Calcular totales de energía
    total_generada = 0
    total_autoconsumida = 0
    total_pago = 0
    
    for registro in registros:
        if registro.energia_neta_gen:
            total_generada += sum(registro.energia_neta_gen)
        if registro.energia_autoconsumida:
            total_autoconsumida += sum(registro.energia_autoconsumida)
        if registro.pago_tda:
            total_pago += sum(registro.pago_tda)
    
    return {
        **cliente.__dict__,
        "total_registros": total_registros,
        "total_energia_generada": float(total_generada),
        "total_energia_autoconsumida": float(total_autoconsumida),
        "total_pago_tda": float(total_pago)
    }
