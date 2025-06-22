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
            "limit": int(self.get_query_argument("limit", "10")),
            "offset": int(self.get_query_argument("offset", "0")),
            "sort_field": self.get_query_argument("sort_field", None),
            "sort_order": self.get_query_argument("sort_order", "asc"),
        }
        try:
            with UnitOfWork() as unit_of_work:
                repo = LeadRepository(unit_of_work.session)
                lead_service = LeadService(repo)
                all_leads = lead_service.list_leads(**parameters)
            self.write({"leads": [lead.dict() for lead in all_leads]})

        except LeadNotNotFoundError:
            raise HTTPError(404, reason="Leads not founds")


class Lead(RequestHandler):
    def post(self):
        try:
            payload = {
                "name": self.get_argument("name"),
                "first_name": self.get_argument("first_name"),
                "phone": self.get_argument("phone"),
                "email": self.get_argument("email"),
                "adv_id": int(self.get_argument("adv_id")),
            }
            CreateLeadSchema().validate(payload)
            with UnitOfWork() as unit_of_work:
                repo = LeadRepository(unit_of_work.session)
                lead_service = LeadService(repo)
                lead = lead_service.place_lead(payload)
                unit_of_work.commit()
            self.set_status(200)
            self.write(lead.dict())

        except ValidationError as e:
            self.set_status(400)
            self.write({"errors": e.messages})

        except HTTPException as e:
            self.set_status(e.code)
            self.write({"error": e.message})



    def get(self, lead_id=None):
        try:
            with UnitOfWork() as unit_of_work:
                repo = LeadRepository(unit_of_work.session)
                lead_service = LeadService(repo)
                result = lead_service.get_lead(lead_id)
            self.write(result.dict())
        except LeadNotNotFoundError:
            raise HTTPError(404, reason="Lead not found")


    def put(self, lead_id=None):
        try:
            payload = {
                "name": self.get_argument("name"),
                "first_name": self.get_argument("first_name"),
                "phone": self.get_argument("phone"),
                "email": self.get_argument("email"),
                "adv_id": int(self.get_argument("adv_id")),
            }

            with UnitOfWork() as unit_of_work:
                repo = LeadRepository(unit_of_work.session)
                lead_service = LeadService(repo)
                result = lead_service.update_lead(lead_id, **payload)
                unit_of_work.commit()
            self.write(result.dict())
        except LeadNotNotFoundError:
            raise HTTPError(404, reason="Lead not found")

    def delete(self,lead_id=None):
        try:
            with UnitOfWork() as unit_of_work:
                repo = LeadRepository(unit_of_work.session)
                lead_service = LeadService(repo)
                lead_service.delete_lead(lead_id)
                unit_of_work.commit()
            self.set_status(204)
        except LeadNotNotFoundError:
            raise HTTPError(404, reason="Lead not found")
