from repositories.userRepository import UserRepository
from flask_jwt_extended import create_access_token
from datetime import timedelta

class AuthService:
    @staticmethod
    def register(username,email,password):
        return UserRepository.create(username,email,password) 
    
    @staticmethod
    def login(username,password):
        user = UserRepository.find_by_username(username)
        if not user or not user.check_password(password):
            return None
        
        claims = {
            "username": user.username
        }
        token = create_access_token(
        identity= str(user.id),
        additional_claims= claims,
        expires_delta= timedelta (hours=2)
        )   
        return{"access_token":token, 'user':username}