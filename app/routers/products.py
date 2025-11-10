from fastapi import APIRouter
from .. import crud,schemas

router = APIRouter(
    prefix = "/products",
    tags = ["products"],
)

@router.get("/{id}",response_model=schemas.ProductSchema)
def get_product(id:int):
    return crud.get_products_by_id(id)

@router.post("/")
def add_product(product : schemas.ProductSchema):
    crud.add_product(product)
    