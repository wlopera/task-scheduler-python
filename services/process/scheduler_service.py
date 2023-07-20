from bson import ObjectId
import json


class SchedulerService():
    """
        Este modulo permite tener servicios MongoDB para uso del TaskScheduler en general.
    """

    def __init__(self, mongo_db_connection, COLLECTION_NAME, clientMongoDB):
        self.mongo_db_connection = mongo_db_connection
        self.clientMongoDB = clientMongoDB
        self.collection = mongo_db_connection[COLLECTION_NAME]

    def get_order(self, order_id):
        filter = {"_id": ObjectId(order_id)}
        result = self.collection.find(filter)
        json_response = [json.dumps(item, default=str) for item in result]
        order = json.loads(json_response[0])
        print("Orden actual", order)
        return order
