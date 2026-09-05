import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import router
from app.config import settings
from app.database.mongodb import connect_to_mongo, close_mongo_connection
from app.middleware.error_handler import register_exception_handlers
from app.middleware.logging_middleware import RequestLoggingMiddleware


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start MongoDB connection
    connect_to_mongo()

    yield

    # Close MongoDB connection
    close_mongo_connection()


app = FastAPI(
    title="Creating Humanity API",
    description=(
        "Manages the creation of humanity and provides endpoints for "
        "user authentication, employee management, and other related functionalities."
    ),
    contact={
        "name": "Creating Humanity Engineering Team"
    },
    lifespan=lifespan,
    
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)

register_exception_handlers(app)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)





@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
    description="Basic liveness check of the API.",
)
async def root() -> dict:
    return {
        "success": True,
        "message": "Creating Humanity API is running successfully.",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )