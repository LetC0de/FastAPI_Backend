from src.user.dtos import UserSchema, UserLoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException, status , Request
from pwdlib import PasswordHash
from src.utils.settings import settings
from datetime import datetime, timedelta
from jwt.exceptions import InvalidTokenError
from src.utils.mail import send_email
import jwt

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)


async def register(body: UserSchema, db: Session):

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

    #email confirmation
    res = await send_email(new_user.email)
    print(res)

    return new_user


def login_user(body: UserLoginSchema, db: Session):
    

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found") 
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    
    if not verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")
    
    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)

    token = jwt.encode({"_id": user.id,"exp": exp_time.timestamp()}, settings.SECRET_KEY, settings.ALGORITHM)
    
    return {"token": token}


def is_authenticated(request:Request, db:Session):
    try:
        token = request.headers.get("authorization")

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")
        
        token =token.split(" ")[-1]

        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id = data.get("_id")

        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")