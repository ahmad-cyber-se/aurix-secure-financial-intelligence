from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
from jwt import InvalidTokenError

from app.core.config import settings

password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError):
        return False


def create_access_token(user_id: UUID) -> tuple[str, str, datetime]:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.jwt_expire_minutes)
    jti = str(uuid4())
    payload = {
        "sub": str(user_id),
        "jti": jti,
        "iat": now,
        "exp": expires_at,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token, jti, expires_at


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
        )
    except InvalidTokenError as exc:
        raise ValueError("Invalid or expired access token") from exc
