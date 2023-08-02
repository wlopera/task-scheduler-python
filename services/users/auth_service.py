import json

from ..template_interface import TemplateInterface


class AuthService():
    """
        Este modulo permite tener servicios MongoDB para uso de usuarios en general.
    """

    def __init__(self, mongo_db_connection, COLLECTION_USERS, clientMongoDB):
        self.mongo_db_connection = mongo_db_connection
        self.clientMongoDB = clientMongoDB
        self.collection = mongo_db_connection[COLLECTION_USERS]

    def login(self, user_name):
        filter = {"name": user_name}
        response = self.collection.find(filter)
        json_response = [json.dumps(item, default=str) for item in response]
        if len(json_response) > 0:
            return json.loads(json_response[0])
        else:
            return json_response

