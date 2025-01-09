from fastapi import APIRouter, status, HTTPException, Depends
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from dotenv import load_dotenv
import os
from bson import ObjectId


from pydantic import EmailStr

from app.dependencies import CurrentUser
from ..database.config import user_collection, meal_collection, favourites_collection
from ..database.models import UserResponseModel, MealCollection, MealModel


router = APIRouter(tags=["Users"], prefix="/users")






@router.get("/me", response_model=UserResponseModel)
async def get_user(user : CurrentUser) :
    return user


@router.get("/favourite-meals", response_model=MealCollection)
async def get_favourite_meals(user : CurrentUser) :
    pipeline = [
        {
            "$match": {
                "user_id": ObjectId(user['_id'])
            }
        },
        {
            "$lookup": {
                "from": "meals",
                "localField": "meal_id",
                "foreignField": "_id",
                "as": "meal_details"
            }
        },
        {
            "$unwind": "$meal_details"
        },
        {
            "$project": {
                "meal_details._id": 1,
                "meal_details.name": 1,
                "meal_details.category": 1,
                "meal_details.area": 1,
                "meal_details.instructions": 1,
                "meal_details.youtubeUrl": 1,
                "meal_details.imageUrl": 1,
                "meal_details.ingredients": 1,
                "meal_details.author": 1
            }
        }
    ]
    
    # Menjalankan pipeline agregasi
    cursor = favourites_collection.aggregate(pipeline)
    
    # Mengonversi hasil cursor menjadi list of meals
    meals = []
    async for document in cursor:
        meal_data = document['meal_details']
        meal = MealModel(**meal_data)  # Membuat model MealModel dari data meal_details
        meals.append(meal)
    
    # Mengembalikan MealCollection yang berisi list meals
    return MealCollection(meals=meals)

