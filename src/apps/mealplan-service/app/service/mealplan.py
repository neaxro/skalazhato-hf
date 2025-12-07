import asyncio
from app.repository.postgres import PostgresRepository
from app.repository.recipe import RecipeServiceRepository
from typing import Optional, List, Dict
from app.models.models import (
    MealplanRead,
    MealplanReadWithRecipes,
    MealRecipeWithIngredients,
    RecipeIngredient
)
from app.service.redis import get_cache, set_cache
from app.utils.config import config

class MealplanService():
    def __init__(self):
        self.repository = PostgresRepository()
        self.recipeRepository = RecipeServiceRepository(
            host=config.RECIPE_SERVICE_HOST,
            namespace=config.RECIPE_SERVICE_NAMESPACE
        )
    
    async def get_mealplan(self, id: int) -> MealplanRead:
        cache_key = f"mealplan:{id}"
        
        data = await get_cache(cache_key, MealplanRead)
        if data:
            return data
        
        result = self.repository.get_mealplan(id)
        if result:
            await set_cache(cache_key, result)
        
        return result
    
    async def get_mealplan_with_recipes(self, id: int) -> MealplanReadWithRecipes:
        cache_key = f"mealplan_with_recipes:{id}"

        # 1️⃣ Check cache first
        cached = await get_cache(cache_key, MealplanReadWithRecipes)
        if cached:
            return cached

        # 2️⃣ Get mealplan metadata
        mealplan = self.repository.get_mealplan(id)

        # 3️⃣ Get mealplan_recipe mappings
        mealplan_recipes = self.repository.get_mealplan_recipes(id)

        # 4️⃣ Fetch recipes with ingredients in parallel
        async def fetch_recipe(mr):
            recipe_with_ingredients = await self.recipeRepository.get_recipe_with_ingredients(mr.recipe_id)
            return MealRecipeWithIngredients(
                id=mr.id,
                mealplan_id=mr.mealplan_id,
                recipe_id=mr.recipe_id,
                day_of_week=mr.day_of_week,
                ingredients=[RecipeIngredient(**ing.dict()) for ing in recipe_with_ingredients.ingredients]
            )

        meal_recipes: List[MealRecipeWithIngredients] = await asyncio.gather(
            *(fetch_recipe(mr) for mr in mealplan_recipes)
        )

        # 5️⃣ Construct final object
        result = MealplanReadWithRecipes(
            id=mealplan.id,
            user_id=mealplan.user_id,
            week_start=mealplan.week_start,
            created_at=mealplan.created_at,
            recipes=meal_recipes
        )

        # 6️⃣ Cache the result
        await set_cache(cache_key, result)

        return result

mealplanService = MealplanService()
