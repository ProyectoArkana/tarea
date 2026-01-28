#Run pip install flask-blueprint
from flask import Blueprint

blueprint_home = Blueprint('home',__name__)
@blueprint_home.route('/home')
def home():
    return {
        'msj': 'desde home'
    }