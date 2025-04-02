# Fite to validate the data that is being sent and recieved to the API
import datetime
import uuid
from fastapi import HTTPException
from typing import List, Optional
from pydantic import BaseModel, field_validator


class DeliveryItemSchema(BaseModel):
    product_id: uuid.UUID
    quantity: int


class DeliveryCreateSchema(BaseModel):
    purchase_id: uuid.UUID
    address_id: uuid.UUID
    user_id: uuid.UUID
    items: List[DeliveryItemSchema]

class StockResponseSchema(BaseModel):
    product_id: uuid.UUID
    warehouse_id: uuid.UUID
    quantity: int
    last_updated: datetime.datetime


class FilterRequest(BaseModel):
    product: Optional[str] = None
    name: Optional[str] = None
    

    @field_validator('product', mode='before')
    def validate_product_param(cls, v):
        if v is not None:
            try:
                uuid.UUID(v)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="The product parameter must be a valid UUID format",
                )
        return v
    
    @field_validator('warehouse', mode='before')
    def validate_warehouse_param(cls, v):
        if v is not None:
            try:
                uuid.UUID(v)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="The product warehouse must be a valid UUID format",
                )
        return v
