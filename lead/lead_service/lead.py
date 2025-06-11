class Lead:
    def __init__(
        self,
        id,
        name,
        first_name,
        phone,
        email,
        adv_id,
        is_active,
        is_archived,
        lead_=None,
    ):
        self._lead = lead_
        self._id = id
        self.name = name
        self.first_name = first_name
        self.phone = phone
        self.email = email
        self.adv_id = adv_id
        self.is_active = is_active
        self.is_archived = is_archived

    @property
    def id(self):
        return self._id or self._lead.id

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "first_name": self.first_name,
            "phone": self.phone,
            "email": self.email,
            "adv_id": self.adv_id,
            "is_active": self.is_active,
            "is_archived": self.is_archived,
        }
