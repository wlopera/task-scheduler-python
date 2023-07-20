from bson import ObjectId
import json


class SchedulerService():
    """
        Este modulo permite tener servicios MongoDB para uso del TaskScheduler en general.
    """

    def __init__(self, mongo_db_connection, COLLECTION_ORDERS, COLLECTION_HISTORICAL, clientMongoDB):
        self.mongo_db_connection = mongo_db_connection
        self.clientMongoDB = clientMongoDB
        self.collection_order = mongo_db_connection[COLLECTION_ORDERS]
        self.collection_historical = mongo_db_connection[COLLECTION_HISTORICAL]

    def get_order(self, order_id):
        filter = {"_id": ObjectId(order_id)}
        result = self.collection_order.find(filter)
        json_response = [json.dumps(item, default=str) for item in result]
        order = json.loads(json_response[0])
        return order

    def get_historical(self):
        result = self.collection_historical.find()
        json_response = [json.dumps(item, default=str) for item in result]
        print(11111, json_response)
        data = [json.loads(json_str) for json_str in json_response]
        print(2222, data)
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

    def delete_all_historical(self, id):
        self.collection_historical.delete_many({})
        return True
