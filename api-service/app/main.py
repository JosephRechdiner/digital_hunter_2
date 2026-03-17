from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db_connection import MysqlManager
from app.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.mysql_manager = MysqlManager()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)