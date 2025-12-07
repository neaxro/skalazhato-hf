import logging
from typing import List, Optional
from fastapi import APIRouter
from app.models.models import MealplanRead, MealplanReadWithRecipes
from pydantic import BaseModel 
from app.service.mealplan import mealplanService

from app.repository.recipe import RecipeServiceRepository

logger = logging.getLogger(__name__)

class MealplanReturnMessage(BaseModel):
    msg: str
    mealplan: MealplanRead

class MealplanWRecipesReturnMessage(BaseModel):
    msg: str
    mealplan: MealplanReadWithRecipes

router = APIRouter()

@router.get(
    "/{id}",
    response_model=MealplanReturnMessage
)
async def get(id: int):
    result = await mealplanService.get_mealplan(id)
    return MealplanReturnMessage(
        msg="Mealplan successfuly fetched.",
        mealplan=result
    )

@router.get(
    "/{id}/recipes",
    response_model=MealplanWRecipesReturnMessage
)
async def get_with_recipes(id: int):
    result = await mealplanService.get_mealplan_with_recipes(id)
    return MealplanReturnMessage(
        msg="Mealplan successfuly fetched.",
        mealplan=result
    )
