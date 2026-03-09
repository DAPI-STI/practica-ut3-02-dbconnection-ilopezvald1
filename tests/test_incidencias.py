import pytest

from src.incidencias import (
    asignar_tecnico,
    cerrar_incidencia,
    crear_incidencia,
    listar_incidencias_activas,
    listar_incidencias_sin_tecnico,
)

TEST_DESC = "[TEST] Incidencia creada por pytest"


def _get_any_equipo_id(conn) -> int:
    cur = conn.cursor()
    cur.execute("SELECT id FROM equipos LIMIT 1;")
    row = cur.fetchone()
    cur.close()
    if row is None:
        pytest.skip("No hay equipos en la BD. Inserta datos en la práctica anterior.")
    return int(row[0])


def _get_any_tecnico_id(conn) -> int:
    cur = conn.cursor()
    cur.execute("SELECT id FROM tecnicos LIMIT 1;")
    row = cur.fetchone()
    cur.close()
    if row is None:
        pytest.skip("No hay técnicos en la BD. Inserta datos en la práctica anterior.")
    return int(row[0])


def _get_last_test_incidencia_id(conn) -> int | None:
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM incidencias WHERE descripcion = %s ORDER BY id DESC LIMIT 1;",
        (TEST_DESC,),
    )
    row = cur.fetchone()
    cur.close()
    return int(row[0]) if row else None


def _cleanup_test_incidencias(conn) -> None:
    cur = conn.cursor()
    cur.execute("DELETE FROM incidencias WHERE descripcion = %s;", (TEST_DESC,))
    conn.commit()
    cur.close()


def test_crear_y_listar_sin_tecnico(conn):
    _cleanup_test_incidencias(conn)

    equipo_id = _get_any_equipo_id(conn)
    n = crear_incidencia(conn, equipo_id, TEST_DESC, "media")
    assert n == 1

    sin_tecnico = listar_incidencias_sin_tecnico(conn)
    assert any(r["descripcion"] == TEST_DESC for r in sin_tecnico)

    _cleanup_test_incidencias(conn)


def test_asignar_y_cerrar(conn):
    _cleanup_test_incidencias(conn)

    equipo_id = _get_any_equipo_id(conn)
    tecnico_id = _get_any_tecnico_id(conn)

    assert crear_incidencia(conn, equipo_id, TEST_DESC, "alta") == 1
    inc_id = _get_last_test_incidencia_id(conn)
    assert inc_id is not None

    n = asignar_tecnico(conn, inc_id, tecnico_id)
    assert n == 1

    activas = listar_incidencias_activas(conn)
    row = next(r for r in activas if r["id"] == inc_id)
    assert row["tecnico_id"] == tecnico_id
    assert row["estado"] in {"en_proceso", "abierta"}

    n2 = cerrar_incidencia(conn, inc_id)
    assert n2 == 1

    activas2 = listar_incidencias_activas(conn)
    assert not any(r["id"] == inc_id for r in activas2)

    _cleanup_test_incidencias(conn)


def test_validaciones(conn):
    equipo_id = _get_any_equipo_id(conn)

    with pytest.raises(ValueError):
        crear_incidencia(conn, equipo_id, "   ", "media")

    with pytest.raises(ValueError):
        crear_incidencia(conn, equipo_id, "ok", "urgente")

    with pytest.raises(ValueError):
        asignar_tecnico(conn, 0, 1)

    with pytest.raises(ValueError):
        cerrar_incidencia(conn, -1)
