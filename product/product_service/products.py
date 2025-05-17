class Product:
    def __init__(self, id, name, price, created):
        self.id = id
        self.name = name
        self.price = price
        self.created = created

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "created": self.created,
        }
