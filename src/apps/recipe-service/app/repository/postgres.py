from psycopg2 import pool
from contextlib import contextmanager
from app.utils.config import config
import logging

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
        )

    @contextmanager
    def connection(self):
        conn = self.pool.getconn()
        try:
            yield conn
        finally:
            self.pool.putconn(conn)

    def test(self):
        query = "SELECT * FROM recipes"
        try:
            with self.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    results = cur.fetchall()
                    logger.debug(f"Fetched {len(results)} number of rows from recipes.")
                    return results
        except Exception as e:
            logger.error("DB query error: %s", e)
            raise
