from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Item(BaseModel):
    taskname: str
    description: Optional[str] = None

class GetItem(BaseModel):
    id: UUID
    taskname: str
    description: Optional[str] = None

class CreateItem(BaseModel):
    id: UUID
    taskname: str
    description: Optional[str] = None