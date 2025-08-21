from fastapi import FastAPI
from api.database import engine
from api.schemas import Base
from api.routers import auth, users

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def health_check():
    return {"status": "ok"}
