from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Iterable, Optional

import mysql.connector
from mysql.connector.connection import MySQLConnection

from dotenv import load_dotenv
load_dotenv()


@dataclass(frozen=True)
class DBConfig:
    """Configuración de conexión a la base de datos."""
    host: str
    port: int
    database: str
    user: str
    password: str


def load_config_from_env() -> DBConfig:
    """
    Lee la configuración de conexión desde variables de entorno.

    Variables esperadas (con valores por defecto):
    - DB_HOST (default: localhost)
    - DB_PORT (default: 3306)
    - DB_NAME (default: sti_incidencias)
    - DB_USER (default: sti_app)
    - DB_PASSWORD (default: sti_app_2026)

    Debe devolver un objeto DBConfig correctamente construido.

    Recomendación:
    - Validar que DB_PORT sea un número entero.
    """
    try:
        port = int(os.getenv("DB_PORT", "3306"))
        return DBConfig(
            host=os.getenv("DB_HOST", "localhost"),
            port=port,
            database=os.getenv("DB_NAME", "sti_incidencias"),
            user=os.getenv("DB_USER", "sti_app"),
            password=os.getenv("DB_PASSWORD", "sti_app_2026"))
    except ValueError as e:
        logger.error("variable DB_PORT tiene que ser numero entero")
        raise e
    
    


def get_connection(cfg: Optional[DBConfig] = None) -> MySQLConnection:
    """
    Crea y devuelve una conexión MySQL/MariaDB.

    - Si cfg es None, debe llamar a load_config_from_env().
    - Debe usar mysql.connector.connect(...) con los parámetros de cfg.
    """
    if cfg is None:
        cfg = load_config_from_env()
    
    return mysql.connector.connect(
        host=cfg.host,
        port=cfg.port,
        database=cfg.database,
        user=cfg.user,
        password=cfg.password
    )
    


def fetch_all(conn: MySQLConnection, query: str, params: Optional[Iterable[Any]] = None) -> list[dict]:
    """
    Ejecuta una consulta SELECT y devuelve una lista de diccionarios (una fila -> un dict).

    Pistas:
    - Crear un cursor con conn.cursor(dictionary=True)
    - Ejecutar cur.execute(query, params o ())
    - Obtener filas con cur.fetchall()
    - Cerrar el cursor siempre (try/finally)
    """
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(query, params or ())
        return cur.fetchall()
    finally:
        cur.close()
    


def execute(conn: MySQLConnection, query: str, params: Optional[Iterable[Any]] = None) -> int:
    """
    Ejecuta una sentencia INSERT/UPDATE/DELETE y devuelve el número de filas afectadas.

    Pistas:
    - Crear un cursor normal conn.cursor()
    - Ejecutar cur.execute(query, params o ())
    - Hacer conn.commit()
    - Devolver cur.rowcount
    - Cerrar el cursor siempre (try/finally)
    """
    cur = conn.cursor()
    try:
        cur.execute(query, params or ())
        conn.commit()
        return cur.rowcount
    finally:
        cur.close()