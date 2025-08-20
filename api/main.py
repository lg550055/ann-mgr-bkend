from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.models import UserInDB, UserCreate, User
from api.auth_utils import create_access_token, decode_access_token, verify_password, get_password_hash

app = FastAPI()

fake_users_db = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.post("/user/register", response_model=User)
async def register_user(user: UserCreate):
    if user.email in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already registered"
        )
    hashed_password = get_password_hash(user.password)

    fake_users_db[user.email] = {
        "email": user.email,
        "hashed_password": hashed_password,
        "disabled": False
    }
    return User(email=user.email, disabled=False)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

