from flask import Flask
from flask_cors import CORS

from routes.orders_routes import orders_routes
from routes.jobs_routes import jobs_routes
from routes.chains_routes import chains_routes

from mongoDB.connection_handler import ConnectionHandler
from util.constants import MONGO_DB_URI, MONGO_DB_PORT, MONGO_DB_NAME

app = Flask(__name__)
app.secret_key = "wlopera"

# Manejador de conexión a MongoDB
handler = ConnectionHandler(MONGO_DB_URI, MONGO_DB_PORT, MONGO_DB_NAME)

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
CORS(app)


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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
