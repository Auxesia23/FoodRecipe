from fastapi import APIRouter, status, HTTPException, Depends
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from dotenv import load_dotenv
import os


from pydantic import EmailStr

from app.dependencies import CurrentUser
from ..database.config import user_collection, meal_collection
from ..database.models import UserResponseModel, MealCollection


router = APIRouter(tags=["Users"], prefix="/users")






@router.get("/me", response_model=UserResponseModel)
async def get_user(user : CurrentUser) :
    return user



