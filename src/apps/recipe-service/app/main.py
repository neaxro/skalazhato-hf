import logging

from typing import Union
from fastapi import FastAPI
from app.routes import recipes

logger = logging.getLogger(__name__)

logger.info("Starting up backend...")
app = FastAPI(
    title="MealPlanner API",
)

logger.info("Attaching routers...")
app.include_router(recipes.router, prefix="/recipes")
