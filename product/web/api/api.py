from starlette import status

from product.product_repository.product_repository import ProductRepository
from product.product_repository.unit_fo_work import UnitOfWork
from product.product_service.product_service import ProductService
from product.web.main import app
from product.web.api.schemas import CreateProductSchema, GetProductSchema

@app.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    response_model=GetProductSchema,
)
def create_product(payload: CreateProductSchema):
    with UnitOfWork() as unit_of_work:
        repo = ProductRepository(unit_of_work.session)
        product_service = ProductService(repo)
        product = payload.model_dump()
        product = product_service.place_product(product)
        unit_of_work.commit()
        return_payload = product.dict()

    return return_payload