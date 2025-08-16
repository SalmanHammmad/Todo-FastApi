from fastapi import APIRouter, Depends, status, Request
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.user_dao import UserDAO
from app.services import security
from app.exceptions.http_exceptions import ConflictException, UnauthorizedException
from app.middlewares.rate_limit import limiter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(request: Request, data: UserCreate, session: AsyncSession = Depends(get_session)):
    dao = UserDAO(session)
    existing = await dao.get_by_email(data.email)
    if existing:
        raise ConflictException("Email already registered")
    user = await dao.create(data.email, security.hash_password(data.password))
    await session.commit()
    return user

@router.post("/login")
@limiter.limit("10/minute")
async def login(request: Request, data: UserLogin, session: AsyncSession = Depends(get_session)):
    dao = UserDAO(session)
    user = await dao.get_by_email(data.email)
    if not user or not security.verify_password(data.password, user.hashed_password):
        raise UnauthorizedException("Invalid credentials")
    token = security.create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}
