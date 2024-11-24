from fastapi import APIRouter, status, HTTPException, Depends
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from dotenv import load_dotenv
import os

from passlib.hash import bcrypt

from app.dependencies import verify_user, get_current_user

from ..database.config import user_collection
from ..database.models import UserModel, UserResponseModel
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

JWT_SECRET = SECRET_KEY

router = APIRouter(tags=["Users"])





@router.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Verifikasi user
    user = await verify_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    # Ambil user dari database tanpa password
    user_obj = await user_collection.find_one({"username": form_data.username})
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    # Buat payload untuk token
    payload = {
        "username": user_obj["username"],
    }

    # Encode token JWT
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    # Return token
    return {'access_token': token, 'token_type': 'bearer'}

@router.post("/users", 
            status_code=status.HTTP_201_CREATED, 
            response_model=UserResponseModel
            )
async def create_user(user: UserModel):
    # Hash the password before saving
    hashed_password = bcrypt.hash(user.password)

    # Prepare user data
    user_data = user.model_dump(by_alias=True, exclude=["id"])
    user_data["password"] = hashed_password
    user_data["created_at"] = datetime.utcnow().isoformat()

    # Check if the user already exists
    existing_user = await user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    # Insert the new user into the database
    result = await user_collection.insert_one(user_data)

    # Fetch and return the created user
    created_user = await user_collection.find_one({"_id": result.inserted_id})
    return created_user

@router.get("/users/", response_model=UserResponseModel)
async def get_user(user : UserResponseModel = Depends(get_current_user)) :
    return user
