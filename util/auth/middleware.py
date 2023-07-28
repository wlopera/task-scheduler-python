import jwt
from flask import request, jsonify

SECRET_KEY = 'TaskJobScheduler-wlopera'

def validar_token():
    authorization = request.headers.get('Authorization', '')
    if len(authorization) == 0:
        return jsonify({'message': 'Acceso no autorizado'}), 401

    token = request.headers.get('Authorization', '').split(' ')
    try:
        decoded_token = jwt.decode(token[1], SECRET_KEY, algorithms=['HS256'])
        if 'usuario' in decoded_token:
            # Puedes hacer más verificaciones aquí según tus necesidades, como comprobar roles de usuario, etc.
            return jsonify({'message': 'Token válido'}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'El token ha expirado'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token inválido'}), 401
    return jsonify({'message': 'Acceso no autorizado'}), 401
