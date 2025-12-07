import logging
from typing import List, Optional
from fastapi import APIRouter
from app.models.models import RecipeBase, RecipeRead, RecipeCreate, RecipeWithIngredients
from pydantic import BaseModel 

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "",
)
def get(id: Optional[int] = None):
    return {'Hello': 'shoppinglist!'}
