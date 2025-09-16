from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserLogin, UserRead, Token, TokenWithUser
from models.user import User
from services.auth_service import AuthService
from repositories.user_repo import UserRepository
from api.deps import get_db

router = APIRouter()

@router.post("/register", response_model=TokenWithUser)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = AuthService(repo)
    user = service.register_user(user_data)
    token = service.create_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserRead.model_validate(user)
    }

@router.post("/login", response_model=TokenWithUser)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = AuthService(repo)
    user = service.authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = service.create_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserRead.model_validate(user)
    }
