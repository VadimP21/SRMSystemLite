from fastapi import Query
from starlette import status

from product.product_repository.product_repository import ProductRepository
from product.product_repository.unit_fo_work import UnitOfWork
from product.product_service.product_service import ProductService
from product.web.main import app
from product.web.api.schemas import (
    CreateProductSchema,
    GetProductSchema,
    ProductResponse,
    SortOrder,
    SortField,
)


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
def get_products_list(
    limit: int | None = Query(10, ge=1),
    offset: int | None = Query(0, ge=0),
    sort_field: SortField | None = Query(None),
    sort_order: SortOrder | None = Query("asc", regex="^(asc|desc)$"),
):
    with UnitOfWork() as unit_of_work:
        repo = ProductRepository(unit_of_work.session)
        product_service = ProductService(repo)

        all_products = product_service.list_products(
            limit=limit, offset=offset, sort_field=sort_field, sort_order=sort_order
        )
        return {"products": [product.dict() for product in all_products]}
