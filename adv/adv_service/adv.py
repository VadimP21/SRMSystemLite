class Adv:
    def __init__(self, id, name, chanel, cost, created_at, product_id, adv_=None):
        self._adv = adv_
        self._id = id
        self.name = name
        self.chanel = chanel
        self.cost = cost
        self._created_at = created_at
        self.product_id = product_id

    @property
    def id(self):
        return self._id or self._adv.id

    @property
    def created_at(self):
        return self._created_at or self._adv.created_at

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "chanel": self.chanel,
            "cost": self.cost,
            "created_at": self.created_at,
            "product_id": self.product_id,
        }
