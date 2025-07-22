from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.product import Product as ProductModel
from models.user import User
from utils.security import get_current_user
from database import get_db
from schemas.product import Product, ProductCreate

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create products."
        )
    # Referencia a models/product.py
    existing_product = db.query(ProductModel).filter(ProductModel.name == product.name).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exists."
        )
    
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/{product_id}", response_model=Product)  
async def read_product(product_id: int,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    return db_product