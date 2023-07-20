import logging
from util.constants import PATH_LOG
from util.mongoDB_handler import MongoDBHandler


def setup_logger(log_name, scheduler_service):

    try:
        # Configurar el logger
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)

        # Crear el archivo de registro
        # file_handler = logging.FileHandler(
        #     f"{PATH_LOG}/{log_file}.log")
        # file_handler.setLevel(logging.DEBUG)

        # Formateador del registro
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Para uso de archivos LOG
        # file_handler.setFormatter(formatter)
        # # Agregar el manejador de archivo al logger
        # logger.addHandler(file_handler)

        # Para uso de Collection en MongoDB
        handler = MongoDBHandler(formatter, scheduler_service, log_name)
        logger.addHandler(handler)

        return logger

    except Exception as e:
        print(f"Error al configurar el archivo de registro: {str(e)}")
