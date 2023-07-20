from flask import Blueprint, request
from spooler_task import SpoolerTask
import traceback

from util.json_utils import JsonUtils
from util.service_utils import ServiceUtils
from helpers.chains_helper import ChainsHelper

from util.constants import MONGO_DB_COLLECTION_ORDERS
from services.chain_service import ChainService
from services.process.scheduler_service import SchedulerService

from util.constants import PATH_FOLDERS_ORDER, FILE_PARAM_JSON, FILE_ORDERS_JSON, NAME_JOBS, PATH_LOG

chains_routes = Blueprint('chains_routes', __name__, url_prefix='/api/chains')
chain_service = None  # Variable estática para almacenar el servicio de tareas
scheduler_service = None  # Variable estática para almacenar el servicio de scheduler


@chains_routes.record
def initialize_service(state):
    """
        El decorador @orders_routes.record es específico de Flask y se utiliza para registrar una función de configuración 
        que se ejecuta cuando se registra el blueprint orders_routes. 
    """
    global chain_service, scheduler_service

    # Obtener la instancia de la conexión a MongoDB de la configuración de la aplicación
    mongo_db_connection = state.app.config.get('DATABASE')
    # Obtenemos el clinete de mongoDB para procesos transaccionales
    clientMongoDB = state.app.config.get('CLIENT')

    # Creo una instancia de la clase chain_service
    chain_service = ChainService(
        mongo_db_connection, MONGO_DB_COLLECTION_ORDERS, clientMongoDB)

    # Creo una instancia de la clase scheduler_service
    scheduler_service = SchedulerService(
        mongo_db_connection, MONGO_DB_COLLECTION_ORDERS, clientMongoDB)


@chains_routes.route('/<string:order_id>', methods=['POST'])
def get_chains(order_id):
    try:
        chains = chain_service.get(order_id)

        positions = []
        for i, obj in enumerate(chains):
            obj["position"] = i + 1
            positions.append(i+1)

        options = [item["name"] for item in chains]
        options.append("exito")
        options.append("error")

        return ServiceUtils.success({"data": chains, "options": options, "positions": positions})
    except Exception as e:
        return ServiceUtils.error(e)


@chains_routes.route('/modify', methods=['POST'])
def modify_chain():
    try:
        param = request.get_json()
        order_id = param['order_id']
        chains = param['chains']

        chain_service.modify(order_id, chains)

        return get_chains(order_id)
    except Exception as e:
        return ServiceUtils.error(e)


@chains_routes.route('/params', methods=['POST'])
def params_job():
    try:
        param = request.get_json()
        order_id = param['order_id']
        job_id = param['job_id']

        response = chain_service.get_params(order_id, job_id)

        return ServiceUtils.success(response)
    except Exception as e:
        return ServiceUtils.error(e)


@chains_routes.route('/update_params', methods=['POST'])
def update_params():
    try:
        param = request.get_json()
        order_id = param['order_id']
        job_id = param['job_id']
        params = param['params']
        print(12345, order_id, job_id, params)
        chain_service.update_params(order_id, job_id, params)

        return ServiceUtils.success({"data": {}})
    except Exception as e:
        return ServiceUtils.error(e)


@chains_routes.route('/history')
def history():
    try:
        # response = get_history()
        # response.sort(key=lambda x: x['startDate'], reverse=True)
        return ServiceUtils.success({"data": []})
    except Exception as e:
        return ServiceUtils.error(e)


@chains_routes.route('/process/<string:order_id>', methods=['POST'])
def process(order_id):
    values = {}
    try:
        spooler = SpoolerTask(scheduler_service)
        spooler.logger.info("Orden a procesar " + order_id)
        spooler.get_order(order_id)

        values = ChainsHelper.create_record(
            order_id, spooler.current_job, spooler.log_name)

        JsonUtils.add_item(f"{PATH_FOLDERS_ORDER}/{FILE_ORDERS_JSON}", values)

        spooler.process()

        process_record(spooler.logger, values, "SUCCESS")

        return ServiceUtils.success({})
    except Exception as e:
        trace = traceback.format_exc()
        print(f"Error.........................: {str(e)}\n{trace}")
        spooler.logger.error(
            f"Error.........................: {str(e)}\n{trace}")

        process_record(spooler.logger, values, "ERROR")

        return ServiceUtils.error(e)


def process_record(logger, values, type):
    if type == "SUCCESS":
        values = ChainsHelper.update_record(values, "exitoso", "success")
        logger.info("Proceso termino exitosamente.")
    else:
        values = ChainsHelper.update_record(values, "fallido", "error")
        logger.info("Proceso termino con error.")

    JsonUtils.update_item(
        PATH_FOLDERS_ORDER + "/" + FILE_ORDERS_JSON, 'id', values['id'], values)

    handlers = logger.handlers[:]
    for handler in handlers:
        logger.removeHandler(handler)
        handler.close()


# @chains_routes.route('/log/<string:name>', methods=['POST'])
# def log_data(name):
#     try:
#         response = JsonUtils.read_log_file(f"{PATH_LOG}/{name}")
#         return ServiceUtils.success(response)
#     except Exception as e:
#         return ServiceUtils.error(e)


# @chains_routes.route('/history')
# def history():
#     try:
#         response = get_history()
#         response.sort(key=lambda x: x['startDate'], reverse=True)
#         return ServiceUtils.success({"data": response})
#     except Exception as e:
#         return ServiceUtils.error(e)

# def get_history():
#     return JsonUtils.read_json(f"{PATH_FOLDERS_ORDER}/{FILE_ORDERS_JSON}")

# def get_history():
#     return JsonUtils.read_json(f"{PATH_FOLDERS_ORDER}/{FILE_ORDERS_JSON}")
