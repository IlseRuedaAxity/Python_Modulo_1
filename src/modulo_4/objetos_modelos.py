from dataclasses import dataclass, field
from typing import Annotated

from pydantic import BaseModel, Field


# Dataclasses para entidad de dominio
@dataclass(order=True)
class OrderItem:
    product: str
    quantity: int
    price: float

    def total_price(self) -> float:
        return self.quantity * self.price


@dataclass(order=True)
class Order:
    id: int
    customer: str
    items: list[OrderItem] = field(default_factory=list)

    @property
    def total(self) -> float:
        return sum(item.total_price() for item in self.items)

    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)


# Modelos Pydantic para validación
class OrderItemIn(BaseModel):
    product: str
    quantity: Annotated[int, Field(gt=0)]
    price: Annotated[float, Field(gt=0)]


class OrderIn(BaseModel):
    customer: str
    items: list[OrderItemIn]


class OrderItemOut(OrderItemIn):
    total_price: float


class OrderOut(BaseModel):
    id: int
    customer: str
    items: list[OrderItemOut]
    total: float


# Funciones de conversión
def from_orderin_to_order(order_in: OrderIn, order_id: int) -> Order:
    items = [
        OrderItem(product=item.product, quantity=item.quantity, price=item.price)
        for item in order_in.items
    ]
    return Order(id=order_id, customer=order_in.customer, items=items)


def from_order_to_orderout(order: Order) -> OrderOut:
    items_out = [
        OrderItemOut(
            product=item.product,
            quantity=item.quantity,
            price=item.price,
            total_price=item.total_price(),
        )
        for item in order.items
    ]
    return OrderOut(
        id=order.id, customer=order.customer, items=items_out, total=order.total
    )


# Ejemplo de uso
def main() -> None:
    order_in = OrderIn(
        customer="Juan Pérez",
        items=[
            OrderItemIn(product="Laptop", quantity=1, price=1200.0),
            OrderItemIn(product="Mouse", quantity=2, price=25.5),
        ],
    )
    order = from_orderin_to_order(order_in, order_id=101)
    order_out = from_order_to_orderout(order)

    print("Orden creada:")
    print(order_out.model_dump_json(indent=4))


if __name__ == "__main__":
    main()
