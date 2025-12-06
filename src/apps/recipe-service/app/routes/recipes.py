import logging
from typing import List, Optional
from fastapi import APIRouter
from app.service.recipes import recipeService
from app.models.models import RecipeBase, RecipeRead, RecipeCreate, RecipeWithIngredients
from pydantic import BaseModel 

logger = logging.getLogger(__name__)

class RecipeReturnMessage(BaseModel):
    msg: str

class RecipeListMessage(RecipeReturnMessage):
    recipes: List[RecipeRead]

class RecipeCreatedMessage(RecipeReturnMessage):
    recipe_id: int

class RecipeWithIngredientsMessage(RecipeReturnMessage):
    recipe: RecipeWithIngredients

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

@router.get(
    "/{recipe_id}/ingredients",
    response_model=RecipeWithIngredientsMessage
)
def get_with_ingredients(recipe_id: int):
    result = recipeService.get_recipe_with_ingredients(recipe_id)
    return RecipeWithIngredientsMessage(
        msg="Recipe successfuly fetched with ingredients.",
        recipe=result
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
    result = recipeService.delete_recipe(id)

@router.post(
    "/{recipe_id}/ingredient/{ingredient_id}",
    response_model=RecipeReturnMessage,
    status_code=201
)
def recipe_add_ingredient(recipe_id: int, ingredient_id: int, ingredient_quantity: int):
    result = recipeService.add_ingredient(recipe_id, ingredient_id, ingredient_quantity)
    return RecipeReturnMessage(
        msg="Ingredient added to recipe!"
    )

@router.patch(
    "/{recipe_id}/ingredient/{ingredient_id}",
    status_code=204
)
def recipe_update_ingredient(recipe_id: int, ingredient_id: int, ingredient_quantity: int):
    result = recipeService.update_recipe_ingredient(recipe_id, ingredient_id, ingredient_quantity)

@router.delete(
    "/{recipe_id}/ingredient/{ingredient_id}",
    status_code=204
)
def recipe_delete_ingredient(recipe_id: int, ingredient_id: int):
    result = recipeService.delete_recipe_ingredient(recipe_id, ingredient_id)
