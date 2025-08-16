from fastapi import APIRouter, Depends, Request
from app.schemas.todo import TodoCreate, TodoRead, TodoUpdate, PaginatedTodos
from app.utils.deps import get_current_user
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.todo_dao import TodoDAO
from app.exceptions.http_exceptions import NotFoundException
from app.middlewares.rate_limit import limiter
from app.models.user import User

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=PaginatedTodos)
@limiter.limit("30/minute")
async def list_todos(
    request: Request,
    page: int = 1,
    size: int = 10,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    dao = TodoDAO(session)
    from app.utils.pagination import paginate
    page, size = paginate(page, size)
    total, items = await dao.list(current_user.id, page, size)
    return {"total": total, "page": page, "size": size, "items": items}

@router.post("/", response_model=TodoRead, status_code=201)
async def create_todo(
    request: Request,
    data: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    dao = TodoDAO(session)
    todo = await dao.create(current_user.id, data.title, data.description)
    await session.commit()
    await session.refresh(todo)
    return todo

@router.get("/{todo_id}", response_model=TodoRead)
async def get_todo(
    request: Request,
    todo_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    dao = TodoDAO(session)
    todo = await dao.get(todo_id, current_user.id)
    if not todo:
        raise NotFoundException("Todo not found")
    return todo

@router.patch("/{todo_id}", response_model=TodoRead)
async def update_todo(
    request: Request,
    todo_id: int,
    data: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    dao = TodoDAO(session)
    todo = await dao.get(todo_id, current_user.id)
    if not todo:
        raise NotFoundException("Todo not found")
    updated = await dao.update(todo, **data.dict(exclude_unset=True))
    await session.commit()
    return updated

@router.delete("/{todo_id}", status_code=204)
async def delete_todo(
    request: Request,
    todo_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    dao = TodoDAO(session)
    todo = await dao.get(todo_id, current_user.id)
    if not todo:
        raise NotFoundException("Todo not found")
    await dao.delete(todo)
    await session.commit()
    return None
