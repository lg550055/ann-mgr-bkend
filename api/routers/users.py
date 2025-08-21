from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from api.auth_utils import decode_access_token,get_password_hash
from api.database import get_db
from api.models import UserCreate, UserOut
from api.schemas import User
from api.routers.auth import oauth2_scheme

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    creds_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = decode_access_token(token)
    if email is None:
        raise creds_exception

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise creds_exception
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


@router.get("/", response_model=List[UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    _cur_user: User = Depends(get_current_user),
):
    return db.query(User).all()


@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        disabled=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
