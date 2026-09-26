# modulo_7/laboratorio.py

import asyncio
import logging
from pathlib import Path

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

# =========================================================================
# Configuración del logger
# =========================================================================
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8080"


# =========================================================================
# Timeouts
# =========================================================================
TIMEOUT = httpx.Timeout(
    connect=3.0,
    read=5.0,
    write=3.0,
    pool=2.0,
)


# =========================================================================
# GET con reintentos
# =========================================================================
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=1, max=10),
)
def obtener_usuario(id: int) -> dict:
    logger.info(f"Obteniendo usuario {id}...")
    respuesta = httpx.get(
        f"{BASE_URL}/usuarios/{id}",
        timeout=TIMEOUT,
    )
    respuesta.raise_for_status()
    usuario = respuesta.json()
    logger.info(f"✅ Usuario obtenido: {usuario}")
    return usuario


# =========================================================================
# Streaming — descargar archivo a disco
# =========================================================================
def descargar_archivo(destino: Path) -> None:
    logger.info(f"Iniciando descarga por streaming -> {destino}")
    url = f"{BASE_URL}/archivo"

    with httpx.stream("GET", url, timeout=TIMEOUT) as respuesta:
        respuesta.raise_for_status()

        total = int(respuesta.headers.get("content-length", 0))
        descargado = 0

        with destino.open("wb") as f:
            for chunk in respuesta.iter_bytes(chunk_size=8192):
                f.write(chunk)
                descargado += len(chunk)
                if total:
                    porcentaje = (descargado / total) * 100
                    logger.debug(f"Progreso: {porcentaje:.1f}%")

    logger.info(f"✅ Archivo descargado: {destino}")


# =========================================================================
# Async — múltiples peticiones en paralelo
# =========================================================================
async def obtener_usuarios_async(ids: list[int]) -> list[dict]:
    logger.info(f"Obteniendo {len(ids)} usuarios en paralelo...")

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        tareas = [client.get(f"{BASE_URL}/usuarios/{id}") for id in ids]
        respuestas = await asyncio.gather(*tareas, return_exceptions=True)

    usuarios = []
    for i, resultado in enumerate(respuestas):
        if isinstance(resultado, BaseException):
            logger.error(f"❌ Error usuario {ids[i]}: {resultado}")
        elif isinstance(resultado, httpx.Response):
            usuario = resultado.json()
            logger.info(f"✅ Usuario {ids[i]}: {usuario}")
            usuarios.append(usuario)

    return usuarios


# =========================================================================
# Manejo de errores
# =========================================================================
def demo_errores() -> None:
    logger.info("=== Demo manejo de errores ===")

    try:
        respuesta = httpx.get(
            f"{BASE_URL}/ruta_inexistente",
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except httpx.TimeoutException:
        logger.error("❌ Timeout — la petición tardó demasiado")
    except httpx.HTTPStatusError as e:
        logger.error(f"❌ Error HTTP {e.response.status_code}")
    except httpx.RequestError as e:
        logger.error(f"❌ Error de conexión: {e}")


# =========================================================================
# Main
# =========================================================================
def main() -> None:
    logger.info("=== Iniciando laboratorio módulo 7 ===")

    carpeta = Path("modulo_7") / "resultados"
    carpeta.mkdir(parents=True, exist_ok=True)

    logger.info("=== GET con reintentos ===")
    obtener_usuario(1)

    logger.info("=== Descarga por streaming ===")
    descargar_archivo(carpeta / "archivo_descargado.txt")

    logger.info("=== Peticiones async ===")
    asyncio.run(obtener_usuarios_async([1, 1, 1]))

    demo_errores()

    logger.info("=== Laboratorio finalizado ===")


if __name__ == "__main__":
    main()
