from flask import Blueprint, request
from spooler_task import SpoolerTask
import traceback

from util.json_utils import JsonUtils
from util.service_utils import ServiceUtils
from helpers.chains_helper import ChainsHelper
from util.constants import PATH_FOLDERS_ORDER, FILE_PARAM_JSON, FILE_ORDERS_JSON, NAME_JOBS, PATH_LOG

chains_routes = Blueprint('chains_routes', __name__, url_prefix='/api/chains')


@chains_routes.route('/<string:name>', methods=['POST'])
def chains(name):
    try:
        response = get_chains(name)
        return ServiceUtils.success(response)
    except Exception as e:
        return ServiceUtils.error(e)


@chains_routes.route('/modify', methods=['POST'])
def modify_chain():
    try:
        param = request.get_json()
        order_id = param['order_id']
        old_position = int(param['old_id']) - 1
        new_position = int(param['id']) - 1

        data = ChainsHelper.getDataBase(param)

        JsonUtils.remove_item_by_position(
            f"{PATH_FOLDERS_ORDER}/{order_id}/{FILE_PARAM_JSON}", old_position)

        JsonUtils.add_item(
            f"{PATH_FOLDERS_ORDER}/{order_id}/{FILE_PARAM_JSON}", data, new_position)

        response = get_chains(order_id)

        record = [item for item in response['data']
                  if "name" in item and item["name"] == param['name']]

        position = int(record[0]['id']) - 1

        response['data'][position]["active"] = True

        return ServiceUtils.success(response)
    except Exception as e:
        return ServiceUtils.error(e)


@chains_routes.route('/params', methods=['POST'])
def params_job():
    try:
        param = request.get_json()
        order_id = param['order_id']
        job_id = param['job_id']

        response = get_params(order_id, job_id)

        return ServiceUtils.success(response)
    except Exception as e:
        return ServiceUtils.error(e)


@chains_routes.route('/update_params', methods=['POST'])
def update_params_job():
    try:
        param = request.get_json()
        order_id = param['order_id']
        job_id = param['job_id']
        new_data = param['data']

        JsonUtils.write_json(
            f"{PATH_FOLDERS_ORDER}/{order_id}/{NAME_JOBS}/{job_id}/{FILE_PARAM_JSON}", new_data)

        return ServiceUtils.success({})
    except Exception as e:
        return ServiceUtils.error(e)


@chains_routes.route('/process/<string:name>', methods=['POST'])
def process(name):
    values = {}
    try:
        spooler = SpoolerTask()
        spooler.logger.info("Orden a procesar " + name)
        spooler.get_chains(name)
        
        values = ChainsHelper.create_record(
            name, spooler.current_job, spooler.log_name)
        
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


@chains_routes.route('/log/<string:name>', methods=['POST'])
def log_data(name):
    try:
        response = JsonUtils.read_log_file(f"{PATH_LOG}/{name}")
        return ServiceUtils.success(response)
    except Exception as e:
        return ServiceUtils.error(e)


@chains_routes.route('/history')
def history():
    try:
        response = get_history()
        response.sort(key=lambda x: x['startDate'], reverse=True)
        return ServiceUtils.success({"data": response})
    except Exception as e:
        return ServiceUtils.error(e)


def get_chains(name):
    chains = JsonUtils.read_json(
        f"{PATH_FOLDERS_ORDER}/{name}/{FILE_PARAM_JSON}")
    positions = []
    for i, obj in enumerate(chains):
        obj["id"] = i + 1
        positions.append(i+1)

    options = [item["name"] for item in chains]
    options.append("exito")
    options.append("error")

    return {"data": chains, "options": options, "positions": positions}


def get_params(order_id, job_id):
    return JsonUtils.read_json(f"{PATH_FOLDERS_ORDER}/{order_id}/{NAME_JOBS}/{job_id}/{FILE_PARAM_JSON}")


def get_history():
    return JsonUtils.read_json(f"{PATH_FOLDERS_ORDER}/{FILE_ORDERS_JSON}")


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
