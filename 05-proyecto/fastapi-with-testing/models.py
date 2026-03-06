from dataclasses import dataclass


@dataclass
class Product:
    id: int
    title: str
    price: float

    def __repr__(self):
        return f"Product(id={self.id}, title={self.title!r}, price={self.price})"
