import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.error_handler import http_error_handler
from app.core.config import AppSettings
from app.core.events import create_start_app_handler
from app.api.router import router


def get_application() -> FastAPI:
    settings = AppSettings()
    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler("startup", create_start_app_handler())

    application.add_exception_handler(HTTPException, http_error_handler)

    application.include_router(router)

    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
