import logging
from util.constants import PATH_LOG


def setup_logger_mongoDB(log_name, log_file):
    try:

        # Crear un objeto logger personalizado
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)

        # Definir un formato personalizado para los registros
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Configurar un manejador StreamHandler con el formato personalizado
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    except Exception as e:
        print(f"Error al configurar el archivo de registro: {str(e)}")
