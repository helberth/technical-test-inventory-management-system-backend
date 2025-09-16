from passlib.context import CryptContext
from core.security import create_access_token
from models.user import User
from repositories.user_repo import UserRepository
from schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    def register_user(self, user_data: UserCreate) -> User:
        hashed = self.hash_password(user_data.password)
        user = User(username=user_data.username, 
                    email=user_data.email, 
                    hashed_password=hashed)
        return self.repo.create(user)

    def authenticate_user(self, email: str, password: str) -> User | None:
        user = self.repo.get_by_email(email)
        if user and self.verify_password(password, user.hashed_password):
            return user
        return None

    def create_token(self, user: User) -> str:
        return create_access_token({"sub": user.username})
