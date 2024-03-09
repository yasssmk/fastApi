from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema
from fastapi import Response, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from .config import settings


oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')


# SECRET_KEY = "this1smy5ecretK3y"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = int(settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        id: str  = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schema.TokenData(id = str(id))
    
    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oath2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not valide credentials", headers = {"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, credentials_exception)