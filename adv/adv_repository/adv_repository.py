from typing import Dict, Any, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from adv.adv_repository.models import AdvModel
from adv.adv_service.adv import Adv


class AdvRepository:
    """
    Репозиторий для Adv
    Основные функции:
                    принимают Dict[str, Any], int,
                    возвращают Adv | List[Adv] |None
    Внутренние функции:
                    возвращают модели БД
    """

    def __init__(self, session: Session):
        self.session = session

    def _get(self, id_: int) -> AdvModel | None:
        try:
            return self.session.query(AdvModel).filter(AdvModel.id == id_).first()
        except SQLAlchemyError as e:
            print(f"Error getting adv: {e}")
            return None

    def get_list(
        self,
        limit: int | None,
        offset: int | None,
        sort_field: str | None,
        sort_order: str = "asc",
        **filters,
    ):
        try:
            query = self.session.query(AdvModel).filter_by(**filters)
            if sort_field is not None:
                if sort_field == "desc":
                    query = query.order_by(getattr(AdvModel, sort_order).desc())
                else:
                    query = query.order_by(getattr(AdvModel, sort_order))
            if limit is not None:
                query = query.limit(limit)
            if offset is not None:
                query = query.offset(offset)
            ads = query.all()
            return [Adv(**adv.dict()) for adv in ads]
        except SQLAlchemyError as e:
            print(f"Error getting ads: {e}")
            return None

    def add(self, adv: Dict[str, Any]) -> Adv | None:
        try:
            record = AdvModel(**adv)
            self.session.add(record)
            return Adv(**record.dict(), adv_=record)

        except SQLAlchemyError as e:
            print(f"Error adding adv: {e}")
            return None

    def get(self, id_: int) -> Adv | None:
        try:
            adv = self._get(id_)
            if adv:
                return Adv(**adv.dict())
            return None
        except SQLAlchemyError as e:
            print(f"Error adding adv: {e}")
            return None

    def update(self, id_: int, new_adv: dict[str, Any]) -> Adv | None:
        try:
            record = self._get(id_)
            if record is None:
                return None
            for key, val in new_adv.items():
                setattr(record, key, val)
            return Adv(**record.dict())
        except SQLAlchemyError as e:
            print(f"Error adding adv: {e}")
            return None

    def delete(self, id_: int) -> None:
        try:
            record = self._get(id_)
            if record:
                self.session.delete(record)
        except SQLAlchemyError as e:
            print(f"Error deleting adv: {e}")
