import logging
from typing import List, Optional
from fastapi import APIRouter
from app.service.recipes import recipeService
from app.models.models import RecipeBase, RecipeRead, RecipeCreate
from pydantic import BaseModel 

logger = logging.getLogger(__name__)

class RecipeReturnMessage(BaseModel):
    msg: str

class RecipeListMessage(RecipeReturnMessage):
    recipes: List[RecipeRead]

class RecipeCreatedMessage(RecipeReturnMessage):
    recipe_id: int

router = APIRouter()

@router.get(
    "",
    response_model=RecipeListMessage
)
def get(id: Optional[int] = None):
    result = recipeService.get_recipes(id)
    return RecipeListMessage(
        msg="Recipes successfuly fetched.",
        recipes=result
    )

@router.post(
    "",
    response_model=RecipeCreatedMessage,
    status_code=201
)
def create(recipe: RecipeCreate):
    result = recipeService.create_recipe(recipe)
    return RecipeCreatedMessage(
        msg="Recipe successfuly created.",
        recipe_id=result
    )

@router.patch(
    "",
    status_code=204
)
def update(id: int, recipe: RecipeCreate):
    result = recipeService.update_recipe(id, recipe)

@router.delete(
    "",
    status_code=204
)
def delete(id: int):
    result = recipeService.delete_ingredient(id)
