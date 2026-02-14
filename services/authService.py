from repositories.userRepository import UserRepository

class AuthService:
    @staticmethod
    def register(username,email,password):
        return UserRepository.create(username,email,password) 