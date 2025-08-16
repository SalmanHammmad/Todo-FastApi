from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from app.models.todo import Todo
from typing import List, Optional, Tuple

class TodoDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self, owner_id: int, page: int, size: int) -> Tuple[int, List[Todo]]:
        stmt = select(Todo).where(Todo.owner_id == owner_id).order_by(Todo.created_at.desc()).offset((page - 1) * size).limit(size)
        total_stmt = select(func.count()).select_from(Todo).where(Todo.owner_id == owner_id)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        total_result = await self.session.execute(total_stmt)
        total = total_result.scalar_one()
        return total, items

    async def get(self, todo_id: int, owner_id: int) -> Optional[Todo]:
        result = await self.session.execute(select(Todo).where(Todo.id == todo_id, Todo.owner_id == owner_id))
        return result.scalars().first()

    async def create(self, owner_id: int, title: str, description: str | None) -> Todo:
        todo = Todo(owner_id=owner_id, title=title, description=description)
        self.session.add(todo)
        await self.session.flush()
        return todo

    async def update(self, todo: Todo, **data) -> Todo:
        for k, v in data.items():
            if v is not None:
                setattr(todo, k, v)
        await self.session.flush()
        return todo

    async def delete(self, todo: Todo) -> None:
        await self.session.delete(todo)
