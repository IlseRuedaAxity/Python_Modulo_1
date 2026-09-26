import json
from pathlib import Path


def cargar_datos(ruta_archivo: str | Path) -> list[dict] | None:
    try:
        with open(ruta_archivo, encoding="utf-8") as f:
            datos = json.load(f)
        return datos
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_archivo}")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo {ruta_archivo} no tiene formato JSON válido")
        return None


def filtrar_mayores(datos: list[dict], edad_minima: int = 18) -> list[dict]:
    return [usuario for usuario in datos if usuario.get("edad", 0) >= edad_minima]


def main() -> None:
    datos = cargar_datos("usuarios.json")
    if datos is None:
        return

    mayores = filtrar_mayores(datos)
    print(f"Número de usuarios mayores de 18 años: {len(mayores)}")

    for usuario in mayores:
        print(usuario.get("nombre", "Nombre no disponible"))


if __name__ == "__main__":
    main()
