from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
import atexit

from routes.orders_routes import orders_routes
from routes.jobs_routes import jobs_routes
from routes.chains_routes import chains_routes

from util.constants import MONGO_DB_URI, MONGO_DB_PORT, MONGO_DB_NAME
import traceback

try:
    app = Flask(__name__)
    app.secret_key = "wlopera"

    # Manejador de conexión a MongoDB
    mongo_uri = os.environ.get("MONGO_DB_URI", MONGO_DB_URI)
    mongo_port = int(os.environ.get("MONGO_DB_PORT", MONGO_DB_PORT))
    mongo_name = os.environ.get("MONGO_DB_NAME", MONGO_DB_NAME)

    client = MongoClient(mongo_uri, mongo_port)
    db = client[mongo_name]
    # handler.init()

    # Configurar la conexión en la aplicación Flask
    """    
        app.config es un diccionario en el que puedes almacenar cualquier configuración adicional que desees para tu aplicación Flask.
        
        Al asignar la instancia de la conexión a la configuración de la aplicación, puedes acceder a ella en otras partes de tu aplicación
        utilizando app.config['DATABASE'] para obtener la conexión a MongoDB.
    """
    app.config['CLIENT'] = client
    app.config['DATABASE'] = db

    # # Rutas
    app.register_blueprint(orders_routes)
    app.register_blueprint(jobs_routes)
    app.register_blueprint(chains_routes)

    @app.route('/api/', methods=['GET'])
    def test1():
        """
            Consultar los directorios de la carpeta requerida..
        Author:
            wlopera
        Return:
                dict: Carpetas de una ruta
        """
        mongo = f"data: {mongo_uri} - {mongo_port}  - {mongo_name}"
        return {"data": "Json de prueba 2", "code": 200, "mongo": mongo}


    # Función para cerrar la conexión a MongoDB al finalizar la aplicación Flask
    def close_mongo_connection():
        client.close()

    # Registrar la función para ser llamada al finalizar la aplicación
    atexit.register(close_mongo_connection)

    CORS(app)

    if __name__ == '__main__':
        app.run(debug=True, port=5000)

except ConnectionFailure as e:
    print(f"Error de conexión a MongoDB: {e}")
    trace = traceback.format_exc()
    print(f"Error.........................: {trace}")

except RuntimeError as e:
    print(f"Error en tiempo de ejecución: {e}")
    trace = traceback.format_exc()
    print(f"Error.........................: {trace}")
