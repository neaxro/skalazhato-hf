import logging
from fastapi import APIRouter
from app.service.mealplan import mealplanService

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/{plan_id}",
)
async def get(plan_id: int):
    shoppingList = await mealplanService.createShoppingList(plan_id)
    return shoppingList
