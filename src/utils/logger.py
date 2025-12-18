from functools import wraps
import logging
from typing import Callable, TypeVar, Any

R = TypeVar("R")


def log(func: Callable[..., R]) -> Callable[..., R]: 
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> R: 
        try:
            response = await func(*args, **kwargs)
            return response 
        except Exception as exc:
            logging.error(f"Args: {args}, Kwargs: {kwargs}, Error: {str(exc)}")
            raise
    return wrapper


def configure_logging(level: int = logging.INFO) -> None: 
    logging.basicConfig(
        level=level, 
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s | %(levelname)-5s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        handlers=[
            logging.FileHandler("../app.log"),
            logging.StreamHandler()
        ]
    )