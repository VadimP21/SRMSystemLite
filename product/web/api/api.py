from fastapi import Query, HTTPException
from starlette import status

from product.product_repository.product_repository import ProductRepository
from product.product_repository.unit_of_work import UnitOfWork
from product.product_service.exeptions import ProductNotFoundError
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
    response_model=ProductResponse,
)
def get_products_list(
    limit: int | None = Query(10, ge=10, le=50),
    offset: int | None = Query(0, ge=0, le=50),
    sort_field: SortField | None = Query(None),
    sort_order: SortOrder | None = Query("asc", pattern="^(asc|desc)$"),
):
    with UnitOfWork() as unit_of_work:
        repo = ProductRepository(unit_of_work.session)
        product_service = ProductService(repo)

        all_products = product_service.list_products(
            limit=limit, offset=offset, sort_field=sort_field, sort_order=sort_order
        )
    return {"products": [product.dict() for product in all_products]}


@app.get(
    "/products/{product_name}",
    response_model=GetProductSchema,
)
def get_product(product_name: str):
    try:
        with UnitOfWork() as unit_of_work:
            repo = ProductRepository(unit_of_work.session)
            product_service = ProductService(repo)

            result = product_service.get_product(product_name=product_name)

        return result.dict()
    except ProductNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Product '{product_name}' not found"
        )


@app.put(
    "/products/{product_name}",
    response_model=GetProductSchema,
)
def update_product(product_name: str, product_details: CreateProductSchema):
    try:
        with UnitOfWork() as unit_of_work:
            repo = ProductRepository(unit_of_work.session)
            product_service = ProductService(repo)
            new_product = product_details.model_dump()

            result = product_service.update_product(
                product_name=product_name, new_product=new_product
            )
            unit_of_work.commit()
        return result.dict()
    except ProductNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Product '{product_name}' not found"
        )


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(product_id: int):
    try:
        with UnitOfWork() as unit_of_work:
            repo = ProductRepository(unit_of_work.session)
            product_service = ProductService(repo)
            product_service.delete_product(product_id=product_id)

            unit_of_work.commit()
        return
    except ProductNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Product with ID '{product_id}' not found"
        )
