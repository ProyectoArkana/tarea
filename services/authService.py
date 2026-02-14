from repositories.userRepository import UserRepository

class AuthService:

    @staticmethod
    def register(data):

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise ValueError("Correo y password son requeridos")

        user = UserRepository.create(email), password

        return user
