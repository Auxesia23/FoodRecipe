from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from .routers import meals, static, users, admin, auth

from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

app.include_router(meals.router)
app.include_router(static.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(auth.router)

