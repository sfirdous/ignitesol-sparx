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
    return crud.add_product(product)

@router.put("/")
def update_product(id:int,product : schemas.ProductSchema):
    return crud.update_product(id,product)

@router.delete("/")
def delete_product(id:int):
    return crud.delete_product(id)
    