from __future__ import annotations

from mysql.connector.connection import MySQLConnection

from .db import execute, fetch_all


def listar_incidencias_activas(conn: MySQLConnection) -> list[dict]:
    """
    Devuelve incidencias cuyo estado NO sea 'cerrada'.

    Requisitos:
    - Debe devolver una lista de diccionarios (una fila por dict).
    - Debe ordenar primero por prioridad (alta > media > baja) y luego por fecha_apertura ascendente.
    - Debe usar fetch_all(conn, sql, params) para ejecutar el SELECT.

    Pista: se puede ordenar por prioridad usando CASE en SQL.
    """
    sql = """
        SELECT *
        FROM incidencias
        WHERE estado != 'cerrada'
        ORDER BY 
            CASE prioridad
                WHEN 'alta' THEN 1
                WHEN 'media' THEN 2
                WHEN 'baja' THEN 3
            END,
            fecha_apertura ASC
    """
    return fetch_all(conn, sql)


def listar_incidencias_sin_tecnico(conn: MySQLConnection) -> list[dict]:
    """
    Devuelve incidencias activas sin técnico asignado.

    Requisitos:
    - tecnico_id IS NULL
    - estado <> 'cerrada'
    - ordenar por fecha_apertura ascendente
    """
    sql = """
        SELECT *
        FROM incidencias
        WHERE tecnico_id IS NULL AND estado != 'cerrada'
        ORDER BY fecha_apertura ASC
    """
    return fetch_all(conn, sql)


def crear_incidencia(conn: MySQLConnection, equipo_id: int, descripcion: str, prioridad: str = "media") -> int:
    """
    Crea una incidencia nueva en estado 'abierta'.

    Validaciones:
    - descripcion no puede ser vacía ni solo espacios (ValueError)
    - prioridad debe ser 'baja', 'media' o 'alta' (ValueError)
    - equipo_id debe ser entero positivo (ValueError)

    Requisitos SQL:
    - INSERT en tabla incidencias
    - tecnico_id debe ser NULL
    - estado debe ser 'abierta'
    - fecha_apertura debe ser NOW()
    - fecha_cierre debe ser NULL

    Debe devolver el número de filas afectadas (normalmente 1).
    """
    if not isinstance(equipo_id, int) or equipo_id <= 0:
        raise ValueError("equipo_id debe ser un entero positivo")
    
    if not descripcion or not descripcion.strip():
        raise ValueError("La descripción no puede estar vacía")
    
    prioridades_validas = ['baja', 'media', 'alta']
    if prioridad not in prioridades_validas:
        raise ValueError(f"prioridad debe ser una de: {', '.join(prioridades_validas)}")
    sql = """
        INSERT INTO incidencias 
        (equipo_id, descripcion, prioridad, tecnico_id, estado, fecha_apertura, fecha_cierre)
        VALUES (%s, %s, %s, NULL, 'abierta', NOW(), NULL)
    """
    return execute(conn, sql, (equipo_id, descripcion.strip(), prioridad))
    


def asignar_tecnico(conn: MySQLConnection, incidencia_id: int, tecnico_id: int) -> int:
    """
    Asigna un técnico a una incidencia y la marca como 'en_proceso' si la incidencia no está cerrada.

    Validaciones:
    - incidencia_id y tecnico_id deben ser enteros positivos (ValueError)

    Requisitos:
    - UPDATE sobre incidencias
    - Solo debe actualizar si estado <> 'cerrada'
    - Debe devolver filas afectadas (0 si no existe o ya está cerrada)
    """
    if not isinstance(incidencia_id, int) or incidencia_id <= 0:
        raise ValueError("incidencia_id debe ser un entero positivo")
    
    if not isinstance(tecnico_id, int) or tecnico_id <= 0:
        raise ValueError("tecnico_id debe ser un entero positivo")
    sql = """
        UPDATE incidencias
        SET tecnico_id = %s, estado = 'en_proceso'
        WHERE id = %s AND estado != 'cerrada'
    """
    return execute(conn, sql, (tecnico_id, incidencia_id))


def cerrar_incidencia(conn: MySQLConnection, incidencia_id: int) -> int:
    """
    Cierra una incidencia.

    Validaciones:
    - incidencia_id debe ser entero positivo (ValueError)

    Requisitos:
    - UPDATE sobre incidencias
    - estado='cerrada'
    - fecha_cierre=NOW()
    - Solo debe cerrar si estado <> 'cerrada'
    - Devuelve filas afectadas
    """
    if not isinstance(incidencia_id, int) or incidencia_id <= 0:
        raise ValueError("incidencia_id debe ser un entero positivo")
    sql = """
        UPDATE incidencias
        SET estado = 'cerrada', fecha_cierre = NOW()
        WHERE id = %s AND estado != 'cerrada'
    """
    return execute(conn, sql, (incidencia_id,))



def detalle_incidencias_join(conn: MySQLConnection) -> list[dict]:
    """
    Devuelve una vista enriquecida con datos de equipo y técnico.

    Columnas mínimas esperadas:
    - i.id, i.descripcion, i.prioridad, i.estado, i.fecha_apertura, i.fecha_cierre
    - e.tipo, e.modelo, e.ubicacion, e.estado AS estado_equipo
    - t.nombre AS tecnico (puede ser NULL si no hay técnico)

    Requisitos:
    - JOIN equipos (obligatorio)
    - LEFT JOIN tecnicos (opcional)
    - Ordenar por estado, prioridad DESC, fecha_apertura ASC
    """
    sql = """
        SELECT 
            i.id, i.descripcion, i.prioridad, i.estado, 
            i.fecha_apertura, i.fecha_cierre,
            e.tipo, e.modelo, e.ubicacion, e.estado AS estado_equipo,
            t.nombre AS tecnico
        FROM incidencias i
        JOIN equipos e ON i.equipo_id = e.id
        LEFT JOIN tecnicos t ON i.tecnico_id = t.id
        ORDER BY 
            i.estado,
            CASE i.prioridad
                WHEN 'alta' THEN 1
                WHEN 'media' THEN 2
                WHEN 'baja' THEN 3
            END,
            i.fecha_apertura ASC
    """
    return fetch_all(conn, sql)
