# modulo_6/datetime_demo.py

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo


# =========================================================================
# Fecha y hora actual
# =========================================================================
def demo_basico() -> None:
    print("=== Básico ===")

    # Fecha y hora completa
    ahora = datetime.now()
    print(f"Ahora:     {ahora}")

    # Solo fecha
    hoy = date.today()
    print(f"Hoy:       {hoy}")

    # Solo hora
    hora = datetime.now().time()
    print(f"Hora:      {hora}")

    # Fecha específica
    fecha = datetime(2024, 1, 15, 10, 30, 0)
    print(f"Específica: {fecha}")


# =========================================================================
# Formatear fechas
# =========================================================================
def demo_formato() -> None:
    print("\n=== Formatos ===")

    ahora = datetime.now()

    # strftime — datetime a string
    print(ahora.strftime("%d/%m/%Y"))
    print(ahora.strftime("%d/%m/%Y %H:%M:%S"))
    print(ahora.strftime("%Y-%m-%d"))

    # strptime — string a datetime
    fecha = datetime.strptime("15/01/2024", "%d/%m/%Y")
    print(f"Parseada: {fecha}")


# =========================================================================
# Zonas horarias
# =========================================================================
def demo_zonas() -> None:
    print("\n=== Zonas Horarias ===")

    # Sin zona horaria
    sin_zona = datetime.now()
    print(f"Sin zona:  {sin_zona}")

    # Con zona horaria
    cdmx = datetime.now(ZoneInfo("America/Mexico_City"))
    print(f"CDMX:      {cdmx.strftime('%d/%m/%Y %H:%M:%S %Z')}")

    # Convertir zonas
    madrid = cdmx.astimezone(ZoneInfo("Europe/Madrid"))
    print(f"Madrid:    {madrid.strftime('%d/%m/%Y %H:%M:%S %Z')}")

    nueva_york = cdmx.astimezone(ZoneInfo("America/New_York"))
    print(f"NY:        {nueva_york.strftime('%d/%m/%Y %H:%M:%S %Z')}")


# =========================================================================
# Operaciones con fechas
# =========================================================================
def demo_operaciones() -> None:
    print("\n=== Operaciones ===")

    ahora = datetime.now(ZoneInfo("America/Mexico_City"))

    # Sumar y restar días
    manana = ahora + timedelta(days=1)
    ayer = ahora - timedelta(days=1)
    print(f"Ayer:      {ayer.strftime('%d/%m/%Y')}")
    print(f"Hoy:       {ahora.strftime('%d/%m/%Y')}")
    print(f"Mañana:    {manana.strftime('%d/%m/%Y')}")

    # Diferencia entre fechas
    inicio = datetime(2024, 1, 1, tzinfo=ZoneInfo("America/Mexico_City"))
    diferencia = ahora - inicio
    print(f"Días desde 01/01/2024: {diferencia.days}")


# =========================================================================
# Main
# =========================================================================
def main() -> None:
    demo_basico()
    demo_formato()
    demo_zonas()
    demo_operaciones()


if __name__ == "__main__":
    main()
