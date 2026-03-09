import os
import pytest

from src.db import get_connection
from dotenv import load_dotenv
load_dotenv()


def _db_config_present() -> bool:
    # Para ejecutar tests de BD se requiere configuración explícita.
    return bool(os.getenv("DB_USER")) and bool(os.getenv("DB_PASSWORD"))


@pytest.fixture(scope="session")
def conn():
    if not _db_config_present():
        pytest.skip("Tests de BD omitidos: define DB_USER y DB_PASSWORD en variables de entorno.")

    try:
        c = get_connection()
    except Exception as e:
        pytest.skip(f"Tests de BD omitidos: no se pudo conectar ({e}). ¿XAMPP/MySQL encendido?")

    yield c
    c.close()
