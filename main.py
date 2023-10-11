from typing import List
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from schemas.user import UserSerializer
from models.user import UserModel
from db.db import session

app = FastAPI()

origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "hello"}

@app.get("/api/users/all", response_model=List[UserSerializer], status_code=status.HTTP_200_OK)
async def all_users():
    users = session.query(UserModel).all()

    return users

@app.post("/api/users/create", response_model=UserSerializer, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserSerializer):
    new_user = UserModel(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        password=user.password,
    )

    check_user = session.query(UserModel).filter(user.username==new_user.username, user.email==new_user.email).first()

    if check_user is not None:
        raise HTTPException(status_code=400, detail="User already exists")
    
    session.add(new_user)
    session.commit()

    return new_user

@app.post("/api/users/login", response_model=UserSerializer, status_code=status.HTTP_200_OK)
async def login_user(user: UserSerializer):
    auth_user = session.query(UserModel).filter(UserModel.username==user.username, UserModel.password==user.password).first()

    if auth_user is None:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return auth_user
