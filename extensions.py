from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger

db = SQLAlchemy()
migrate = Migrate()

Swagger = Swagger (template={
    "Swagger":"2.0",
    "info":{
        "title": "api_82"
    }

})


