from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm

from dotenv import load_dotenv
import os
from passlib.hash import bcrypt

import jwt

from authlib.integrations.starlette_client import OAuth

from app.database.models import UserModel
from app.dependencies import verify_user
from app.database.config import user_collection
from app.mail import VerifyEmail

router = APIRouter(tags=["Auth"], prefix="/auth")

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

JWT_SECRET = SECRET_KEY


# REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
# oauth = OAuth()
# google = oauth.register(
#     name='google',
#     client_id=os.getenv('GOOGLE_CLIENT_ID'),
#     client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     access_token_params=None,
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     authorize_params=None,
#     api_base_url='https://www.googleapis.com/oauth2/v1/',
#     userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
#     # This is only needed if using openId to fetch user info
#     client_kwargs={'scope': 'openid email profile'},
#     jwks_uri = "https://www.googleapis.com/oauth2/v3/certs"
# )



@router.post('/signin')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Verifikasi user
    user = await verify_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    # Buat payload untuk token
    payload = {
        "email": user["email"],
        "superuser" : user["superuser"]
    }

    # Encode token JWT
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    # Return token
    return {'access_token': token, 'token_type': 'bearer'}

@router.post("/signup", 
            status_code=status.HTTP_201_CREATED
            )
async def create_user(user: UserModel, task : BackgroundTasks):
    # Hash the password before saving
    hashed_password = bcrypt.hash(user.password)

    # Prepare user data
    user_data = user.dict(by_alias=True, exclude=["id"])
    user_data["password"] = hashed_password
    user_data["created_at"] = datetime.utcnow().isoformat()
    user_data["superuser"] = False
    user_data["active"] = True
    user_data["verified"] = False

    # Check if the user already exists
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    # Insert the new user into the database
    result = await user_collection.insert_one(user_data)

    # Fetch and return the created user
    created_user = await user_collection.find_one({"_id": result.inserted_id})

    payload = {
        "email": created_user["email"],
        "superuser" : created_user["superuser"]
    }

    # Encode token JWT
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    task.add_task(VerifyEmail,created_user['email'],token)
    return {"massage" : "User created successfully. Verification email sent."}



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







# @router.get('/google')
# async def login_with_google(request: Request):
#     print(REDIRECT_URI)
#     return await oauth.google.authorize_redirect(request, REDIRECT_URI)


# @router.get('/google/callback')
# async def google_auth_callback(request: Request):
#     token = await oauth.google.authorize_access_token(request)
#     user_info = token.get('userinfo')
    
#     if user_info:
#         # Misalnya: Cek atau buat pengguna di database Anda
#         user = await user_collection.find_one({"email": user_info["email"]})
#         if not user:
#             # Tambahkan pengguna baru ke database jika belum ada
#             new_user = {
#                 "email": user_info["email"],
#                 "password": None,  # Karena autentikasi menggunakan Google
#                 "verified": True,
#                 "active": True,
#                 "superuser": False,
#             }
#             await user_collection.insert_one(new_user)
#             user = new_user
        
#         # Buat token JWT
#         payload = {
#         "email": user["email"],
#         "superuser" : user["superuser"]
#     }

#     # Encode token JWT
#         token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        
#         return {"acces_token" : token}
        
    
#     raise HTTPException(status_code=400, detail="Google authentication failed")

