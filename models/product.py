from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from database import Base

class Product(Base): 
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=True,)
    stock = Column(Integer, nullable=True)
    
    __table_args__ = (
        UniqueConstraint('name', name='uq_product_name'),
    )