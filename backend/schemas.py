from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., title="Name of the product", max_length=100)
    price: float = Field(..., gt=0, title="Price of the product")
    description: Optional[str] = Field(None, title="Description of the product", max_length=300)
    
class ProductCreate(ProductBase):
    name: str = Field(..., title="Name of the product", max_length=100)
    price: float = Field(..., gt=0, title="Price of the product")
    description: Optional[str] = Field(None, title="Description of the product", max_length=300)

class ProductUpdate(ProductBase):
    name: str = Field(..., title="Name of the product", max_length=100)
    price: float = Field(..., gt=0, title="Price of the product")
    description: Optional[str] = Field(None, title="Description of the product", max_length=300)
    last_updated: Optional[datetime] = Field(default_factory=datetime.utcnow, title="Last updated timestamp")

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
