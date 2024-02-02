from fastapi import APIRouter, HTTPException
from typing import List
from models import Operacao
from db_config import get_database
from bson import ObjectId

router = APIRouter()
db = get_database()
operacoes_collection = db["acoes"]

@router.post("/cadastrar")
async def cadastrar_operacao(operacao: Operacao):
    operacao_dict = operacao.model_dump()
    operacao_dict["data"] = operacao_dict["data"].isoformat()
    operacao_id = operacoes_collection.insert_one(operacao_dict).inserted_id
    return {"mensagem": "Operação cadastrada com sucesso", "operacao_id": str(operacao_id)}

@router.get("/operacao/{operacao_id}", response_model=Operacao)
async def obter_operacao(operacao_id: str):
    if not ObjectId.is_valid(operacao_id):
        raise HTTPException(status_code=404, detail="Operação não encontrada")
    
    operacao = operacoes_collection.find_one({"_id": ObjectId(operacao_id)})
    if operacao:
        operacao['_id'] = str(operacao['_id'])
        return operacao
    else:
        raise HTTPException(status_code=404, detail="Operação não encontrada")

@router.get("/operacao/cod/{cod_acao}", response_model=List[Operacao])
async def obter_operacao_cod(cod_acao: str):
    operacoes = operacoes_collection.find({"cod_acao": cod_acao})
    if operacoes:
        operacoes = [dict(operacao, _id=str(operacao['_id'])) for operacao in operacoes]
        return operacoes
    else:
        raise HTTPException(status_code=404, detail="Operações não encontradas para o código de ação fornecido")

@router.get("/list", response_model=List[Operacao])
async def listar_operacoes():
    operacoes = list(operacoes_collection.find())
    for operacao in operacoes:
        operacao['_id'] = str(operacao['_id'])
    return operacoes
