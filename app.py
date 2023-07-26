from flask import Flask
from flask_cors import CORS
import os

from routes.orders_routes import orders_routes
from routes.jobs_routes import jobs_routes
from routes.chains_routes import chains_routes

from mongoDB.connection_handler import ConnectionHandler
from util.constants import MONGO_DB_URI, MONGO_DB_PORT, MONGO_DB_NAME

app = Flask(__name__)
app.secret_key = "wlopera"

# Manejador de conexión a MongoDB
# handler = ConnectionHandler(MONGO_DB_URI, MONGO_DB_PORT, MONGO_DB_NAME)
mongo_uri = os.environ.get("MONGO_DB_URI", MONGO_DB_URI)
mongo_port = int(os.environ.get("MONGO_DB_PORT", MONGO_DB_PORT))
mongo_name = os.environ.get("MONGO_DB_NAME", MONGO_DB_NAME)
print(1111, mongo_uri)
print(2222, mongo_port)
print(3333, mongo_name)

handler = ConnectionHandler(mongo_uri, mongo_port, mongo_name)

# Configurar la conexión en la aplicación Flask
"""    
    app.config es un diccionario en el que puedes almacenar cualquier configuración adicional que desees para tu aplicación Flask.
    
    Al asignar la instancia de la conexión a la configuración de la aplicación, puedes acceder a ella en otras partes de tu aplicación
    utilizando app.config['DATABASE'] para obtener la conexión a MongoDB.
"""
app.config['CLIENT'] = handler.client
app.config['DATABASE'] = handler.db

# Rutas
app.register_blueprint(orders_routes)
app.register_blueprint(jobs_routes)
app.register_blueprint(chains_routes)


@app.route('/api/', methods=['GET'])
def test():
    """
        Consultar los directorios de la carpeta requerida..
    Author:
        wlopera
    Return:
            dict: Carpetas de una ruta
    """
    return {"data": "Json de prueba", "code": 200}


CORS(app)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
