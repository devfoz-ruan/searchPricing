
from sqlalchemy import Column, Integer, String, ForeignKey
from ..database import Base
from sqlalchemy.orm import relationship

class Image(Base):
    __tablename__ = "Image"

    id = Column(Integer, primary_key=True)
    id_prod = Column(Integer, ForeignKey("Produto.id"))
    url = Column(String)

    Produto = relationship("Produto", back_populates="Image")
    
