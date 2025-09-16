from pydantic import BaseModel, Field, model_validator
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    quantity: int = Field(..., ge=0, description="Quantity must be 0 or greater")
    image_url: Optional[str] = Field(None, max_length=255)
    
    @model_validator(mode='after')
    def validate_positive_price(cls, values):
        if values.price <= 0:
            raise ValueError('Price must be greater than 0')
        return values
        
    @model_validator(mode='after')
    def validate_non_negative_quantity(cls, values):
        if values.quantity < 0:
            raise ValueError('Quantity must be 0 or greater')
        return values

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    price: Optional[float] = Field(None, gt=0, description="Price must be greater than 0")
    quantity: Optional[int] = Field(None, ge=0, description="Quantity must be 0 or greater")
    image_url: Optional[str] = Field(None, max_length=255)
    
    @model_validator(mode='after')
    def validate_positive_price(cls, values):
        if values.price is not None and values.price <= 0:
            raise ValueError('Price must be greater than 0')
        return values
        
    @model_validator(mode='after')
    def validate_non_negative_quantity(cls, values):
        if values.quantity is not None and values.quantity < 0:
            raise ValueError('Quantity must be 0 or greater')
        return values

class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
