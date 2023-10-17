from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKey
from fastapi.middleware.cors import CORSMiddleware
from app.auth.key import get_api_key


def create_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = create_app()


@app.get("/")
async def root(api_key: APIKey = Depends(get_api_key)):
    return {"message": "hello world"}


from app.routes import outletRoutes
