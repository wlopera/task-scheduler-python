from flask import Blueprint, request

from util.service_utils import ServiceUtils
from util.constants import MONGO_DB_COLLECTION_ORDERS
from services.orders_service import OrderService

orders_routes = Blueprint('orders_routes', __name__, url_prefix='/api/orders')
order_service = None  # Variable estática para almacenar el servicio de órdenes


@orders_routes.record
def initialize_service(state):
    """
        El decorador @orders_routes.record es específico de Flask y se utiliza para registrar una función de configuración 
        que se ejecuta cuando se registra el blueprint orders_routes. 
    """
    global order_service
    # Obtener la instancia de la conexión a MongoDB de la configuración de la aplicación
    mongo_db_connection = state.app.config.get('DATABASE')

    # Creo una instancia d ela clase order_service
    order_service = OrderService(
        mongo_db_connection, MONGO_DB_COLLECTION_ORDERS)


@orders_routes.route('/', methods=['GET'])
def get_orders():
    try:
        orders = order_service.get()
        return ServiceUtils.success({"data": orders})
    except Exception as e:
        return ServiceUtils.error(e)


@orders_routes.route('/add/<string:name>', methods=['POST'])
def add_order(name):
    try:
        orders = order_service.add(name)
        return ServiceUtils.success({"data": orders})
    except Exception as e:
        return ServiceUtils.error(e)


@orders_routes.route('/modify', methods=['POST'])
def modify_order():
    try:
        param = request.get_json()
        old_order = param['old_order']
        new_order = param['new_order']

        orders = order_service.modify(old_order, new_order)

        return ServiceUtils.success({"data": orders})
    except Exception as e:
        return ServiceUtils.error(e)


@orders_routes.route('/delete/<string:id>', methods=['POST'])
def delete_order(id):
    try:
        orders = order_service.delete(id)
        return ServiceUtils.success({"data": orders})
    except Exception as e:
        return ServiceUtils.error(e)
