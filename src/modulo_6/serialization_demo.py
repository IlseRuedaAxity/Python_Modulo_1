# modulo_6/serialization_demo.py

import csv
import json
from pathlib import Path

import yaml


# =========================================================================
# CSV
# =========================================================================
def demo_csv() -> None:
    archivo = Path("modulo_6") / "resultados" / "usuarios.csv"

    usuarios = [
        {"nombre": "Ana", "edad": 30, "ciudad": "CDMX"},
        {"nombre": "Juan", "edad": 25, "ciudad": "GDL"},
        {"nombre": "Maria", "edad": 28, "ciudad": "MTY"},
    ]

    # Escribir
    with archivo.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nombre", "edad", "ciudad"])
        writer.writeheader()
        writer.writerows(usuarios)
    print(f"CSV creado: {archivo}")

    # Leer
    print("\nLeyendo CSV:")
    with archivo.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            print(fila)


# =========================================================================
# JSON
# =========================================================================
def demo_json() -> None:
    archivo = Path("modulo_6") / "resultados" / "usuarios.json"

    usuarios = [
        {"nombre": "Ana", "edad": 30, "ciudad": "CDMX"},
        {"nombre": "Juan", "edad": 25, "ciudad": "GDL"},
        {"nombre": "Maria", "edad": 28, "ciudad": "MTY"},
    ]

    # Escribir
    with archivo.open("w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
    print(f"\nJSON creado: {archivo}")

    # Leer
    print("\nLeyendo JSON:")
    with archivo.open("r", encoding="utf-8") as f:
        datos = json.load(f)
        for usuario in datos:
            print(usuario)


# =========================================================================
# YAML
# =========================================================================
def demo_yaml() -> None:
    archivo = Path("modulo_6") / "resultados" / "usuarios.yaml"

    usuarios = [
        {"nombre": "Ana", "edad": 30, "ciudad": "CDMX"},
        {"nombre": "Juan", "edad": 25, "ciudad": "GDL"},
        {"nombre": "Maria", "edad": 28, "ciudad": "MTY"},
    ]

    # Escribir
    with archivo.open("w", encoding="utf-8") as f:
        yaml.dump(usuarios, f, allow_unicode=True, default_flow_style=False)
    print(f"\nYAML creado: {archivo}")

    # Leer
    print("\nLeyendo YAML:")
    with archivo.open("r", encoding="utf-8") as f:
        datos = yaml.safe_load(f)
        for usuario in datos:
            print(usuario)


# =========================================================================
# Main
# =========================================================================
def main() -> None:
    # Asegurar que la carpeta existe
    carpeta = Path("modulo_6") / "resultados"
    carpeta.mkdir(parents=True, exist_ok=True)

    demo_csv()
    demo_json()
    demo_yaml()


if __name__ == "__main__":
    main()
