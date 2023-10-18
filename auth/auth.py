import os
from db.db import session
from models.user import UserModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

SECRET_KEY=os.getenv("SECRET_KEY_JWT")
ALGORITHM=os.getenv("ALGORITHM_JWT")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
