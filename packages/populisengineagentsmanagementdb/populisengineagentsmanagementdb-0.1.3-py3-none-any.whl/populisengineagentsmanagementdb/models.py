from pydantic import BaseModel

class Item(BaseModel):
    nome: str
    descricao: str = None
    preco: float
    em_estoque: bool = True
