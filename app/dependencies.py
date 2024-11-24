import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .database.models import UserModel, UserResponseModel
from .database.config import user_collection

from passlib.hash import bcrypt

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

JWT_SECRET = SECRET_KEY
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def verify_password (plain_password : str, hashed_password : str):
    return bcrypt.verify(plain_password, hashed_password)

async def verify_user(username: str, password: str):
    user = await user_collection.find_one({"username" : username})
    if not user:
        return False
    if not verify_password(password,user["password"]):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        username = payload.get("username")
        user = await user_collection.find_one({"username": username})
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )
    return user