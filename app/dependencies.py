from bson import ObjectId
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from typing import Annotated

from app.database.models import UserResponseModel
from app.database.config import user_collection, meal_collection

from passlib.hash import bcrypt

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

JWT_SECRET = SECRET_KEY
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/signin')

def verify_password (plain_password : str, hashed_password : str):
    return bcrypt.verify(plain_password, hashed_password)

async def verify_user(email: EmailStr, password: str):
   # Cari pengguna berdasarkan email
    user = await user_collection.find_one({"email": email})
    
    # Jika pengguna tidak ditemukan
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Jika password tidak cocok
    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    # Jika akun belum diverifikasi
    if not user.get("verified", False):
        raise HTTPException(status_code=403, detail="Account not verified")
    
    # Jika akun noncative
    if not user.get("active", False):
        raise HTTPException(status_code=403, detail="Your account is inactive. Please contact support to reactivate it.")
    
    # Pengguna valid
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponseModel:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        email = payload.get("email")
        user = await user_collection.find_one({"email": email})
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )
    return user

CurrentUser = Annotated[UserResponseModel, Depends(get_current_user)]

async def get_current_super_user(current_user : CurrentUser) -> UserResponseModel:
    if current_user["superuser"] == False :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Superuser permission required"
        )
    return current_user

CurrentSuperUser = Annotated[UserResponseModel, Depends(get_current_super_user)]


async def is_owner(id:str,user:CurrentUser) -> bool:
    meal_obj = await meal_collection.find_one({"_id" : ObjectId(id)})
    if meal_obj["author"] != user["email"] :
        return False
    return True