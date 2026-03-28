from extentions import db
from passlib.hash import bcrypt,pbkdf2_sha256

class User(db.Model):
    __tablename__ ='users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    cognito_sub = db.Column(db.String(128), unique=True, nullable=False)
    
    def set_password(self, password: str):
        #self.password = bcrypt.hash(password)
        password_encode = password.encode('utf-8')[:72]
        self.password = pbkdf2_sha256.hash(password_encode)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'cognito_sub': self.cognito_sub
        }
    
    def check_password(self, password :str) -> bool:
        #return bcrypt.verify(password)
        password_encode = password.encode ('utf-8')[:72]
        return pbkdf2_sha256.hash(password_encode)