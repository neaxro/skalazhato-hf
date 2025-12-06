from app.repository.postgres import PostgresRepository
from typing import Optional
from app.models.models import RecipeCreate, RecipeWithIngredients

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
    
    def delete_recipe(self, recipe_id: int) -> None:
        return self.repository.delete_recipe(recipe_id)

    def get_recipe_with_ingredients(self, recipe_id: int) -> RecipeWithIngredients:
        recipe = self.repository.get_recipe_by_id(recipe_id)
        if not recipe:
            raise Exception(f"Recipe with id {recipe_id} is not found!")
        
        ingredients = self.repository.get_recipe_ingredients(recipe_id)
        
        return RecipeWithIngredients(
            id=recipe[0].id,
            name=recipe[0].name,
            description=recipe[0].description,
            created_at=recipe[0].created_at,
            updated_at=recipe[0].updated_at,
            ingredients=ingredients
        )

    def add_ingredient(self, recipe_id: int, ingredient_id: int, ingredient_quantity: int) -> int:
        try:
            recipe = self.repository.get_recipe_by_id(recipe_id)
        except Exception as e:
            raise Exception(f"Recipe with id {recipe_id} is not found!")

        try:
            ingredient = self.repository.get_ingredient_by_id(ingredient_id)
        except Exception as e:
            raise Exception(f"Ingredient with id {ingredient_id} is not found!")
        
        existing_ingredient = self.repository.get_recipe_contains_ingredient(recipe_id, ingredient_id)
        if existing_ingredient:
            raise Exception("Recipe already contains ingredient!")

        return self.repository.create_recipe_ingredients(recipe_id, ingredient_id, ingredient_quantity)

    def update_recipe_ingredient(
        self,
        recipe_id: int,
        ingredient_id: int,
        new_quantity: int
    ) -> int:
        return self.repository.update_recipe_ingredient(recipe_id, ingredient_id, new_quantity)
    
    def delete_recipe_ingredient(self, recipe_id: int, ingredient_id: int) -> None:
        return self.repository.delete_recipe_ingredient(recipe_id, ingredient_id)

recipeService = RecipeService()
