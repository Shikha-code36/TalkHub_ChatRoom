from fastapi import APIRouter, Form

from serviceworkers.authentication_service import register_user, authenticate_user
from models.user import UserCreate

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    await register_user(user)
    return {"message": "User registered successfully"}

@router.post("/register/verify")
async def register(user: UserCreate):
    await register_user(user)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    form_data = {"username": username, "password": password}
    return await authenticate_user(form_data)
