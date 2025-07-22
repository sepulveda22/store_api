from pydantic import BaseModel
from schemas.product import Product
from schemas.user import User

class CartItemBase(BaseModel):
    product_id: int
    quantity: int
    
class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True