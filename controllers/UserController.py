from flask import Blueprint,request,jsonify
from services.authService import AuthService
from flasgger import swag_from

user_bp = Blueprint('auth',__name__)

@user_bp.route('/register',methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'parameters':[{'name': 'body', 'in': 'body', 'schema': {
        'type': 'object',
        'propierties':{
            'username': {'type': 'string'},
            'email':{'type': 'string'},
            'password':{'type':'string'}
        },
        'required':['username','email','password']
    }
    }],
    'responses':{200: {'description':'Usuario creado'}}
})

def register():
    data = request.get_json();
    try:
        user = AuthService.register(data['username'],data['email'],data['password'])
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({'msj': str(e)}), 400
    
@user_bp.route('/login', methods=['POST'])
@swag_from({
    'tags':['Auth'],
    'parameters':[
        {'name': 'body', 'in': 'body', 'schema': {
            'type': 'object',
            'properties':{
                'username':{'type':'string'},
                'password': {'type':'string'}
            },
            'required':['username', 'password']
        }}
    ],
    'responses':{200:{'description':'Token'}}
})
    
def login():
    data = request.get_json();
    result = AuthService.login(data['username'],data['password'])
    if not result:
        return jsonify({'message': 'Credenciales invalidas'}),401
    
    token = result['access_token']
    user = result['user']
    return jsonify({'access_token':token, 'user':user.to_dict()}),200