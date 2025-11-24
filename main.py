from fastapi import FastAPI, Query
import requests
from pydantic import BaseModel
import uvicorn
from settings import settings
from .utils import fetchNotaParana, dataTratament
from .data import db_connect
from schemas import Produto, Image



app = FastAPI(title="Busca Menor Preço - Paraná")

BASE_URL = settings.api_notapr

@app.get("/buscar")
def buscar_produtos(
    termo: str = Query(..., min_length=3, description="Termo da busca, ex: 'arroz'"),
    local: str = Query("6gkzqf9vb" , description="Código do local"),
    categoria: int = Query(20, description="ID da categoria"),
    offset: int = Query(0, description="Offset da busca (paginação)"),
    raio: int = Query(20, description="Raio da busca em km"),
    data: int = Query(-1, description="Filtro de data"),
    ordem: int = Query(0, description="Tipo de ordenação"),
    preco_min: float = Query(None, description="Preço mínimo opcional"),
    preco_max: float = Query(None, description="Preço máximo opcional"),
    gtin: str = Query(None, description="Código GTIN do produto")
):
    """
    Faz uma requisição à API do Menor Preço e retorna resultados filtrados.
    """
    params = {
        "local": local,
        "termo": termo,
        "categoria": categoria,
        "offset": offset,
        "raio": raio,
        "data": data,
        "ordem": ordem,
        "gtin": gtin
    }

    try:
        produtos = fetchNotaParana(params)

        # Aplica filtros locais de preço (opcionais)
        if preco_min is not None:
            produtos = [p for p in produtos if p.get("preco", 0) >= preco_min]
        if preco_max is not None:
            produtos = [p for p in produtos if p.get("preco", 0) <= preco_max]
            
        produtos_json = dataTratament(produtos)
            
        return produtos_json

    except requests.RequestException as e:
        return {"erro": str(e)}
 
@app.post("/cadastro")
def cadastro_produtos(
    ProdsEmp: list[Produto],
    url_img: str
):
   try: 
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Produto Values(?, ?, ?, ?)", (ProdsEmp[0].name, ProdsEmp[0].price, ProdsEmp[0].store, ProdsEmp[0].cod_bar))
    produto_id = cursor.lastrowid
    cursor.execute("INSERT INTO Image Values(?, ?)", (produto_id, url_img))
   except: 
    return {f"Produto 1{ProdsEmp[0]} e Produto 2{ProdsEmp[1]}" }

if __name__ == "__main__":
    uvicorn.run(app, host= "localhost", port= 8080)

@app.get("/Login")
def cadastro_cliente():
   return "cadastro feito"

