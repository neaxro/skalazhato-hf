import httpx
from typing import List, Union
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from app.models.models import RecipeWithIngredients, RecipeRead

class RecipeServiceRepository:
    def __init__(self, host: str, namespace: str = "default"):
        self.base_url = f"http://{host}.{namespace}.svc.cluster.local/recipe"

    retry_policy = retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(httpx.RequestError)
    )

    @retry_policy
    async def get_recipe_with_ingredients(self, recipe_id: int) -> RecipeWithIngredients:
        url = f"{self.base_url}/recipes/{recipe_id}/ingredients"
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

        recipe_data = data.get("recipe")
        if not recipe_data:
            raise Exception(f"No 'recipe' found in response for id {recipe_id}")

        return RecipeWithIngredients(**recipe_data)

    @retry_policy
    async def get_recipe(self, recipe_id: int) -> Union[RecipeRead, None]:
        url = f"{self.base_url}/recipe/recipes"
        params = {"id": recipe_id}

        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

        recipes = data.get("recipes", [])
        if recipes:
            return RecipeRead(**recipes[0])

        return None
