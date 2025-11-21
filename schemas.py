from pydantic import BaseModel


class Produto(BaseModel):
    name: str
    price: float
    store: str
    cod_bar: str

class Image(BaseModel):
    url: str
