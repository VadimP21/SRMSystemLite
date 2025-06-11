from lead.lead_service.exeptions import LeadNotNotFoundError


class LeadService:
    def __init__(self, lead_repository):
        self.lead_repository = lead_repository

    def place_lead(self, item):
        return self.lead_repository.add(item)

    def get_lead(self, lead_id):
        lead = self.lead_repository.get(lead_id)
        if lead is not None:
            return lead
        raise LeadNotNotFoundError(f"Lead with id {lead_id} is not found")

    def update_lead(self, lead_id, item):
        lead = self.lead_repository.get(lead_id)
        if lead is None:
            raise LeadNotNotFoundError(f"Lead with id {lead_id} is not found")
        return self.lead_repository.update(lead_id, item)

    def archive_lead(self, lead_id):
        lead = self.lead_repository.get(lead_id)
        if lead is None:
            raise LeadNotNotFoundError(f"Lead with id {lead_id} is not found")
        self.lead_repository.archive(lead_id)

    def list_leads(self, **filters):
        limit = filters.pop("limit")
        offset = filters.pop("offset", None)
        sort_field = filters.pop("sort_field", None)
        sort_order = filters.pop("sort_order", None)

        return self.lead_repository.get_list(
            limit=limit,
            offset=offset,
            sort_field=sort_field,
            sort_order=sort_order,
            **filters,
        )
