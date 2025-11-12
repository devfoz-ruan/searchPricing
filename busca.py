from fastapi import FastAPI, Query
import requests
import pandas as pd
from datetime import datetime

app = FastAPI(title="Busca Menor Preço - Paraná")

BASE_URL = "https://menorpreco.notaparana.pr.gov.br/api/v1/produtos"
@app.get("/buscar")
def buscar_produtos(
    termo: str = Query("arroz", description="Termo da busca, ex: 'arroz'"),
    local: str = Query("6gkzqf9vb", description="Código do local"),
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
        # Faz a requisição à API pública
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        produtos = data.get("produtos", [])

        # Aplica filtros locais de preço (opcionais)
        if preco_min is not None:
            produtos = [p for p in produtos if p.get("preco", 0) >= preco_min]
        if preco_max is not None:
            produtos = [p for p in produtos if p.get("preco", 0) <= preco_max]
            
        if produtos:
            # Cria um DataFrame com os produtos
            
            df = pd.DataFrame(produtos)
           
            df = df[df['gtin'] != '']
            
            # Define o nome do arquivo com timestamp
            df['nome_estabelecimento'] = df['estabelecimento'].apply(lambda x: x.get('nm_fan'))
            df['nome_cidade'] = df['estabelecimento'].apply(lambda x: x.get('mun'))
            df = df.drop(['id', 'ncm', 'cdanp', 'datahora','nrdoc', 'distkm','estabelecimento', 'local'], axis=1)
        
            filename = "resultados_busca.xlsx"
            
            # Salva o DataFrame como Excel
            
            df.to_excel(filename, sheet_name='Resultados', index=False)
            
        return {"total": len(produtos), "resultados": produtos, "arquivo": filename if produtos else None}

    except requests.RequestException as e:
        return {"erro": str(e)}
    