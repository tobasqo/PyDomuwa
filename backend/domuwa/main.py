import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import Response

from domuwa.auth.routes import router as auth_router
from domuwa.config import settings
from domuwa.database import create_db_and_tables
from domuwa.routers.answers_router import get_answers_router
from domuwa.routers.game_category_router import get_game_category_router
from domuwa.routers.game_types_router import get_game_types_router
from domuwa.routers.players_router import get_players_router
from domuwa.routers.qna_categories_router import get_qna_categories_router
from domuwa.routers.questions_router import get_questions_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.getLogger("asyncio").setLevel(logging.INFO)
    create_db_and_tables()
    yield


app = FastAPI(debug=True, lifespan=lifespan)

API_PREFIX = "/api"
app.include_router(auth_router)
app.include_router(get_players_router(), prefix=API_PREFIX)
app.include_router(get_game_types_router(), prefix=API_PREFIX)
app.include_router(get_qna_categories_router(), prefix=API_PREFIX)
app.include_router(get_answers_router(), prefix=API_PREFIX)
app.include_router(get_questions_router(), prefix=API_PREFIX)
app.include_router(get_game_category_router(), prefix=API_PREFIX)
# app.include_router(game_rooms_router, prefix=API_PREFIX)

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_MIDDLEWARE_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_home():
    return Response("Server is running...")
