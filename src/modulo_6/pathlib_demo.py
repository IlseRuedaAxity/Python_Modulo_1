# modulo_6/pathlib_demo.py

from pathlib import Path


def main() -> None:
    # =========================================================================
    # Rutas básicas
    # =========================================================================
    ruta_actual = Path.cwd()
    print(f"Ruta actual: {ruta_actual}")

    # =========================================================================
    # Crear carpeta de resultados
    # =========================================================================
    carpeta = Path("modulo_6") / "resultados"
    carpeta.mkdir(parents=True, exist_ok=True)
    print(f"Carpeta creada: {carpeta}")

    # =========================================================================
    # Escribir un archivo
    # =========================================================================
    archivo = carpeta / "datos.txt"
    archivo.write_text("Hola, mundo!\nSegunda línea", encoding="utf-8")
    print(f"Archivo creado: {archivo}")

    # =========================================================================
    # Leer un archivo
    # =========================================================================
    contenido = archivo.read_text(encoding="utf-8")
    print(f"Contenido:\n{contenido}")

    # =========================================================================
    # Verificar existencia
    # =========================================================================
    print(f"¿Existe?: {archivo.exists()}")
    print(f"¿Es archivo?: {archivo.is_file()}")
    print(f"¿Es carpeta?: {archivo.is_dir()}")

    # =========================================================================
    # Información de la ruta
    # =========================================================================
    print(f"Nombre: {archivo.name}")
    print(f"Sin extensión: {archivo.stem}")
    print(f"Extensión: {archivo.suffix}")
    print(f"Carpeta padre: {archivo.parent}")


if __name__ == "__main__":
    main()
