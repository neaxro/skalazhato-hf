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
