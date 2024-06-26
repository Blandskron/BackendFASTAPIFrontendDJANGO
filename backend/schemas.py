# schemas.py
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

import models

class ProductBase(BaseModel):
    name: str = Field(..., title="Name of the product", max_length=100)
    price: float = Field(..., gt=0, title="Price of the product")
    description: Optional[str] = Field(None, title="Description of the product", max_length=300)
    image_url: Optional[str] = Field(None, title="URL of the product image")

class ProductCreate(ProductBase):
    def create_product_in_db(self, db: Session):
        try:
            self.validate()
            db_product = models.Product(
                name=self.name,
                price=self.price,
                description=self.description,
                image_url=self.image_url
            )
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            return db_product
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=str(e))

class ProductUpdate(ProductBase):
    last_updated: Optional[datetime] = Field(default_factory=datetime.utcnow, title="Last updated timestamp")

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
