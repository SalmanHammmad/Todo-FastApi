from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.services.security import decode_token
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.user_dao import UserDAO
from app.exceptions.http_exceptions import UnauthorizedException

bearer_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_session),
):
    if creds is None:
        raise UnauthorizedException("Missing credentials")
    subject = decode_token(creds.credentials)
    user = await UserDAO(session).get_by_email(subject)
    if not user:
        raise UnauthorizedException("User not found")
    return user
