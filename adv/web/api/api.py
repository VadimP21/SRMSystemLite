from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_smorest.error_handler import ErrorSchema

from adv.adv_repository.adv_repository import AdvRepository
from adv.adv_repository.unit_fo_work import UnitOfWork
from adv.adv_service.adv_service import AdvService
from adv.adv_service.exeptions import AdvNotNotFoundError
from adv.web.api.schemas import (
    GetAdsSchema,
    CreateAdvSchema,
    GetAdvSchema,
    GetAdsParameters,
)

blueprint = Blueprint("adv", __name__, description="Advertisement API")


@blueprint.route("/ads")
class Ads(MethodView):
    @blueprint.arguments(GetAdsParameters, location="query")
    @blueprint.response(status_code=200, schema=GetAdsSchema)
    def get(self, parameters):
        with UnitOfWork() as unit_of_work:
            repo = AdvRepository(unit_of_work.session)
            adv_service = AdvService(repo)
            all_ads = adv_service.list_ads(**parameters)
        return {"ads": [adv.dict() for adv in all_ads]}

    @blueprint.arguments(CreateAdvSchema)
    @blueprint.response(status_code=201, schema=GetAdvSchema)
    def post(self, payload):
        with UnitOfWork() as unit_of_work:
            repo = AdvRepository(unit_of_work.session)
            adv_service = AdvService(repo)
            adv = adv_service.place_adv(payload)
            unit_of_work.commit()
            return_payload = adv.dict()
        return return_payload


@blueprint.route("/ads/<adv_id>")
class Adv(MethodView):
    @blueprint.response(status_code=200, schema=GetAdvSchema)
    @blueprint.alt_response(status_code=404, schema=ErrorSchema)
    def get(self, adv_id):
        try:
            with UnitOfWork() as unit_of_work:
                repo = AdvRepository(unit_of_work.session)
                adv_service = AdvService(repo)
                result = adv_service.get_adv(adv_id)
            return result.dict()

        except AdvNotNotFoundError:
            abort(404, description=f"Advertisement with ID='{adv_id}' not found")

    @blueprint.arguments(CreateAdvSchema)
    @blueprint.response(status_code=200, schema=GetAdvSchema)
    @blueprint.alt_response(status_code=404, schema=ErrorSchema)
    def put(self, adv_id, payload):
        try:
            with UnitOfWork() as unit_of_work:
                repo = AdvRepository(unit_of_work.session)
                adv_service = AdvService(repo)
                result = adv_service.update_adv(adv_id, payload)
                unit_of_work.commit()
            return result.dict()

        except AdvNotNotFoundError:
            abort(404, message=f"Advertisement with ID='{adv_id}' not found")

    @blueprint.response(status_code=204)
    @blueprint.alt_response(status_code=404, schema=ErrorSchema)
    def delete(self, adv_id):
        try:
            with UnitOfWork() as unit_of_work:
                repo = AdvRepository(unit_of_work.session)
                adv_service = AdvService(repo)
                adv_service.delete_adv(adv_id)
                unit_of_work.commit()
            return

        except AdvNotNotFoundError:
            abort(404, message=f"Advertisement with ID='{adv_id}' not found")
