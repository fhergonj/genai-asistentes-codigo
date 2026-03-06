from models import Product


class Database:
    def __init__(self):
        self.products = {}
        self.next_id = 1
        self._load_sample_data()

    def _load_sample_data(self):
        self.create_product(Product(id=1, title="Laptop", price=999.99))
        self.create_product(Product(id=2, title="Mouse", price=29.99))
        self.next_id = 3

    def create_product(self, product: Product) -> Product:
        if product.id == 0 or product.id is None:
            product.id = self.next_id
            self.next_id += 1
        self.products[product.id] = product
        return product

    def get_product(self, product_id: int) -> Product | None:
        return self.products.get(product_id)

    def list_products(self) -> list[Product]:
        return list(self.products.values())

    def update_product(self, product_id: int, product: Product) -> Product | None:
        if product_id not in self.products:
            return None
        product.id = product_id
        self.products[product_id] = product
        return product

    def delete_product(self, product_id: int) -> bool:
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False

    def reset(self):
        self.products.clear()
        self.next_id = 1
        self._load_sample_data()


db = Database()
