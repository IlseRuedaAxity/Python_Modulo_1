# modulo_5/type_hints.py

from collections.abc import Callable
from typing import Generic, Literal, NotRequired, Protocol, TypedDict, TypeVar

# =============================================================================
# BÁSICO — anotaciones simples
# =============================================================================

nombre: str = "Ana"
edad: int = 30
activo: bool = True
precio: float = 9.99


def saludar(nombre: str, veces: int = 1) -> str:
    return f"Hola {nombre}" * veces


# =============================================================================
# Union — acepta más de un tipo
# =============================================================================


# Python 3.9 o anterior
def procesar_union(valor: int | str) -> str:
    return str(valor)


# Python 3.10+ (forma moderna con |)
def procesar_moderno(valor: int | str) -> str:
    return str(valor)


# =============================================================================
# Literal — valores exactos permitidos
# =============================================================================

Rol = Literal["admin", "editor", "viewer"]


def asignar_rol(usuario: str, rol: Rol) -> None:
    print(f"{usuario} tiene rol: {rol}")


asignar_rol("Ana", "admin")
# asignar_rol("Ana", "superuser")  # ❌ mypy lo detecta


# =============================================================================
# TypedDict — diccionarios con estructura fija
# =============================================================================


class Producto(TypedDict):
    nombre: str
    precio: float
    disponible: bool


item: Producto = {
    "nombre": "Laptop",
    "precio": 1500.0,
    "disponible": True,
}


# Con campos opcionales
class ProductoOpcional(TypedDict):
    nombre: str
    precio: float
    descripcion: NotRequired[str]


# =============================================================================
# Protocol — duck typing con tipos (interfaces implícitas)
# =============================================================================


class Guardable(Protocol):
    def guardar(self) -> bool: ...
    def eliminar(self, id: int) -> None: ...


class RepositorioSQL:
    def guardar(self) -> bool:
        return True

    def eliminar(self, id: int) -> None:
        print(f"Eliminado {id}")


class RepositorioMemoria:
    def guardar(self) -> bool:
        return True

    def eliminar(self, id: int) -> None:
        print(f"Eliminado de memoria {id}")


def persistir(repo: Guardable) -> None:
    repo.guardar()


# =============================================================================
# Tipos avanzados adicionales
# =============================================================================


# Optional moderno = X | None
def buscar(id: int) -> str | None:
    return None


# Callable — funciones como parámetros
def ejecutar(fn: Callable[[int, str], bool]) -> bool:
    return fn(1, "test")


# TypeVar — genéricos (sintaxis compatible con mypy)
T = TypeVar("T")  # noqa: UP046


def primero(lista: list[T]) -> T:  # noqa: UP047
    return lista[0]


# Generic — clases genéricas (sintaxis compatible con mypy)
class Caja(Generic[T]):  # noqa: UP046
    def __init__(self, contenido: T) -> None:
        self.contenido = contenido

    def abrir(self) -> T:
        return self.contenido


caja_int: Caja[int] = Caja(42)
caja_str: Caja[str] = Caja("hola")
