from flask import Blueprint, jsonify, request
from services.authService import AuthService

user_bp = Blueprint('auth', __name__)

@user_bp.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    try:
        user = AuthService.register(data['username'], data['password'])
        return jsonify(user.to_dict()), 201

    except ValueError as e:
        return jsonify({'msj': str(e)}), 400



