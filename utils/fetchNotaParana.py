import requests
from settings import settings

def fetchNotaParana(params):
    try: 
        response = requests.get(settings.api_notapr, params=params)
        response.raise_for_status()
        data = response.json()

        produtos = data.get("produtos", [])
        return produtos

    except requests.RequestException as e:
        return {"erro": str(e)}
 
