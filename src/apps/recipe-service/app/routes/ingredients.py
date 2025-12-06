import logging
from typing import List, Optional
from fastapi import APIRouter
from app.service.ingredients import ingredientsService
from app.models.models import IngredientRead, IngredientCreate
from pydantic import BaseModel 

logger = logging.getLogger(__name__)

class IngredientReturnMessage(BaseModel):
    msg: str

class IngredientListMessage(IngredientReturnMessage):
    ingredients: List[IngredientRead]

class IngredientCreatedMessage(IngredientReturnMessage):
    ingredient_id: int

router = APIRouter()

@router.get(
    "",
    response_model=IngredientListMessage
)
def get(id: Optional[int] = None):
    result = ingredientsService.get_ingredients(id)
    return IngredientListMessage(
        msg="Ingredients successfuly fetched.",
        ingredients=result
    )

@router.post(
    "",
    response_model=IngredientCreatedMessage,
    status_code=201
)
def create(ingredient: IngredientCreate):
    result = ingredientsService.create_ingredient(ingredient)
    return IngredientCreatedMessage(
        msg="Ingredient successfuly created.",
        ingredient_id=result
    )

@router.patch(
    "",
    status_code=204
)
def update(id: int, ingredient: IngredientCreate):
    result = ingredientsService.update_ingredient(id, ingredient)

@router.delete(
    "",
    status_code=204
)
def delete(id: int):
    result = ingredientsService.delete_ingredient(id)
