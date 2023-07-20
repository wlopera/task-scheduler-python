from bson import ObjectId
import json


class SchedulerService():
    """
        Este modulo permite tener servicios MongoDB para uso del TaskScheduler en general.
    """

    def __init__(self, mongo_db_connection, COLLECTION_ORDERS, COLLECTION_HISTORICAL, COLLECTION_LOGS, clientMongoDB):
        self.mongo_db_connection = mongo_db_connection
        self.clientMongoDB = clientMongoDB
        self.collection_order = mongo_db_connection[COLLECTION_ORDERS]
        self.collection_historical = mongo_db_connection[COLLECTION_HISTORICAL]
        self.collection_logs = mongo_db_connection[COLLECTION_LOGS]

    def get_order(self, order_id):
        filter = {"_id": ObjectId(order_id)}
        result = self.collection_order.find(filter)
        json_response = [json.dumps(item, default=str) for item in result]
        order = json.loads(json_response[0])
        return order

    def get_historical(self):
        result = self.collection_historical.find()
        json_response = [json.dumps(item, default=str) for item in result]
        data = [json.loads(json_str) for json_str in json_response]
        return data

    def add_historical(self, data):
        result = self.collection_historical.insert_one(data)
        return result.inserted_id

    def update_historical(self, data):
        # Definir los criterios de búsqueda para encontrar los documentos a actualizar
        filter = {"id": ObjectId(data['id'])}
        # Actualizar el valor en la tabla
        self.collection_historical.update_one(filter, {"$set": data})
        return True

    def delete_all_historical(self):
        self.collection_historical.delete_many({})
        return True

    def get_logs(self, log_name):
        filter = {"log_filename": log_name}

        cursor = self.collection_logs.find(filter)

        # Extraer el campo "formatted_log" de los documentos coincidentes
        formatted_logs = [item["formatted_log"] for item in cursor]

        # Crear un nuevo objeto JSON con solo los valores de "formatted_log"
        resultado_json = json.dumps(formatted_logs)

        return resultado_json

    def add_log(self, log_data):
        self.collection_logs.insert_one(log_data)

    def delete_all_logs(self):
        self.collection_logs.delete_many({})
        return True
