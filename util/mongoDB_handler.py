import logging
import datetime


class MongoDBHandler(logging.Handler):
    def __init__(self, formatter, scheduler_service, log_name):
        super().__init__()
        self.formatter = formatter
        self.scheduler_service = scheduler_service
        self.log_name = log_name

    def emit(self, record):
        # Permite insertar los registros directamente en la colección "APP_LOGS" de MongoDB
        log_data = {
            "timestamp": datetime.datetime.now(),
            "log_filename": self.log_name,
            "level": record.levelname,
            "message": record.getMessage(),
            "formatted_log": self.formatter.format(record)
        }
        self.scheduler_service.add_log(log_data)
