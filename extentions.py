from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
JWT = JWTManager()

swagger = Swagger(template={
    "swagger":"2.0",
    "info":{
        "title": "api 82",

    },
    "securityDefinitions":{
        "BearerAuth":{
            "type": "apiKey",
            "name":"Authorization",
            "in":"header",
            "description":"Coloca Bearer <tu-token>"
        }
    }
})