# modulo_6/laboratorio.py

import csv
import json
import logging
from pathlib import Path


# =========================================================================
# Configuración del logger
# =========================================================================
def configurar_logging() -> None:
    carpeta = Path("modulo_6") / "resultados"
    carpeta.mkdir(parents=True, exist_ok=True)

    archivo_log = carpeta / "laboratorio.log"

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(archivo_log, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


logger = logging.getLogger(__name__)


# =========================================================================
# Crear CSV de ejemplo
# =========================================================================
def crear_csv_ejemplo() -> Path:
    archivo = Path("modulo_6") / "resultados" / "ventas.csv"

    ventas = [
        {
            "producto": "Laptop",
            "categoria": "Electronica",
            "precio": 1500.0,
            "cantidad": 3,
        },
        {
            "producto": "Mouse",
            "categoria": "Electronica",
            "precio": 25.0,
            "cantidad": 10,
        },
        {
            "producto": "Teclado",
            "categoria": "Electronica",
            "precio": 75.0,
            "cantidad": 8,
        },
        {"producto": "Silla", "categoria": "Muebles", "precio": 300.0, "cantidad": 5},
        {
            "producto": "Escritorio",
            "categoria": "Muebles",
            "precio": 450.0,
            "cantidad": 2,
        },
        {
            "producto": "Libreta",
            "categoria": "Papeleria",
            "precio": 5.0,
            "cantidad": 50,
        },
        {"producto": "Pluma", "categoria": "Papeleria", "precio": 2.0, "cantidad": 100},
    ]

    with archivo.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["producto", "categoria", "precio", "cantidad"]
        )
        writer.writeheader()
        writer.writerows(ventas)

    logger.info(f"CSV de ejemplo creado: {archivo}")
    return archivo


# =========================================================================
# Ingesta de CSV
# =========================================================================
def ingestar_csv(archivo: Path) -> list[dict[str, str | float | int]]:
    logger.info(f"Iniciando ingesta de CSV: {archivo}")

    if not archivo.exists():
        logger.error(f"El archivo no existe: {archivo}")
        return []

    datos: list[dict[str, str | float | int]] = []

    with archivo.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            try:
                datos.append(
                    {
                        "producto": fila["producto"],
                        "categoria": fila["categoria"],
                        "precio": float(fila["precio"]),
                        "cantidad": int(fila["cantidad"]),
                    }
                )
                logger.debug(f"Fila leída: {fila['producto']}")
            except (ValueError, KeyError) as e:
                logger.warning(f"Fila inválida ignorada: {fila} — Error: {e}")

    logger.info(f"Ingesta completada: {len(datos)} registros leídos")
    return datos


# =========================================================================
# Calcular métricas
# =========================================================================
def calcular_metricas(
    datos: list[dict[str, str | float | int]],
) -> dict[str, float | int | dict[str, float]]:
    logger.info("Calculando métricas...")

    if not datos:
        logger.error("No hay datos para calcular métricas")
        return {}

    # Métricas generales
    precios = [float(d["precio"]) for d in datos]
    cantidades = [int(d["cantidad"]) for d in datos]
    totales = [float(d["precio"]) * int(d["cantidad"]) for d in datos]

    # Métricas por categoría
    categorias: dict[str, float] = {}
    for d in datos:
        categoria = str(d["categoria"])
        total = float(d["precio"]) * int(d["cantidad"])
        categorias[categoria] = categorias.get(categoria, 0) + total

    metricas: dict[str, float | int | dict[str, float]] = {
        "total_productos": len(datos),
        "precio_promedio": round(sum(precios) / len(precios), 2),
        "precio_maximo": max(precios),
        "precio_minimo": min(precios),
        "cantidad_total": sum(cantidades),
        "venta_total": round(sum(totales), 2),
        "venta_por_categoria": categorias,
    }

    logger.debug(f"Métricas calculadas: {metricas}")
    logger.info(f"Total productos: {metricas['total_productos']}")
    logger.info(f"Venta total: ${metricas['venta_total']}")

    return metricas


# =========================================================================
# Exportar métricas a JSON
# =========================================================================
def exportar_json(
    metricas: dict[str, float | int | dict[str, float]],
) -> None:
    if not metricas:
        logger.error("No hay métricas para exportar")
        return

    archivo = Path("modulo_6") / "resultados" / "metricas.json"

    with archivo.open("w", encoding="utf-8") as f:
        json.dump(metricas, f, indent=4, ensure_ascii=False)

    logger.info(f"Métricas exportadas a JSON: {archivo}")


# =========================================================================
# Main
# =========================================================================
def main() -> None:
    configurar_logging()

    logger.info("=== Iniciando laboratorio módulo 6 ===")

    # 1. Crear CSV de ejemplo
    archivo_csv = crear_csv_ejemplo()

    # 2. Ingestar CSV
    datos = ingestar_csv(archivo_csv)

    if not datos:
        logger.critical("No se pudieron leer datos, abortando")
        return

    # 3. Calcular métricas
    metricas = calcular_metricas(datos)

    # 4. Exportar a JSON
    exportar_json(metricas)

    logger.info("=== Laboratorio finalizado exitosamente ===")


if __name__ == "__main__":
    main()
