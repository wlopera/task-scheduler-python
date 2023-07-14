from flask import Flask
from flask_cors import CORS

from routes.orders_routes import orders_routes
from routes.jobs_routes import jobs_routes
from routes.chains_routes import chains_routes

from mongoDB.connection_handler import ConnectionHandler
from util.constants import MONGO_DB_URI, MONGO_DB_PORT, MONGO_DB_NAME

app = Flask(__name__)
app.secret_key = "wlopera"

# Rutas
app.register_blueprint(orders_routes)
app.register_blueprint(jobs_routes)
app.register_blueprint(chains_routes)
CORS(app)

# Manejador de conexión a MongoDB 
handler = ConnectionHandler(MONGO_DB_URI, MONGO_DB_PORT, MONGO_DB_NAME)

# Pasar la conexión a los routes
orders_routes.mongo_db_connection = handler.db
# jobs_routes.mongo_db_connection = mongo_db_connection
# chains_routes.mongo_db_connection = mongo_db_connection

if __name__ == '__main__':
    app.run(debug=True, port=5000)
