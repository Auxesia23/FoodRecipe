from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from dotenv import load_dotenv
import os
from passlib.hash import bcrypt

import jwt

from app.database.models import UserModel
from app.dependencies import verify_user
from app.database.config import user_collection
from app.mail import VerifyEmail

router = APIRouter(tags=["Auth"], prefix="/auth")

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

JWT_SECRET = SECRET_KEY


@router.post('/signin')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Verifikasi user
    user = await verify_user(form_data.username, form_data.password)

    # Ambil user dari database tanpa password
    user_obj = await user_collection.find_one({"email": form_data.username})
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    # Buat payload untuk token
    payload = {
        "email": user_obj["email"],
    }

    # Encode token JWT
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    # Return token
    return {'access_token': token, 'token_type': 'bearer'}

@router.post("/signup", 
            status_code=status.HTTP_201_CREATED
            )
async def create_user(user: UserModel):
    # Hash the password before saving
    hashed_password = bcrypt.hash(user.password)

    # Prepare user data
    user_data = user.model_dump(by_alias=True, exclude=["id"])
    user_data["password"] = hashed_password
    user_data["created_at"] = datetime.utcnow().isoformat()

    # Check if the user already exists
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    # Insert the new user into the database
    result = await user_collection.insert_one(user_data)

    # Fetch and return the created user
    created_user = await user_collection.find_one({"_id": result.inserted_id})

    # Buat payload untuk token
    payload = {
        "email": created_user["email"],
    }

    # Encode token JWT
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    verification = await VerifyEmail(created_user["email"], token)
    return {"massage" : verification}



@router.get("/verifyemail",description="Verify email with token")
async def email_verification(token : str) :
    try:
        # Decode JWT
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token: email missing")

        # Update user verification status
        user = await user_collection.find_one_and_update(
            {"email": email},
            {"$set": {"verified": True}}
        )

        # Handle case where user is not found
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "Email successfully verified"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
