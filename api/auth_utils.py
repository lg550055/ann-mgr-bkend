from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt, JWTError
from passlib.context import CryptContext
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_key")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 9  # accounts for utc difference

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        print("--------s Starting token decoding: " + token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("--------s Token decoding completed")
        email = payload.get("sub")
        return email
    except JWTError as err:
        print("--------s Token decoding failed: " + str(err))
        return None

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
