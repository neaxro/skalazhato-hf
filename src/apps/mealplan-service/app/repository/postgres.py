import logging
from app.models.models import *

from psycopg2 import pool, extras
from contextlib import contextmanager
from app.utils.config import config
from typing import List, Dict

logger = logging.getLogger(__name__)

class PostgresRepository:
    def __init__(self):
        self.pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dbname=config.POSTGRES_DATABASE,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASS,
            host=config.POSTGRES_HOST,
            cursor_factory=extras.RealDictCursor,
        )

    @contextmanager
    def connection(self):
        conn = self.pool.getconn()
        try:
            yield conn
        finally:
            self.pool.putconn(conn)

    def get_recipes(self) -> List[RecipeRead]:
        query = "SELECT * FROM recipes"
        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    results = cur.fetchall()
                    logger.debug(f"Fetched {len(results)} number of rows from recipes.")
        except Exception as e:
            logger.error("DB query error: %s", e)
            raise
        
        return [RecipeRead(**record) for record in results]

    def get_recipe_by_id(self, id: int) -> List[RecipeRead]:
        query = f"SELECT * FROM recipes WHERE id = {id}"
        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    result = cur.fetchone()
                    logger.debug(f"Fetched {len(result)} number of rows from recipes. (ID: {id})")
        except Exception as e:
            logger.error("DB query error: %s", e)
            raise

        return [RecipeRead(**result)]

    def create_recipe(self, recipe: RecipeCreate) -> int:
        query = """
            INSERT INTO recipes (name, description)
            VALUES (%s, %s)
            RETURNING id
        """
        params = (recipe.name, recipe.description)

        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    recipe_id = cur.fetchone()["id"]
                    conn.commit()
                    logger.debug(f'Inserted recipe "{recipe.name}" with id={recipe_id}')
                    return recipe_id
        except Exception as e:
            logger.error("DB insert error: %s", e)
            raise
        
    def update_recipe(self, recipe_id: int, recipe: RecipeCreate) -> None:
        query = """
            UPDATE recipes
            SET name = %s,
                description = %s
            WHERE id = %s
        """
        params = (recipe.name, recipe.description, recipe_id)

        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)

                    if cur.rowcount == 0:
                        raise ValueError(f"Recipe with id {recipe_id} not found")

                    conn.commit()
                    logger.debug(f'Updated recipe id={recipe_id}')
        except Exception as e:
            logger.error("DB update error: %s", e)
            raise

    def delete_recipe(self, recipe_id: int) -> None:
        query = """
            DELETE FROM recipes
            WHERE id = %s
        """
        params = (recipe_id,)

        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)

                    if cur.rowcount == 0:
                        raise ValueError(f"Recipe with id {recipe_id} not found")

                    conn.commit()
                    logger.debug(f'Deleted recipe id={recipe_id}')
        except Exception as e:
            logger.error("DB delete error: %s", e)
            raise

    def get_ingredients(self) -> List[IngredientRead]:
        query = "SELECT * FROM ingredients"
        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    results = cur.fetchall()
                    logger.debug(f"Fetched {len(results)} number of rows from ingredients.")
        except Exception as e:
            logger.error("DB query error: %s", e)
            raise
        
        return [IngredientRead(**record) for record in results]

    def get_ingredient_by_id(self, id: int) -> List[IngredientRead]:
        query = f"SELECT * FROM ingredients WHERE id = {id}"
        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    result = cur.fetchone()
                    logger.debug(f"Fetched {len(result)} number of rows from ingredients. (ID: {id})")
        except Exception as e:
            logger.error("DB query error: %s", e)
            raise

        return [IngredientRead(**result)]

    def create_ingredient(self, ingredient: IngredientCreate) -> int:
        query = """
            INSERT INTO ingredients (name, unit)
            VALUES (%s, %s)
            RETURNING id
        """
        params = (ingredient.name, ingredient.unit)

        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    ingredient_id = cur.fetchone()["id"]
                    conn.commit()
                    logger.debug(f'Inserted ingredient "{ingredient.name}" with id={ingredient_id}')
                    return ingredient_id
        except Exception as e:
            logger.error("DB insert error: %s", e)
            raise

    def update_ingredient(self, ingredient_id: int, ingredient: IngredientCreate) -> None:
        query = """
            UPDATE ingredients
            SET name = %s,
                unit = %s
            WHERE id = %s
        """
        params = (ingredient.name, ingredient.unit, ingredient_id)

        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)

                    if cur.rowcount == 0:
                        raise ValueError(f"Ingredient with id {ingredient_id} not found")

                    conn.commit()
                    logger.debug(f'Updated ingredient id={ingredient_id}')
        except Exception as e:
            logger.error("DB update error: %s", e)
            raise

    def delete_ingredient(self, ingredient_id: int) -> None:
        query = """
            DELETE FROM ingredients
            WHERE id = %s
        """

        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (ingredient_id,))

                    if cur.rowcount == 0:
                        raise ValueError(f"Ingredient with id {ingredient_id} not found")

                    conn.commit()
                    logger.debug(f'Deleted ingredient id={ingredient_id}')
        except Exception as e:
            logger.error("DB delete error: %s", e)
            raise

    def get_recipe_ingredients(self, recipe_id: int) -> List[RecipeIngredient]:
        query = """
            SELECT i.id, i.name, i.unit, ri.quantity
            FROM recipe_ingredients ri
            JOIN ingredients i ON ri.ingredient_id = i.id
            WHERE ri.recipe_id = %s
        """
        params = (recipe_id,)

        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    rows = cur.fetchall()

            recipe_ingredients = [
                RecipeIngredient(
                    id=row["id"],
                    name=row["name"],
                    unit=row.get("unit"),
                    quantity=Decimal(row["quantity"])
                )
                for row in rows
            ]

            return recipe_ingredients

        except Exception as e:
            logger.error("DB fetch error: %s", e)
            raise

    def get_recipe_contains_ingredient(self, recipe_id: int, ingredient_id: int):
        query = """
            SELECT * FROM recipe_ingredients
            WHERE recipe_id = %s
                AND ingredient_id = %s
        """
        params = (recipe_id, ingredient_id)
        
        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    result = cur.fetchone()
        except Exception as e:
            logger.error("DB query error: %s", e)
            raise
        
        return RecipeIngredientRead(**result) if result else None

    def create_recipe_ingredients(self, recipe_id: int, ingredient_id: int, ingredient_quantity: int) -> int:
        query = """
            INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        params = (recipe_id, ingredient_id, ingredient_quantity)

        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    pair_id = cur.fetchone()["id"]
                    conn.commit()
                    logger.debug(f'Added ingredient to recipe, pair id={pair_id}')
                    return pair_id
        except Exception as e:
            logger.error("DB insert error: %s", e)
            raise

    def update_recipe_ingredient(
        self,
        recipe_id: int,
        ingredient_id: int,
        new_quantity: int
    ) -> int:
        query = """
            UPDATE recipe_ingredients
            SET quantity = %s
            WHERE recipe_id = %s AND ingredient_id = %s
            RETURNING id
        """
        params = (new_quantity, recipe_id, ingredient_id)

        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    updated_row = cur.fetchone()
                    if not updated_row:
                        raise ValueError(
                            f"No ingredient with id={ingredient_id} found in recipe id={recipe_id}"
                        )
                    conn.commit()
                    logger.debug(
                        f"Updated ingredient {ingredient_id} in recipe {recipe_id}, new quantity={new_quantity}"
                    )
                    return updated_row["id"]
        except Exception as e:
            logger.error("DB update error: %s", e)
            raise

    def delete_recipe_ingredient(self, recipe_id: int, ingredient_id: int) -> None:
        query = """
            DELETE FROM recipe_ingredients
            WHERE recipe_id = %s AND ingredient_id = %s
            RETURNING id
        """
        params = (recipe_id, ingredient_id)

        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    deleted_row = cur.fetchone()
                    if not deleted_row:
                        raise ValueError(
                            f"No ingredient with id={ingredient_id} found in recipe id={recipe_id}"
                        )
                    conn.commit()
                    logger.debug(
                        f"Deleted ingredient {ingredient_id} from recipe {recipe_id}"
                    )
        except Exception as e:
            logger.error("DB delete error: %s", e)
            raise
