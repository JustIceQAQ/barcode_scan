from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.page.api import page_router


def app_factory(lifespan_) -> FastAPI:
    from configs.settings import get_settings
    from configs import TITLE, VERSION
    from fastapi.openapi.utils import get_openapi
    from apps.routers import apis_router

    runtime_settings = get_settings()
    app_ = FastAPI(
        title=TITLE,
        debug=runtime_settings.IS_DEBUG,
        docs_url=runtime_settings.FASTAPI_DOCS_URL,
        redoc_url=runtime_settings.FASTAPI_REDOC_URL,
        openapi_url=runtime_settings.FASTAPI_OPENAPI_URL,
        swagger_ui_parameters={
            "syntaxHighlight.theme": "obsidian",
            "docExpansion": "none",
        },
        lifespan=lifespan_,
    )

    app_.include_router(apis_router)
    app_.include_router(page_router)

    def custom_openapi():  # pragma: no cover
        if app_.openapi_schema:
            return app_.openapi_schema
        openapi_schema = get_openapi(
            title=TITLE,
            version=VERSION,
            description=TITLE,
            routes=app_.routes,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": "https://roboadvisor.com.tw/img/alpha-logo.5ecb9126.png"
        }
        app_.openapi_schema = openapi_schema

        return app_.openapi_schema

    app_.openapi = custom_openapi
    return app_


async def startup() -> None:
    from configs.settings import get_settings
    import logging

    logger = logging.getLogger("uvicorn.error")
    runtime_settings = get_settings()
    logger.info(f"You are running [{runtime_settings.ENVIRONMENT}] environment.")


async def shutdown() -> None:
    pass


@asynccontextmanager
async def lifespan(app_: FastAPI):  # pragma: no cover
    await startup()
    yield
    await shutdown()


app = app_factory(lifespan)
