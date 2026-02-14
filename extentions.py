from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger


db = SQLAlchemy()
migrate = Migrate()

swagger = Swagger(template={
    "swagger":"2.0",
    "info":{
        "title": "api 82"
    }
})