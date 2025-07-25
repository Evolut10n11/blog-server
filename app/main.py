import os
import logging
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
import sqlalchemy
import databases

# --- Логирование в файл ---
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

# --- Подключение к PostgreSQL ---
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:example@db:5432/blog"
)
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# --- Схема таблицы posts ---
posts = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("content", sqlalchemy.String, nullable=False),
)

# Автоматически создаём таблицу при старте (локально)
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

# --- Инициализируем FastAPI ---
app = FastAPI(title="Мини-блог")

class PostIn(BaseModel):
    title: str
    content: str

class Post(BaseModel):
    id: int
    title: str
    content: str

@app.on_event("startup")
async def startup():
    await database.connect()
    logger.info("✅ Connected to DB")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logger.info("🔌 Disconnected from DB")

@app.get("/posts", response_model=List[Post])
async def list_posts():
    logger.info("GET /posts")
    query = posts.select()
    return await database.fetch_all(query)

@app.post("/posts", response_model=Post)
async def create_post(post: PostIn):
    logger.info(f"POST /posts: {post}")
    query = posts.insert().values(title=post.title, content=post.content)
    post_id = await database.execute(query)
    return {**post.dict(), "id": post_id}
