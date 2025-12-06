from app.repository.postgres import PostgresRepository
from typing import Optional
from app.models.models import RecipeCreate

class RecipeService():
    def __init__(self):
        self.repository = PostgresRepository()
    
    def get_recipes(self, id: Optional[int]):
        if id:
            return self.repository.get_recipe_by_id(id)
        return self.repository.get_recipes()
    
    def create_recipe(self, recipe: RecipeCreate) -> int:
        return self.repository.create_recipe(recipe)

    def update_recipe(self, recipe_id: int, recipe: RecipeCreate) -> None:
        return self.repository.update_recipe(recipe_id, recipe)
    
    def delete_ingredient(self, recipe_id: int) -> None:
        return self.repository.delete_recipe(recipe_id)

recipeService = RecipeService()
