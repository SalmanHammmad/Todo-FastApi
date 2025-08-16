from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoRead(TodoBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedTodos(BaseModel):
    total: int
    page: int
    size: int
    items: List[TodoRead]
