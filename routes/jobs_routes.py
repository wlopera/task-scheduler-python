from flask import Blueprint, request
from util.folder_utils import FolderUtils
from util.json_utils import JsonUtils
from util.service_utils import ServiceUtils
from util.constants import PATH_FOLDERS_ORDER, FILE_PARAM_JSON, NAME_JOBS
from util.constants import MONGO_DB_COLLECTION_ORDERS
from services.jobs_service import JobService

jobs_routes = Blueprint('jobs_routes', __name__, url_prefix='/api/jobs')
job_service = None  # Variable estática para almacenar el servicio de tareas


@jobs_routes.record
def initialize_service(state):
    """
        El decorador @orders_routes.record es específico de Flask y se utiliza para registrar una función de configuración 
        que se ejecuta cuando se registra el blueprint orders_routes. 
    """
    global job_service
    # Obtener la instancia de la conexión a MongoDB de la configuración de la aplicación
    mongo_db_connection = state.app.config.get('DATABASE')

    # Creo una instancia de la clase job_service
    job_service = JobService(
        mongo_db_connection, MONGO_DB_COLLECTION_ORDERS)


@jobs_routes.route('/<string:order_id>', methods=['POST'])
def get_jobs(order_id):
    try:
        jobs = job_service.get(order_id)
        return ServiceUtils.success({"data": jobs})
    except Exception as e:
        return ServiceUtils.error(e)


@jobs_routes.route('/add', methods=['POST'])
def add_job():
    try:
        param = request.get_json()

        order_id = param['order_id']
        name = param['name']

        jobs = job_service.add(name, order_id)
        return ServiceUtils.success({"data": jobs})
    except Exception as e:
        return ServiceUtils.error(e)


@jobs_routes.route('/modify', methods=['POST'])
def modify_job():
    try:
        param = request.get_json()
        order_id = param['order_id']
        new_job = param['new_value']

        jobs = job_service.modify(order_id, new_job)

        return ServiceUtils.success({"data": jobs})
    except Exception as e:
        return ServiceUtils.error(e)


@jobs_routes.route('/delete', methods=['POST'])
def delete_job():
    try:
        param = request.get_json()
        order_id = param['order_id']
        item_id = param['item_id']

        jobs = job_service.delete(order_id, item_id)

        return ServiceUtils.success({"data": jobs})
    except Exception as e:
        return ServiceUtils.error(e)
