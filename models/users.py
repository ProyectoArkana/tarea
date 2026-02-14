from extensions import db
#from passlib.hash import bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.column(db.string(80),nullable=False, unique=True )
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def set_password (self, password: str):
        #self.password = bcrypt.hash(password)
        password_encode = password.encoede('utf-8')[:72]
        self.password = bcrypt.hash(password)

    def to_dict(self):
        return {
            "id": self.id,
            'username':self.username,
            "email": self.email
        }
