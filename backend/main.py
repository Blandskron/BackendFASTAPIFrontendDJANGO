from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    price: float

products = [
    Product(id=1, name="Laptop", price=999.99),
    Product(id=2, name="Mouse", price=19.99),
    Product(id=3, name="Keyboard", price=49.99)
]

@app.get("/products", response_model=List[Product])
async def get_products():
    return products

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products", response_model=Product)
async def create_product(product: Product):
    products.append(product)
    return product

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, updated_product: Product):
    for idx, product in enumerate(products):
        if product.id == product_id:
            products[idx] = updated_product
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}", response_model=Product)
async def delete_product(product_id: int):
    for idx, product in enumerate(products):
        if product.id == product_id:
            deleted_product = products.pop(idx)
            return deleted_product
    raise HTTPException(status_code=404, detail="Product not found")
