from app.repository.postgres import PostgresRepository
from typing import Optional, List, Dict
from app.models.models import IngredientCreate, IngredientRead

class IngredientsService():
    def __init__(self):
        self.repository = PostgresRepository()
    
    def get_ingredients(self, id: Optional[int]) -> List[IngredientRead]:
        if id:
            return self.repository.get_ingredient_by_id(id)
        return self.repository.get_ingredients()
    
    def create_ingredient(self, ingredient: IngredientCreate) -> int:
        return self.repository.create_ingredient(ingredient)
    
    def update_ingredient(self, ingredient_id: int, ingredient: IngredientCreate) -> None:
        return self.repository.update_ingredient(ingredient_id, ingredient)
    
    def delete_ingredient(self, ingredient_id: int) -> None:
        return self.repository.delete_ingredient(ingredient_id)

ingredientsService = IngredientsService()
