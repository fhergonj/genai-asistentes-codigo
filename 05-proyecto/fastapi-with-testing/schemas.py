from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Product title")
    price: float = Field(..., gt=0, description="Product price")


class ProductUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, description="Product title")
    price: float | None = Field(None, gt=0, description="Product price")


class ProductRead(BaseModel):
    id: int
    title: str
    price: float
