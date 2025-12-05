import logging
from app.models.models import *

from psycopg2 import pool, extras
from contextlib import contextmanager
from app.utils.config import config
from typing import List

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
        query = "SELECT * FROM recipes"
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
