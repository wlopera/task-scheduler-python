from flask import Blueprint, request

from util.service_utils import ServiceUtils
from util.constants import MONGO_DB_COLLECTION_USERS
from services.users.auth_service import AuthService
from util.auth.get_token import generar_token

auth_routes = Blueprint('auth_routes', __name__, url_prefix='/api/auth')
auth_service = None  # Variable estática para almacenar el servicio de tareas


@auth_routes.record
def initialize_service(state):
    """
        El decorador @orders_routes.record es específico de Flask y se utiliza para registrar una función de configuración 
        que se ejecuta cuando se registra el blueprint orders_routes. 
    """
    global auth_service
    # Obtener la instancia de la conexión a MongoDB de la configuración de la aplicación
    mongo_db_connection = state.app.config.get('DATABASE')
    # Obtenemos el clinete de mongoDB para procesos transaccionales
    clientMongoDB = state.app.config.get('CLIENT')

    # Creo una instancia de la clase job_service
    auth_service = AuthService(
        mongo_db_connection, MONGO_DB_COLLECTION_USERS, clientMongoDB)


@auth_routes.route('/login', methods=['POST'])
def login():
    try:
        param = request.get_json()
        username = param['username']
        password = param['password']

        result = auth_service.login(username)
        if len(result) == 0:
            return ServiceUtils.success({"data": {"token": None, "description": "Usuario no valido"}})
        elif result['encript'] == password:
            token = generar_token(username)
            return ServiceUtils.success({"data": {"token": token, "description": "Usuario valido"}})
        else:
            return ServiceUtils.success({"data": {"token": None, "description": "Usuario no autorizado"}})
    except Exception as e:
        return ServiceUtils.error(e)
