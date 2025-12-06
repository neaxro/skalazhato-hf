import logging
from typing import List, Optional
from fastapi import APIRouter
from app.service.recipes import recipeService
from app.models.models import RecipeBase

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("", response_model=List[RecipeBase])
def get(id: Optional[int] = None):
    return recipeService.get_recipes(id)

@router.get("/hello")
def read_root():
    return {"Hello": "World"}
