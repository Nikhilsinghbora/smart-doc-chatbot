from fastapi import FastAPI
from contextlib import asynccontextmanager
from .api import router

def create_app() -> FastAPI:

    @asynccontextmanager
    async def lifespan(app:FastAPI):
        # This is where you can put your initialization code
        print("Database initialized")

        yield
        # This is where you can put your cleanup code
        print("Database closed")

    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    return app