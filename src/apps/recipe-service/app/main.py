import logging

from typing import Union
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.routes import recipes, ingredients
from pydantic import BaseModel
from app.utils.config import config

class ErrorResponse(BaseModel):
    msg: str = "Error occured."
    error: str

logger = logging.getLogger(__name__)

logger.info("Starting up backend...")
app = FastAPI(
    title="MealPlanner API",
    root_path=config.ROOTPATH
)

@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")

    if isinstance(exc, HTTPException):
        error_message = str(exc.detail)
        status_code = exc.status_code
    else:
        error_message = str(exc)
        status_code = 500

    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(
            error=error_message
        ).dict()
    )


logger.info("Attaching routers...")
app.include_router(recipes.router, prefix="/recipes")
app.include_router(ingredients.router, prefix="/ingredients")
