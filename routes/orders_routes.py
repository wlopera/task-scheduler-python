from flask import Blueprint, request
from util.folder_utils import FolderUtils
from util.json_utils import JsonUtils
from util.service_utils import ServiceUtils
from util.constants import PATH_FOLDERS_ORDER, FILE_PARAM_JSON, NAME_JOBS
from util.constants import MONGO_DB_COLLECTION_ORDERS
import json
from bson import ObjectId

orders_routes = Blueprint('orders_routes', __name__, url_prefix='/api/orders')
mongo_db_connection = None  # Variable estática para almacenar la conexión


@orders_routes.route('/', methods=['GET'])
def get_orders():
    """
        Consultar los directorios de la carpeta requerida..
    Author:
        wlopera
    Return:
            dict: Carpetas de una ruta
    """
    try:
        orders = get_orders_folders()
        return ServiceUtils.success({"data": orders})
    except Exception as e:
        return ServiceUtils.error(e)


@orders_routes.route('/add/<string:name>', methods=['POST'])
def add_order(name):
    """
        Crear carpeta.
    Args:
        name (str): Nombre de la carpeta a crear
    Author:
        wlopera
    Return:
            dict: Resultado del procesamiento
    """
    try:
        collection = orders_routes.mongo_db_connection[MONGO_DB_COLLECTION_ORDERS]
        resultado = collection.insert_one({
            "name": name,
            "chains": [],
            "jobs": []
        })

        print("Documento creado con el ID:", resultado.inserted_id)

        orders = get_orders_folders()
        activate_order(orders, name)
        return ServiceUtils.success({"data": orders})
    except Exception as e:
        return ServiceUtils.error(e)


@orders_routes.route('/modify', methods=['POST'])
def modify_order():
    """
        Modificar nombre de carpeta.
    Args:
        old_value (str): Nombre de la carpeta a modificar
        new_value (str): Nombre nuevo de la carpeta a modificar
    Author:
        wlopera
    Return:
            dict: Resultado del procesamiento
    """
    try:
        param = request.get_json()
        old_name = param['old_value']
        new_name = param['new_value']
        
        print('old_name:',old_name)
        print('new_name:',new_name)

        collection = orders_routes.mongo_db_connection[MONGO_DB_COLLECTION_ORDERS]
        # Definir los criterios de búsqueda para encontrar los documentos a actualizar
        filtro = {"_id": ObjectId(old_name['id'])}

        # Actualizar el valor en la tabla utilizando el método update_one()
        result = collection.update_one(filtro, {"$set": {"name": new_name['name']}})
        print(12345, result.modified_count)

        orders = get_orders_folders()
        activate_order(orders, new_name)
        return ServiceUtils.success({"data": orders})
    except Exception as e:
        return ServiceUtils.error(e)


@orders_routes.route('/delete/<string:id>', methods=['POST'])
def delete_order(id):
    """
        Eliminar carpeta.
    Args:
        id (str): Identificador de la carpeta a eliminar.
    Author:
        wlopera
    Return:
            dict: Resultado del procesamiento
    """
    try:
        collection = orders_routes.mongo_db_connection[MONGO_DB_COLLECTION_ORDERS]
        response = collection.delete_one({'_id': ObjectId(id)})
        if response.deleted_count > 0:
            print("Documento eliminado exitosamente.")
        else:
            print("No se encontró el documento con el ID:", id)
            
        orders = get_orders_folders()
        return ServiceUtils.success({"data": orders})
    except Exception as e:
        return ServiceUtils.error(e)


def get_orders_folders():
    """
        Lee los directorios de una ruta requerida.
    Author: 
        wlopera
    Return:
        dict: Carpetas de una ruta
    """
    collection = orders_routes.mongo_db_connection[MONGO_DB_COLLECTION_ORDERS]
    reponse = collection.find()
    json_response = [json.dumps(item, default=str) for item in reponse]
    orders = []
    for item in json_response:
        obj = json.loads(item)
        orders.append({"id": obj["_id"], "name": obj["name"]})

    return orders


def create_order_folders(name):
    """
        Crea una carpeta en una ruta requerida.
    Args:
        name (str): Nombre de la carpeta a eliminar
    Author: 
        wlopera
    """
    FolderUtils.create_folder(PATH_FOLDERS_ORDER, name)
    FolderUtils.create_folder(f"{PATH_FOLDERS_ORDER}/{name}/", NAME_JOBS)
    JsonUtils.write_json(f"{PATH_FOLDERS_ORDER}/{name}/{FILE_PARAM_JSON}", [])


def rename_order_folders(old_name, new_name):
    """
        Renombrar carpeta.
    Args:
        old_value (str): Nombre de la carpeta a modificar
        new_value (str): Nombre nuevo de la carpeta a modificar
    Author: 
        wlopera
    """
    FolderUtils.rename_folder(PATH_FOLDERS_ORDER, old_name, new_name)


def delete_order_folders(name):
    """
        Eliminar carpeta.
    Args:
        name (str): Nombre de la carpeta a eliminar
    Author:
        wlopera
    """
    FolderUtils.delete_folder(f"{PATH_FOLDERS_ORDER}/{name}")


def activate_order(orders, name):
    """
        Recorrer y activar la carpeta actual.
    Args:
        name (str): Nombre de la carpeta a activar
    Author:
        wlopera
    """
    for order in orders:
        if order["name"] == name:
            order["active"] = True
        else:
            order.pop("active", None)
