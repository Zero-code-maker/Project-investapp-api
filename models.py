from pydantic import BaseModel
from datetime import date

class Operacao(BaseModel):
    cod_acao: str
    val: float
    qt: int
    corretagem: int
    data: date
    tipo: str
