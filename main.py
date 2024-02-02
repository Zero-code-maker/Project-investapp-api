from fastapi import FastAPI
from routes import router as operacoes_router

app = FastAPI()

app.include_router(operacoes_router, prefix="/operacoes")
