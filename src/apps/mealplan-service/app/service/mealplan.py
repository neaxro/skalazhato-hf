import asyncio
from app.repository.postgres import PostgresRepository
from app.repository.recipe import RecipeServiceRepository
from typing import Optional, List, Dict
from app.models.models import (
    MealplanRead,
    MealplanReadWithRecipes,
    RecipeWithIngredients,
    RecipeIngredient,
    DTOMealplanCreate,
    MealplanCreate,
    MealplanRecipeCreate,
    MealplanRecipeRead
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

        cached = await get_cache(cache_key, MealplanReadWithRecipes)
        if cached:
            return cached

        mealplan = self.repository.get_mealplan(id)
        mealplan_recipes = self.repository.get_mealplan_recipes(id)

        async def fetch_recipe(mr):
            recipe_with_ingredients = await self.recipeRepository.get_recipe_with_ingredients(mr.recipe_id)
            return RecipeWithIngredients(
                id=recipe_with_ingredients.id,
                name=recipe_with_ingredients.name,
                description=recipe_with_ingredients.description,
                created_at=recipe_with_ingredients.created_at,
                updated_at=recipe_with_ingredients.updated_at,
                ingredients=[RecipeIngredient(**ing.dict()) for ing in recipe_with_ingredients.ingredients]
            )

        recipes: list[RecipeWithIngredients] = await asyncio.gather(
            *(fetch_recipe(mr) for mr in mealplan_recipes)
        )

        result = MealplanReadWithRecipes(
            id=mealplan.id,
            user_id=mealplan.user_id,
            week_start=mealplan.week_start,
            created_at=mealplan.created_at,
            recipes=recipes
        )

        await set_cache(cache_key, result)

        return result

    async def createMealplan(self, mealplan: DTOMealplanCreate) -> int:
        mealplanData = MealplanCreate(
            user_id=mealplan.user_id,
            week_start=mealplan.week_start
        )
        mealplan_id = self.repository.create_mealplan(mealplanData)
        
        for recipe in mealplan.recipes:
            data = MealplanRecipeCreate(
                mealplan_id=mealplan_id,
                recipe_id=recipe.recipe_id,
                day_of_week=recipe.day_of_week
            )
            self.repository.create_mealplan_recipe(data)
        
        return mealplan_id

    async def shoppingListItemsForRecipe(self, recipe: MealplanRecipeRead) -> List[RecipeIngredient]:
        recipe_data = await self.recipeRepository.get_recipe_with_ingredients(recipe.recipe_id)
        ingredients: List[RecipeIngredient] = recipe_data.ingredients

        aggregated = {}
        for ing in ingredients:
            if ing.id in aggregated:
                aggregated[ing.id].quantity += ing.quantity
            else:
                aggregated[ing.id] = RecipeIngredient(
                    id=ing.id,
                    name=ing.name,
                    unit=ing.unit,
                    quantity=ing.quantity
                )
        return list(aggregated.values())

    async def createShoppingList(self, mealplan_id: int) -> List[RecipeIngredient]:
        mealplan_recipes: List[MealplanRecipeRead] = self.repository.get_mealplan_recipes(mealplan_id)

        aggregated_items: dict[int, RecipeIngredient] = {}
        for recipe in mealplan_recipes:
            items = await self.shoppingListItemsForRecipe(recipe)
            for item in items:
                if item.id in aggregated_items:
                    aggregated_items[item.id].quantity += item.quantity
                else:
                    aggregated_items[item.id] = item

        return list(aggregated_items.values())

mealplanService = MealplanService()
