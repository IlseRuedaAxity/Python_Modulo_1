# modulo_6/logging_demo.py

import logging
from pathlib import Path


# =========================================================================
# Configuración del logger
# =========================================================================
def configurar_logging() -> None:
    carpeta = Path("modulo_6") / "resultados"
    carpeta.mkdir(parents=True, exist_ok=True)

    archivo_log = carpeta / "app.log"

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(archivo_log, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


# =========================================================================
# Logger por módulo
# =========================================================================
logger = logging.getLogger(__name__)


# =========================================================================
# Demo niveles
# =========================================================================
def demo_niveles() -> None:
    logger.debug("Esto es DEBUG — detalle para desarrollo")
    logger.info("Esto es INFO — todo va bien")
    logger.warning("Esto es WARNING — algo inesperado")
    logger.error("Esto es ERROR — algo salió mal")
    logger.critical("Esto es CRITICAL — error grave")


# =========================================================================
# Demo uso real
# =========================================================================
def procesar_usuario(nombre: str, edad: int) -> dict[str, str | int] | None:
    logger.info(f"Procesando usuario: {nombre}")

    if not nombre:
        logger.error("El nombre no puede estar vacío")
        return None

    if edad < 0 or edad > 120:
        logger.warning(f"Edad fuera de rango: {edad}")
        return None

    logger.debug(f"Usuario válido: {nombre}, {edad}")
    return {"nombre": nombre, "edad": edad}


# =========================================================================
# Main
# =========================================================================
def main() -> None:
    configurar_logging()

    logger.info("=== Iniciando aplicación ===")

    # Demo niveles
    demo_niveles()

    # Demo uso real
    logger.info("\n=== Procesando usuarios ===")
    procesar_usuario("Ana", 30)  # ✅ válido
    procesar_usuario("", 25)  # ❌ nombre vacío
    procesar_usuario("Juan", 150)  # ⚠️ edad fuera de rango
    procesar_usuario("Maria", 28)  # ✅ válido

    logger.info("=== Aplicación finalizada ===")


if __name__ == "__main__":
    main()
