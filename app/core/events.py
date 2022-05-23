from typing import Callable
from pathlib import Path


def create_start_app_handler() -> Callable:
    async def start_app() -> None:
        Path("../var/www/html/uploads/").mkdir(parents=True, exist_ok=True)

    return start_app
