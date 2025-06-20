from http.client import HTTPException

from marshmallow import ValidationError
from tornado.web import RequestHandler, HTTPError

from lead.lead_repository.lead_repository import LeadRepository
from lead.lead_repository.unit_of_work import UnitOfWork
from lead.lead_service.exeptions import LeadNotNotFoundError
from lead.lead_service.lead_service import LeadService
from lead.web.schemas import CreateLeadSchema, GetLeadSchema


class Leads(RequestHandler):
    def get(self):
        parameters = {
            "limit": self.get_query_argument("limit"),
            "offset": self.get_query_argument("offset"),
            "sort_field": self.get_query_argument("sort_field"),
            "sort_order": self.get_query_argument("sort_order"),
        }
        try:
            with UnitOfWork() as unit_of_work:
                repo = LeadRepository(unit_of_work.session)
                lead_service = LeadService(repo)
                all_leads = lead_service.list_leads(**parameters)
            return {"leads": [lead.dict() for lead in all_leads]}

        except LeadNotNotFoundError:
            raise HTTPError(404, reason="Leads not founds")


class Lead(RequestHandler):
    def post(self):
        payload = {
            "name": self.get_argument("name"),
            "first_name": self.get_argument("first_name"),
            "phone": self.get_argument("phone"),
            "email": self.get_argument("email"),
            "adv_id": self.get_argument("adv_id"),
        }
        errors = CreateLeadSchema().validate(payload)
        if errors:
            raise ValidationError(errors)
        with UnitOfWork() as unit_of_work:
            repo = LeadRepository(unit_of_work.session)
            lead_service = LeadService(repo)
            lead = lead_service.place_lead(payload)
            unit_of_work.commit()
            return_payload = lead.dict()
            errors = GetLeadSchema().validate(return_payload)
            if errors:
                raise ValidationError(errors)
        return return_payload

    def get(self):
        lead_id = self.get_query_argument("lead_id")
        try:
            with UnitOfWork() as unit_of_work:
                repo = LeadRepository(unit_of_work.session)
                lead_service = LeadService(repo)
                result = lead_service.get_lead(lead_id)
                errors = GetLeadSchema().validate(result)
                if errors:
                    raise ValidationError(errors)
            return result.dict()
        except LeadNotNotFoundError:
            raise HTTPError(404, reason="Lead not found")

    def put(self):
        lead_id = self.get_query_argument("id")
        payload = {
            "name": self.get_argument("name"),
            "first_name": self.get_argument("first_name"),
            "phone": self.get_argument("phone"),
            "email": self.get_argument("email"),
            "adv_id": self.get_argument("adv_id"),
        }
        try:
            with UnitOfWork() as unit_of_work:
                repo = LeadRepository(unit_of_work.session)
                lead_service = LeadService(repo)
                result = lead_service.update_lead(lead_id, **payload)
                unit_of_work.commit()
            return result.dict()
        except LeadNotNotFoundError:
            raise HTTPError(404, reason="Lead not found")

    def delete(self):
        lead_id = self.get_query_argument("id")
        try:
            with UnitOfWork() as unit_of_work:
                repo = LeadRepository(unit_of_work.session)
                lead_service = LeadService(repo)
                lead_service.delete_lead(lead_id)
                unit_of_work.commit()
            return
        except LeadNotNotFoundError:
            raise HTTPError(404, reason="Lead not found")
