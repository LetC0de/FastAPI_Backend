from fastapi import APIRouter, Depends, status, Request, BackgroundTasks
from src.user.dtos import UserSchema, UserResponseSchema, UserLoginSchema
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user import controller

user_router = APIRouter(prefix="/user")


@user_router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(body: UserSchema,bg_tasks: BackgroundTasks,db: Session = Depends(get_db)):
    return await controller.register(body, db, bg_tasks)


@user_router.post("/login", status_code=status.HTTP_200_OK)
def login(body: UserLoginSchema, db: Session = Depends(get_db)):
    return controller.login_user(body, db)



@user_router.get("/is_auth", response_model=UserResponseSchema,status_code=status.HTTP_200_OK)
def is_auth(request: Request, db: Session = Depends(get_db)):
    return controller.is_authenticated(request, db)