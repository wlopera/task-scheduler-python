# archivo mongodb_connection.py

import pymongo


class ConnectionHandler:

    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client[database]

    def close(self):
        print("Cerrando MongoDB...")
        self.client.close()