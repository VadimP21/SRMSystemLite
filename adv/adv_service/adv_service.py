from adv.adv_service.adv import Adv
from adv.adv_service.exeptions import AdvNotFind


class AdvService:
    def __init__(self, adv_repository):
        self.adv_repository = adv_repository

    def place_adv(self, item):
        return self.adv_repository.add(item)

    def get_adv(self, adv_id) -> Adv:
        adv = self.adv_repository.get(adv_id)
        if adv is not None:
            return adv
        raise AdvNotFind(f"Advertisement with id {adv_id} is not found")

    def update_adv(self, adv_id, item):
        adv = self.adv_repository.get(adv_id)
        if adv is None:
            raise AdvNotFind(f"Advertisement with id {adv_id} is not found")
        return self.adv_repository.update(adv_id, item)

    def delete_adv(self, adv_id):
        adv = self.adv_repository.get(adv_id)
        if adv is None:
            raise AdvNotFind(f"Advertisement with id {adv_id} is not found")
        self.adv_repository.delete(adv_id)

    def list_ads(self, **filters):
        limit = filters.pop("limit")
        offset = filters.pop("offset", None)
        sort_field = filters.pop("sort_field", None)
        sort_order = filters.pop("sort_order", None)

        return self.adv_repository.get_list(
            limit=limit,
            offset=offset,
            sort_field=sort_field,
            sort_order=sort_order,
            **filters,
        )
