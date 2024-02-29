from fastapi import FastAPI
from routes import router as operacoes_router
from db_config import get_database

app = FastAPI()

database = get_database()

app.include_router(operacoes_router, prefix="/operacoes")
