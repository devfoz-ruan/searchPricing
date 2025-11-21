from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from ..database import Base

class ProdutoNPR(Base):
    __tablename__ = "ProdutoNPR"

    id = Column(Integer, primary_key=True)
    id_prod = Column(Integer, ForeignKey("Produto.id"))
    name = Column(String)
    price = Column(Integer)
    store = Column(String)
    cod_bar = Column(String)
    
    Produto = relationship ("Produto", back_populates="ProdutoNPR")
