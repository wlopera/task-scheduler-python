import jwt
import datetime

SECRET_KEY = 'TaskJobScheduler-wlopera'


def generar_token(username):
    # Generar el token con una fecha de expiración de 1 hora.
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    # Generar el token con una fecha de expiración de 10 minutos.
    #expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

    token = jwt.encode({'usuario': username, 'APP': "TaskJobSchduler", 'exp': expiration},
                       SECRET_KEY, algorithm='HS256')
    return token
