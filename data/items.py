from dataclasses import dataclass


@dataclass
class Item:
    id: int
    title: str
    price: int


access = Item(
    id=1,
    title="Доступ в приватный чат",
    price=1
)

items = [access]
