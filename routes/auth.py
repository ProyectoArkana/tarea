from flask import Blueprint, request, jsonify
from auth.cognito_service import create_cognito_user, login_cognito, associate_mfa_token, verify_mfa_setup
from models.User import User
from extentions import db

auth_bpc = Blueprint ("cognito_auth", __name__)

@auth_bpc.route("/register", methods=["POST"])
def register():
    """
    Registrar usuario en Cognito
    ---
    tags:
        - Cognito
    consumes:
        - application/json
    parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            required:
                - email
                - password
            properties:
                email:
                    type: string
                password:
                    type: string
                nombre:
                    type: string
    responses:
        201:
            description: Usuario creado correctamente
        400:
            description: Datos incompletos
    """
    data = request.json
    email = data.get("email")
    password = data.get ("password")
    nombre = data.get ("nombre")

    if not email or not password:
        return jsonify({"error":"Datos incompletos"}), 400
    
    try: 
        sub = create_cognito_user(email, password)

        user = User(
            username=nombre,
            email=email,
            cognito_sub=sub
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"message":"Usuario creado correctamente"}), 201
    
    except Exception as e:
        return jsonify({"error":str(e)}), 500

@auth_bpc.route("/login", methods=["POST"])
def login():
    """
    Iniciar sesión en Cognito (Detecta desafío MFA)
    ---
    tags:
        - Cognito
    parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            required:
                - email
                - password
            properties:
                email:
                    type: string
                password:
                    type: string
    responses:
        200:
            description: Login exitoso o requiere configuración MFA
        401:
            description: Credenciales inválidas
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y password requeridos"}), 400

    try:
        response = login_cognito(email, password)

        # Si el User Pool requiere MFA y es el primer login
        if response.get("ChallengeName") == "MFA_SETUP":
            session = response.get("Session")
            mfa_data = associate_mfa_token(session)
            
            return jsonify({
                "status": "MFA_SETUP_REQUIRED",
                "secret_code": mfa_data["SecretCode"], # <--- Para generar el QR en React
                "session": mfa_data["Session"]          # <--- Necesario para verificar
            }), 200

        return jsonify({
            "status": "SUCCESS",
            "auth_result": response.get("AuthenticationResult")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 401

@auth_bpc.route("/verify-mfa", methods=["POST"])
def verify_mfa():
    """
    Verificar primer código de App Autenticadora (Activa MFA)
    ---
    tags:
        - Cognito
    parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            required:
                - session
                - code
            properties:
                session:
                    type: string
                code:
                    type: string
    responses:
        200:
            description: MFA activado correctamente
        400:
            description: Código inválido
    """
    data = request.json
    print(f"DATOS RECIBIDOS: {data}")
    session = data.get("session")
    code = data.get("code")

    if not session or not code:
        return jsonify({"error": "Sesión y código requeridos"}), 400

    try:
        verify_mfa_setup(session, code)
        return jsonify({"message": "MFA activado con éxito. Procede al login normal."}), 200
    except Exception as e:
        return jsonify({"error": f"Error al verificar: {str(e)}"}), 400