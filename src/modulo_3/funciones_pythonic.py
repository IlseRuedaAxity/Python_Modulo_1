import random
import time
from collections.abc import Callable, Generator, Iterator
from contextlib import contextmanager
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


# Decorador para reintentos con backoff exponencial
def reintentos(max_reintentos: int = 3, backoff: int = 1) -> Callable[[F], F]:
    def decorador(func: F) -> F:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            intentos = 0
            while intentos < max_reintentos:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    intentos += 1
                    print(f"Intento {intentos} fallido: {e}")
                    time.sleep(backoff * intentos)
            raise Exception("Máximos intentos alcanzados")

        return wrapper  # type: ignore[return-value]

    return decorador


# Función de ejemplo que falla aleatoriamente para probar el decorador
@reintentos(max_reintentos=5, backoff=2)
def funcion_que_falla() -> str:
    if random.random() < 0.7:
        raise ValueError("Error temporal simulado")
    return "Éxito"


# Generador que divide un iterable en lotes de tamaño fijo
def generador_por_lotes(iterable: list[Any], tamano_lote: int) -> Iterator[list[Any]]:
    for i in range(0, len(iterable), tamano_lote):
        yield iterable[i : i + tamano_lote]


# Context manager para medir el tiempo de ejecución de un bloque de código
@contextmanager
def temporizador() -> Generator[None, None, None]:
    inicio = time.time()
    yield
    fin = time.time()
    print(f"Tiempo transcurrido: {fin - inicio:.4f} segundos")


def main() -> None:
    print("Probando decorador de reintentos con backoff:")
    try:
        resultado = funcion_que_falla()
        print(f"Resultado: {resultado}")
    except Exception as e:
        print(f"Error final: {e}")

    print("\nProbando generador por lotes:")
    datos = list(range(1, 21))
    for lote in generador_por_lotes(datos, 5):
        print(lote)

    print("\nProbando context manager de temporización:")
    with temporizador():
        time.sleep(2)


if __name__ == "__main__":
    main()
