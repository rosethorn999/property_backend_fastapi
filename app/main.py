from fastapi import Depends, FastAPI
from functools import lru_cache
from app.api import api_router
from .config import Settings
from fastapi.middleware.cors import CORSMiddleware

# from .dependencies import get_query_token, get_token_header
# from .internal import admin

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "https://property-stg-next.nodm.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@lru_cache()
def get_settings():
    return Settings()


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
