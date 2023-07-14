import sys
import importlib
from util.logger import setup_logger
from datetime import datetime
from util.json_utils import JsonUtils
from util.constants import PATH_FOLDERS_ORDER, FILE_PARAM_JSON
import time


class SpoolerTask:

    def __init__(self):
        self.current_order = {}
        self.jobs = {}
        self.current_job = None
        # self.logger = setup_logger("scheduler", "Scheduler-" + datetime.now().strftime('%Y%m%d%H%M%S'))
        # self.log_name = "Scheduler-" + datetime.now().strftime('%Y%m%d')
        self.log_name = "Scheduler-" + datetime.now().strftime('%Y%m%d%H%M%S')
        self.logger = setup_logger("scheduler", self.log_name)
        self.logger.info(
            "#----------------------- Inicia proceso de Scheduler")

    def get_chains(self, order_id):
        self.current_order = order_id
        # Consultas las tareas a procesar
         
        self.jobs = JsonUtils.read_json(f"{PATH_FOLDERS_ORDER}/{order_id}/{FILE_PARAM_JSON}")
        self.current_job = self.jobs[0]['name']

    def get_job(self, name):
        for job in self.jobs:
            if job['name'] == name:
                return job
        return None

    def process(self):
        self.logger.info("detener................")
        time.sleep(20)
        self.logger.info("continuar................")
        # Iniciar el procesamiento de tareas
        for iterator in range(len(self.jobs)):
            self.process_job(self.get_job(self.current_job))
        self.logger.info("Scheduler finalizado con exito")

    def process_job(self, job):
        package_job = "jobs." + job['package']
        class_job = job['class']
        path_param = "JobScheduler/backend/orders/" + \
            self.current_order + "/jobs/" + self.current_job

        # print("--------------------------------------------")
        print("Package:" + package_job)
        print("Class:" + class_job)
        print("path_param:" + str(path_param))

        try:
            module = importlib.import_module(package_job)
            self.logger.info(f"Modulo: {module}")
            instance = getattr(module, class_job)
            self.logger.info(f"Instancia: {instance}")
            instance.order = []
            instance.logger = self.logger

            # Actualizar parametros de la orden con los de la tarea
            instance.update_param(instance, path_param)           
            result = instance.spooler_process(instance)
            self.logger.info(f"Resultado: {result}")
            if result == False:
                print("Error salida del app")
                self.logger.error("Error salida del app: ", self.current_job)
                raise Exception("Error salida del app: ", self.current_job)
                #sys.exit()
            else:                
                print("Proceso exitoso...!")
                self.logger.info("Proceso exitoso: ", self.current_job)
                self.current_job = job['next']
                print("")
        except ImportError as err:
            print(f"Error: {err}")
            self.logger.error(f"Error: {err}")
            print("")
            raise(err) 

if __name__ == "__main__":
    spooler = SpoolerTask()

    args = sys.argv
    print(12345, args)

    if (len(args) > 1):
        spooler.get_chains(args[1])
    else:
        # print("Debe ingregar un archivo de parametros de entrada")
        # spooler.logger.error("Debe ingregar un archivo de parametros de entrada")
        # sys.exit()
        spooler.get_chains("batch_files")

    # spooler.logger.info("ORDER ==> " + str(spooler.order))
    spooler.logger.info("JOBS ==> " + str(spooler.jobs))
    spooler.logger.info("Tarea inicial ==> " + spooler.current_job)

    spooler.process()
