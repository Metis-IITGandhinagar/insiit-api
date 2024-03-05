from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKey
from fastapi.middleware.cors import CORSMiddleware
from app.auth.key import get_api_key
from config import app_description, tags_metadata
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel
from app.routers.mess import router as MessRouter
from app.routers.outlet import router as OutletRouter
from app.routers.bus import router as BusRouter

# from fastapi.templating import Jinja2Templates


def create_app():
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/v1/openapi.json",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = create_app()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="InsIIT API",
        version="1.0",
        description=app_description,
        routes=app.routes,
        tags=tags_metadata,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://avatars.githubusercontent.com/u/146699003?s=1000&v=4"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


class HelloWorldResponseModel(BaseModel):
    message: str


@app.get(
    "/",
    summary="Hello World!",
    tags=["hello world!"],
    response_model=HelloWorldResponseModel,
)
async def root():
    return {
        "message": "Hello from InsIIT! Visit /api/v1/docs to view the API documentation."
    }


@app.get("/api/v1/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="InsIIT API - Docs",
        swagger_favicon_url="https://avatars.githubusercontent.com/u/146699003?s=1000&v=4",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
    )


app.include_router(MessRouter)
app.include_router(OutletRouter)
app.include_router(BusRouter)
