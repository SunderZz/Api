from fastapi import APIRouter, FastAPI, Depends
from typing import Annotated
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from users.router import router as users_router
from starlette.types import Scope, Send, Receive, Message, ASGIApp

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI(
    title="Pysae API",
    openapi_tags=[
        {
            "name": "v3",
            "description": "Latest version",
        },
        {"name": "v2", "description": "Progressively removed in favor of v3"},
    ],
)

fallback_url_router = APIRouter(tags=["fallback_url"])
CAPACITOR_ORIGIN = "http://localhost"


class ContentTypeMiddleware:
    def __init__(self, app: ASGIApp, default: str):
        self.app = app
        self.default = default


def get_db():
    db = SessionLocal
    try: 
        yield db
    finally:
        db.close_all()

db_dependency= Annotated[Session, Depends(get_db)]



app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(users_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CAPACITOR_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

