import pandas as pd
def dataTratament (produtos):
    df = pd.DataFrame(produtos)
    df = df[df['gtin'] != '']
    
    # Define o nome do arquivo com timestamp
    df['nome_estabelecimento'] = df['estabelecimento'].apply(lambda x: x.get('nm_fan'))
    df['nome_cidade'] = df['estabelecimento'].apply(lambda x: x.get('mun'))
    df = df.drop(['id', 'ncm', 'cdanp', 'datahora','nrdoc', 'distkm','estabelecimento', 'local', 'valor_desconto','valor_tabela','tempo'], axis=1)
    df = df.rename(columns={
        "desc": "name",
        "valor": "price",
        "nome_estabelecimento": "store"
    })
    df_json = df.to_json(orient='records')

    
    return df_json
