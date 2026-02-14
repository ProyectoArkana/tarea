from models.users import User
from extensions import db

class UserRepository:

    @staticmethod
    def create(email, password):

        user = User(
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        return user
