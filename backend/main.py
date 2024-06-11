from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

import models
import schemas

app = FastAPI(title="Blandskron", version="1.0")

# Inicializar la base de datos
models.init_db()

# Dependency
def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products", response_model=List[schemas.Product], tags=["products"])
async def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products

@app.get("/products/{product_id}", response_model=schemas.Product, tags=["products"])
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products/create/", response_model=schemas.Product, tags=["products"])
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(name=product.name, price=product.price, description=product.description)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{product_id}", response_model=schemas.Product, tags=["products"])
async def update_product(product_id: int, updated_product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product.name = updated_product.name
    product.price = updated_product.price
    product.description = updated_product.description
    product.last_updated = updated_product.last_updated
    db.commit()
    db.refresh(product)
    return product

@app.delete("/products/{product_id}", response_model=schemas.Product, tags=["products"])
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return product
