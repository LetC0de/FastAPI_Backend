from fastapi import APIRouter, Depends, status
from src.user.dtos import UserSchema, UserResponseSchema, UserLoginSchema
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user import controller

user_router = APIRouter(prefix="/user")


@user_router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def register(body: UserSchema, db: Session = Depends(get_db)):
    return controller.register(body, db)


@user_router.post("/login", status_code=status.HTTP_200_OK)
def login(body: UserLoginSchema, db: Session = Depends(get_db)):
    return controller.login_user(body, db)
