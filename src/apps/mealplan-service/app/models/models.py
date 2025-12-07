from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, conint


class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = None

class RecipeCreate(RecipeBase):
    pass

class RecipeRead(RecipeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class IngredientBase(BaseModel):
    name: str
    unit: Optional[str] = None

class IngredientCreate(IngredientBase):
    pass

class IngredientRead(IngredientBase):
    id: int

    class Config:
        from_attributes = True

class RecipeIngredientBase(BaseModel):
    recipe_id: int
    ingredient_id: int
    quantity: Decimal

class RecipeIngredientCreate(RecipeIngredientBase):
    pass

class RecipeIngredientRead(RecipeIngredientBase):
    id: int

    class Config:
        from_attributes = True

class MealplanBase(BaseModel):
    user_id: Optional[int] = None
    week_start: date

class MealplanRead(MealplanBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MealplanCreate(MealplanBase):
    pass

class MealplanRecipeBase(BaseModel):
    mealplan_id: int
    recipe_id: int
    day_of_week: conint(ge=0, le=6)

class MealplanRecipeCreate(MealplanRecipeBase):
    pass

class MealplanRecipeRead(MealplanRecipeBase):
    id: int

    class Config:
        from_attributes = True

class RecipeIngredient(IngredientRead):
    quantity: Decimal

class RecipeWithIngredients(RecipeRead):
    ingredients: List[RecipeIngredient]

class MealplanReadWithRecipes(MealplanRead):
    recipes: List[RecipeWithIngredients]

# DTOs

class MealplanCreateRecipeItem(BaseModel):
    recipe_id: int
    day_of_week: conint(ge=0, le=6)

class DTOMealplanCreate(MealplanBase):
    recipes: List[MealplanCreateRecipeItem]
