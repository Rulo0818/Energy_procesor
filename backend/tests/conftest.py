import pytest
from unittest.mock import MagicMock

# Tests unitarios de validación no necesitan BD real (validar_cups_existe está simulado).


@pytest.fixture
def db_session():
    """Sesión mock para tests de validación (validar_linea no usa BD real para CUPS)."""
    return MagicMock()


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from app.main import app
    from app.api.deps import get_db

    def override_get_db():
        session = MagicMock()
        # GET /energia: query().filter().all() -> []
        q = MagicMock()
        q.filter.return_value = q
        q.order_by.return_value = q
        q.all.return_value = []
        q.first.return_value = None
        session.query.return_value = q
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
