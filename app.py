from flask import Flask
from flask_cors import CORS
from config import Config
from extentions import db, migrate, swagger, JWT
from controllers.UserController import user_bp
from controllers.HomeController import blueprint_home
from routes.auth import auth_bpc
from models.User import User

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)
    JWT.init_app(app)
    app.register_blueprint(user_bp, url_prefix='/api/auth')
    app.register_blueprint(blueprint_home, url_prefix='/api/')
    app.register_blueprint(auth_bpc, url_prefix="/auth/cognito")
    @app.route('/')
    def home():
        return {'msj': 'hola mundo'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        debug=True,
        host='0.0.0.0'
    )
