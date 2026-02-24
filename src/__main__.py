from __future__ import annotations

from db import get_connection
from incidencias import (
    asignar_tecnico,
    cerrar_incidencia,
    crear_incidencia,
    detalle_incidencias_join,
    listar_incidencias_activas,
    listar_incidencias_sin_tecnico,
)


def main() -> None:
    """Menú de consola simple para probar las funciones de acceso a BD."""
    conn = get_connection()
    try:
        while True:
            print("\n=== STI Incidencias ===")
            print("1) Listar incidencias activas")
            print("2) Listar incidencias sin técnico")
            print("3) Crear incidencia")
            print("4) Asignar técnico")
            print("5) Cerrar incidencia")
            print("6) Vista JOIN (detalle)")
            print("0) Salir")
            op = input("Opción: ").strip()

            if op == "0":
                break

            if op == "1":
                rows = listar_incidencias_activas(conn)
                for r in rows:
                    print(r)

            elif op == "2":
                rows = listar_incidencias_sin_tecnico(conn)
                for r in rows:
                    print(r)

            elif op == "3":
                equipo_id = int(input("equipo_id: ").strip())
                descripcion = input("descripcion: ").strip()
                prioridad = input("prioridad (baja/media/alta) [media]: ").strip() or "media"
                n = crear_incidencia(conn, equipo_id, descripcion, prioridad)
                print(f"Incidencia creada (filas afectadas: {n}).")

            elif op == "4":
                incidencia_id = int(input("incidencia_id: ").strip())
                tecnico_id = int(input("tecnico_id: ").strip())
                n = asignar_tecnico(conn, incidencia_id, tecnico_id)
                print(f"Asignación realizada (filas afectadas: {n}).")

            elif op == "5":
                incidencia_id = int(input("incidencia_id: ").strip())
                n = cerrar_incidencia(conn, incidencia_id)
                print(f"Cierre realizado (filas afectadas: {n}).")

            elif op == "6":
                rows = detalle_incidencias_join(conn)
                for r in rows:
                    print(r)

            else:
                print("Opción no válida.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
