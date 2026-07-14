from src.user.dtos import UserSchema, UserLoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)


def register(body: UserSchema, db: Session):

    #1 username validation 
    is_user_exist = db.query(UserModel).filter(UserModel.username == body.username).first()

    if is_user_exist:
        raise HTTPException(status_code=400, detail="User already exist")
    
    #2 email validation
    is_email_exist = db.query(UserModel).filter(UserModel.email == body.email).first()

    if is_email_exist:
        raise HTTPException(status_code=400, detail="Email already exist")
    
    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        name = body.name,
        username = body.username,
        password = hash_password,
        email = body.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(body: UserLoginSchema, db: Session):
    print(body)

    return "User Logged In Successfully"