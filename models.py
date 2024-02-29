from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class TipoOperacao(str, Enum):
    compra = "compra"
    venda = "venda"

class Operacao(BaseModel):
    cod_acao: str
    val: float
    qt: int
    corretagem: int
    data: date
    tipo: TipoOperacao
    valor_total: Optional[float] = None

    @staticmethod
    def calcular_valor_total(val: float, qt: int, corretagem: int, tipo: TipoOperacao) -> float:
        if tipo == TipoOperacao.compra:
            return val * qt + 0.003 + corretagem
        elif tipo == TipoOperacao.venda:
            return val * qt - 0.003 - corretagem
        else:
            return 0.0

    @classmethod
    def validate(cls, value):
        valor_total = cls.calcular_valor_total(value.val, value.qt, value.corretagem, value.tipo)
        return cls(**value.dict(), valor_total=valor_total)