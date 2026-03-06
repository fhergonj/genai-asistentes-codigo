from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import db
from schemas import ProductCreate, ProductUpdate, ProductRead

app = FastAPI(title="Product API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost", "127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Product API"}


@app.get("/products", response_model=list[ProductRead])
async def list_products() -> list[ProductRead]:
    """
    List all products.

    Returns:
        list[ProductRead]: List of all products in the database.
    """
    products = db.list_products()
    return [ProductRead(id=p.id, title=p.title, price=p.price) for p in products]


@app.get("/products/{product_id}", response_model=ProductRead)
async def get_product(product_id: int) -> ProductRead:
    """
    Get a single product by ID.

    Args:
        product_id: The ID of the product to retrieve.

    Returns:
        ProductRead: The product data.

    Raises:
        HTTPException: 404 if product not found.
    """
    product = db.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
    return ProductRead(id=product.id, title=product.title, price=product.price)


@app.post("/products", response_model=ProductRead, status_code=201)
async def create_product(product_data: ProductCreate) -> ProductRead:
    """
    Create a new product.

    Args:
        product_data: The product data to create.

    Returns:
        ProductRead: The created product with assigned ID.

    Raises:
        HTTPException: 422 if validation fails.
    """
    from models import Product

    new_product = Product(id=0, title=product_data.title, price=product_data.price)
    created = db.create_product(new_product)
    return ProductRead(id=created.id, title=created.title, price=created.price)


@app.put("/products/{product_id}", response_model=ProductRead)
async def update_product(product_id: int, product_data: ProductUpdate) -> ProductRead:
    """
    Update an existing product.

    Args:
        product_id: The ID of the product to update.
        product_data: The product data to update (all fields optional).

    Returns:
        ProductRead: The updated product.

    Raises:
        HTTPException: 404 if product not found.
        HTTPException: 422 if validation fails.
    """
    existing_product = db.get_product(product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

    updated_title = product_data.title if product_data.title is not None else existing_product.title
    updated_price = product_data.price if product_data.price is not None else existing_product.price

    from models import Product

    updated_product = Product(id=product_id, title=updated_title, price=updated_price)
    result = db.update_product(product_id, updated_product)
    return ProductRead(id=result.id, title=result.title, price=result.price)


@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: int) -> None:
    """
    Delete a product by ID.

    Args:
        product_id: The ID of the product to delete.

    Raises:
        HTTPException: 404 if product not found.
    """
    existing_product = db.get_product(product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

    db.delete_product(product_id)
