from uuid import UUID
from fastapi import HTTPException
from jwt.exceptions import InvalidTokenError
import jwt
from backend.config import SECRET_KEY,ALGORITHM

async def decode_token(token:str)->UUID:
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id=UUID(payload.get("sub"))
        if id is None:
            raise HTTPException(status_code=401,detail="User is unauthorized")
    except InvalidTokenError:
        raise HTTPException(status_code=401,detail="User is unauthorized")
    return id