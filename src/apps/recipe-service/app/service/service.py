from app.repository.postgres import PostgresRepository
from typing import Optional

class RecipeService():
    def __init__(self):
        self.repository = PostgresRepository()
    
    def get_recipes(self, id: Optional[int]):
        if id:
            return self.repository.get_recipe_by_id(id)
        return self.repository.get_recipes()

recipeService = RecipeService()
