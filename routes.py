from fastapi import APIRouter, HTTPException, Depends
from pymongo.collection import Collection
from typing import List
from models import Operacao
from db_config import get_database
from bson import ObjectId

router = APIRouter()

# Função para calcular operação de compra
def calcular_compra(val: float, qt: int, corretagem: int) -> float:
    taxa = 0.003
    custo_total = (val * qt) + taxa + corretagem
    return custo_total

# Função para calcular operação de venda
def calcular_venda(val: float, qt: int, corretagem: int) -> float:
    taxa = 0.003
    custo_total = (val * qt) - taxa - corretagem
    return custo_total

# Função para buscar operação de compra
def buscar_operacoes_compras(db: Collection) -> List[float]:
    operacoes_compra = db["acoes"].find({"tipo": "compra"}, {"_id": 0, "valor_total": 1})
    valores_compras = [operacao["valor_total"] for operacao in operacoes_compra]
    return valores_compras

# Função para buscar operação de venda
def buscar_operacoes_vendas(db: Collection) -> List[float]:
    operacoes_venda = db["acoes"].find({"tipo": "venda"}, {"_id": 0, "valor_total": 1})
    valores_vendas = [operacao["valor_total"] for operacao in operacoes_venda]
    return valores_vendas

# Função para calcular media
def calcular_media(valores: List[float]) -> float:
    if not valores:
        return 0.0
    return sum(valores) / len(valores)
    
# Rota para cadastrar uma operação    
@router.post("/cadastrar")
async def cadastrar_operacao(operacao: Operacao, db=Depends(get_database)):
    if operacao.tipo == "compra":
        valor_total = calcular_compra(operacao.val, operacao.qt, operacao.corretagem)
    elif operacao.tipo == "venda":
        valor_total = calcular_venda(operacao.val, operacao.qt, operacao.corretagem)
    else:
        raise HTTPException(status_code=400, detail="Tipo de operação inválido. Apenas 'compra' ou 'venda' são permitidos.")
    
    operacao_dict = operacao.model_dump()
    operacao_dict["data"] = operacao_dict["data"].isoformat()
    operacao_dict["valor_total"] = valor_total
    
    operacao_id = db["acoes"].insert_one(operacao_dict).inserted_id
    return {"mensagem": "Operação cadastrada com sucesso", "operacao_id": str(operacao_id)}    

# Rota para listar operação pelo ID
@router.get("/operacao/{operacao_id}", response_model=Operacao)
async def obter_operacao(operacao_id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(operacao_id):
        raise HTTPException(status_code=404, detail="Operação não encontrada")
    
    operacao = db["acoes"].find_one({"_id": ObjectId(operacao_id)})
    if operacao:
        operacao['_id'] = str(operacao['_id'])
        return operacao
    else:
        raise HTTPException(status_code=404, detail="Operação não encontrada")

# Rota para lista operação individual pelo codigo da ação
@router.get("/operacao/cod/{cod_acao}", response_model=List[Operacao])
async def obter_operacao_cod(cod_acao: str, db=Depends(get_database)):
    operacoes = db["acoes"].find({"cod_acao": cod_acao})
    if operacoes:
        operacoes = [dict(operacao, _id=str(operacao['_id'])) for operacao in operacoes]
        return operacoes
    else:
        raise HTTPException(status_code=404, detail="Operações não encontradas para o código de ação fornecido")
    
# Rota para Listar todas as operações
@router.get("/list", response_model=List[Operacao])
async def listar_operacoes(db=Depends(get_database)):
    operacoes = list(db["acoes"].find())
    operacoes_obj = [Operacao(**operacao) for operacao in operacoes]
    for operacao_obj, operacao in zip(operacoes_obj, operacoes):
        operacao_obj.valor_total = float(operacao.get("valor_total", 0.0))
    return operacoes_obj

@router.get("/media_compras")
async def calcular_media_compras(db=Depends(get_database)):
    operacoes_compra = buscar_operacoes_compras(db)
    if not operacoes_compra:
        raise HTTPException(status_code=404, detail="Nenhuma operação de compra foi encontrada")
    
    media_compras = calcular_media(operacoes_compra)
    return {"media_compras": media_compras}

@router.get("/media_vendas")
async def calcular_media_compras(db=Depends(get_database)):
    operacoes_vendas = buscar_operacoes_vendas(db)
    if not operacoes_vendas:
        raise HTTPException(status_code=404, detail="Nenhuma operação de venda foi encontrada")
    
    media_vendas = calcular_media(operacoes_vendas)
    return {"media_compras": media_vendas}