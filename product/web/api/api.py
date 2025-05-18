from starlette import status

from product.product_repository.product_repository import ProductRepository
from product.product_repository.unit_fo_work import UnitOfWork
from product.product_service.product_service import ProductService
from product.web.main import app
from product.web.api.schemas import CreateProductSchema, GetProductSchema, ProductResponse


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


@app.get(
    "/products",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
)
def get_products_list(limit: int = None):
    with UnitOfWork() as unit_of_work:
        repo = ProductRepository(unit_of_work.session)
        product_service = ProductService(repo)
        all_products = product_service.list_products(limit=limit)
        return {"products": [product.dict() for product in all_products]}
