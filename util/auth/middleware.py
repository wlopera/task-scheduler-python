import jwt
from flask import request, jsonify

SECRET_KEY = 'TaskJobScheduler-wlopera'

def validar_token():
    authorization = request.headers.get('Authorization', '')
    if len(authorization) == 0:
        return jsonify({'message': 'Debe enviar un Token'}), 401

    token = request.headers.get('Authorization', '').split(' ')
    try:
        print(55555555555555)
        decoded_token = jwt.decode(token[1], SECRET_KEY, algorithms=['HS256'])
        print(3333, decoded_token)
        if 'usuario' in decoded_token:
            print(66666)
            # Puedes hacer más verificaciones aquí según tus necesidades, como comprobar roles de usuario, etc.
            return jsonify({'message': 'Token válido'}), 200
    except jwt.ExpiredSignatureError:
        print(7777)
        return jsonify({'message': 'El token ha expirado'}), 401
    except jwt.InvalidTokenError:
        print(888)
        return jsonify({'message': 'Token inválido'}), 401
    print(9999)
    return jsonify({'message': 'Acceso no autorizado'}), 401
