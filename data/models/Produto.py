
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from ..database import Base

class Produto(Base):
    __tablename__ = "Produto"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    store = Column(String)
    cod_bar = Column(String)
    
    Images= relationship("Image", back_populates="Produto")
    ProdutoNPR = relationship ("ProdutoNPR", back_populates="Produto")
