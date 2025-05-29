from flask.views import MethodView
from flask_smorest import Blueprint

blueprint = Blueprint('adv', __name__, description="Advertisement API")

@blueprint.route('/ads')
class Ads(MethodView):
    def get(self,):
        ...

    def post(self, ):
        ...


@blueprint.route('/ads/<adv_id>')
class Adv(MethodView):
    def get(self,):
        ...

    def put(self, ):
        ...

    def delete(self, ):
        pass