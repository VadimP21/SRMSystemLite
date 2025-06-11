from typing import Dict, Any, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from lead.lead_repository.models import LeadModel
from lead.lead_service.lead import Lead


class LeadRepository:
    def __init__(self, session: Session):
        self.session = session

    def _get_lead(self, id_: int) -> LeadModel | None:
        try:
            return self.session.query(LeadModel).filter(LeadModel.id == id_).first()

        except SQLAlchemyError as e:
            print(f"Error getting lead: {e}")
            return None

    def get_list(
        self,
        limit: int | None,
        offset: int | None,
        sort_field: str | None,
        sort_order: str = "asc",
        **filters,
    ) -> List[Lead] | None:
        try:
            query = self.session.query(LeadModel).filter_by(**filters)
            if sort_field is not None:
                column = getattr(LeadModel, sort_field, None)
                if column is not None:
                    if sort_order.lower() == "desc":
                        query = query.order_by(column.desc())
                    else:
                        query = query.order_by(column.asc())
                else:
                    print(f"Warning: Sort field '{sort_field}' not found in LeadModel.")

            if limit is not None:
                query = query.limit(limit)
            if offset > 0:
                query = query.offset(offset)
            leads = query.all()

            return [Lead(**lead.dict()) for lead in leads]

        except SQLAlchemyError as e:
            print(f"Error getting lead: {e}")
            return None

    def add(self, lead) -> Lead | None:
        try:
            record = LeadModel(**lead)
            self.session.add(record)
            return Lead(**record.dict(), lead_=record)
        except SQLAlchemyError as e:
            print(f"Error adding lead: {e}")
            return None

    def get(self, id_: int) -> Lead | None:
        try:
            lead = self._get_lead(id_)
            if lead:
                return Lead(**lead.dict())
        except SQLAlchemyError as e:
            print(f"Error getting lead: {e}")
            return None

    def update(self, id_, new_lead: Dict[str, Any]) -> Lead | None:
        try:
            record = self._get_lead(id_)
            if record is None:
                return None
            for key, value in new_lead.items():
                setattr(record, key, value)
            return Lead(**record.dict())
        except SQLAlchemyError as e:
            print(f"Error getting lead: {e}")
            return None

    def delete(self, id_):
        try:
            record = self._get_lead(id_)
            if record:
                self.session.delete(record)
        except SQLAlchemyError as e:
            print(f"Error getting lead: {e}")
            return None
