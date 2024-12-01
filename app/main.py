from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from .routers import meals, static, users, admin, auth

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

app.include_router(meals.router)
app.include_router(static.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(auth.router)

