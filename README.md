[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/_qskZYud)
# Práctica Python + MySQL: sti_incidencias (versión alumnado)

## Objetivo
Implementar funciones en Python para conectarse a una base de datos MySQL/MariaDB (XAMPP) y realizar operaciones
básicas sobre el sistema de incidencias `sti_incidencias`.

El proyecto incluye:
- Estructura de carpetas.
- Un _main_ para probar por consola.
- Tests unitarios/integración con `pytest`.

**Importante:** los ficheros en `src/sti_incidencias/` contienen funciones con `NotImplementedError`.
Deben completarse siguiendo los docstrings y haciendo que los tests pasen.

## Requisitos
- XAMPP con MySQL/MariaDB arrancado.
- Base de datos `sti_incidencias` creada en la práctica anterior (tablas: `tecnicos`, `equipos`, `incidencias`).
- Python 3.10+ (recomendado).

## Instalación
```bash
pip install -r requirements.txt
```

## Configuración (variables de entorno)
Configura en tu sistema/IDE (o terminal) las siguientes variables:
- DB_HOST=localhost
- DB_PORT=3306
- DB_NAME=sti_incidencias
- DB_USER=sti_app
- DB_PASSWORD=sti_app_2026

Referencia: `.env.example` (no se carga automáticamente).

## Ejecutar el programa
```bash
python -m sti_incidencias
```

## Ejecutar tests
Los tests intentan conectarse a la base de datos usando variables de entorno. Si no están definidas o no hay conexión,
los tests se marcarán como omitidos (SKIP).

```bash
pytest -q
```
