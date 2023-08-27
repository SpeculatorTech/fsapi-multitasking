from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Item(BaseModel):
    name: str
    description: Optional[str] = None

class ItemGet(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None

class ItemCreate(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None