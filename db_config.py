import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DATABASE_NAME")

if DB_NAME is None or MONGO_URI is None:
    print("Banco de dados não encontrado")
else:
    print(f"Concetado ao Banco de dados")

def get_database():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]
