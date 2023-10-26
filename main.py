from typing import List
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from jose import jwt, JWTError


from schemas.user import JWTToken, UserSerializer
from models.user import UserModel
from db.db import session
from auth.auth import bcrypt_context, SECRET_KEY, ALGORITHM

app = FastAPI()

origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# useless route
@app.get("/")
async def home():
    return { "message" : "hello" }

# this route should only be used as a testing route
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
        password=bcrypt_context.hash(user.password),
    )

    # checking if the user already exists - usernames and emails should be unique 
    check_username = session.query(UserModel).filter_by(username=user.username).first()
    check_email = session.query(UserModel).filter_by(email=user.email).first()

    if check_username or check_email:
        raise HTTPException(status_code=400, detail="User already exists")
    
    session.add(new_user)
    session.commit()

    return new_user

@app.post("/api/users/login", response_model=JWTToken, status_code=status.HTTP_200_OK)
async def login_user(user: UserSerializer):
    # personally I don't like the way this code is written but for now I'm not interested in refactoring it
    
    # first we validate user credentials

    # before verifying the hashed password we must verify if the username exists
    auth_user = session.query(UserModel).filter(UserModel.username==user.username).first()

    if not auth_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    validate = bcrypt_context.verify(user.password, auth_user.password)

    if not validate:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # after it we generate access token
    encode = {"sub": user.username, "id": str(user.user_id)}
    expires = datetime.utcnow() + timedelta()
    encode.update({"exp": expires})
    token = jwt.encode(encode, SECRET_KEY, ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}
