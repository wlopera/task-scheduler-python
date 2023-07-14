import logging
from util.constants import PATH_LOG


def setup_logger(log_name, log_file):
    # Configurar el logger
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)

    try:
        # Crear el archivo de registro
        file_handler = logging.FileHandler(
            f"{PATH_LOG}/{log_file}.log")

        file_handler.setLevel(logging.DEBUG)

        # Formateador del registro
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Agregar el manejador de archivo al logger
        logger.addHandler(file_handler)

        return logger

    except Exception as e:
        print(f"Error al configurar el archivo de registro: {str(e)}")
