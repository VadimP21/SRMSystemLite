class Product:
    def __init__(self, id, name, price, created_at, product_=None):
        self._product = product_
        self._id = id
        self.name = name
        self.price = price
        self._created_at = created_at

    @property
    def id(self):
        return self._id or self._product.id

    @property
    def created_at(self):
        return self._created_at or self._product.created_at

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "created_at": self.created_at,
        }
