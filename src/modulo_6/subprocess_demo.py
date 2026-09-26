# modulo_6/subprocess_demo.py

import logging
import subprocess
from pathlib import Path

# =========================================================================
# Configuración del logger
# =========================================================================
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


# =========================================================================
# Ejecutar comando simple
# =========================================================================
def demo_basico() -> None:
    logger.info("=== Comando básico ===")

    resultado = subprocess.run(
        ["python", "--version"],
        capture_output=True,
        text=True,
    )

    if resultado.returncode == 0:
        logger.info(f"✅ Python version: {resultado.stdout.strip()}")
    else:
        logger.error(f"❌ Error: {resultado.stderr.strip()}")


# =========================================================================
# Ejecutar pip list
# =========================================================================
def demo_pip() -> None:
    logger.info("=== Paquetes instalados ===")

    resultado = subprocess.run(
        ["pip", "list"],
        capture_output=True,
        text=True,
    )

    if resultado.returncode == 0:
        # Mostrar solo los primeros 5 paquetes
        paquetes = resultado.stdout.strip().split("\n")[:5]
        for paquete in paquetes:
            logger.info(paquete)
    else:
        logger.error(f"❌ Error: {resultado.stderr.strip()}")


# =========================================================================
# Listar archivos de una carpeta
# =========================================================================
def demo_listar_carpeta(carpeta: Path) -> None:
    logger.info(f"=== Listando carpeta: {carpeta} ===")

    resultado = subprocess.run(
        ["dir", str(carpeta)],
        capture_output=True,
        text=True,
        shell=True,
    )

    if resultado.returncode == 0:
        logger.info(resultado.stdout.strip())
    else:
        logger.error(f"❌ Error: {resultado.stderr.strip()}")


# =========================================================================
# Comando con error
# =========================================================================
def demo_error() -> None:
    logger.info("=== Comando con error ===")

    resultado = subprocess.run(
        ["comando_inexistente"],
        capture_output=True,
        text=True,
        shell=True,
    )

    if resultado.returncode != 0:
        logger.error(f"❌ Comando falló con código: {resultado.returncode}")


# =========================================================================
# Comando con timeout
# =========================================================================
def demo_timeout() -> None:
    logger.info("=== Comando con timeout ===")

    try:
        resultado = subprocess.run(
            ["ping", "google.com", "-n", "3"],
            capture_output=True,
            text=True,
            timeout=10,
            shell=True,
        )
        logger.info(f"✅ Ping exitoso:\n{resultado.stdout.strip()}")
    except subprocess.TimeoutExpired:
        logger.error("❌ El comando tardó demasiado")


# =========================================================================
# Main
# =========================================================================
def main() -> None:
    logger.info("=== Iniciando subprocess_demo ===")

    demo_basico()
    demo_pip()
    demo_listar_carpeta(Path("modulo_6") / "resultados")
    demo_error()
    demo_timeout()

    logger.info("=== subprocess_demo finalizado ===")


if __name__ == "__main__":
    main()
