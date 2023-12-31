import sys
import importlib
from util.logger import setup_logger
from datetime import datetime
import time

class SpoolerTask:

    def __init__(self, scheduler_service):
        self.scheduler_service = scheduler_service
        self.current_order = {}
        self.jobs = {}
        self.current_job = None
        self.log_name = "Scheduler-" + datetime.now().strftime('%Y%m%d%H%M%S')
        self.logger = setup_logger(self.log_name, scheduler_service)
        self.logger.info(
            "#----------------------- Inicia proceso de Scheduler")
        scheduler_service

    def get_order(self, order_id):
        self.current_order = self.scheduler_service.get_order(order_id)
        self.current_chains = self.current_order['chains']
        self.current_job = self.current_chains[0]['name']

    def get_job(self, name):
        for job in self.current_chains:
            if job['name'] == name:
                return job
        return None

    def get_params(self, current_job):
        for job in self.current_order['jobs']:
            if job['_id'] == current_job['_id']:
                return job['params']
        return None

    def process(self):
        self.logger.info("detener................")
        time.sleep(20)
        self.logger.info("continuar................")
        # Iniciar el procesamiento de tareas
        for iterator in range(len(self.current_chains)):
            self.process_job(self.get_job(self.current_job))
        self.logger.info("Scheduler finalizado con exito")

    def process_job(self, job):
        package_job = "jobs." + job['package']
        class_job = job['class']

        # print("--------------------------------------------")
        # print("Package:" + package_job)
        # print("Class:" + class_job)

        try:
            module = importlib.import_module(package_job)
            self.logger.info(f"Modulo: {module}")
            instance = getattr(module, class_job)
            self.logger.info(f"Instancia: {instance}")
            instance.order = []
            instance.logger = self.logger

            # Actualizar parametros de la orden con los de la tarea
            params = self.get_params(job)
            # print("job:", job)
            # print("params:", params)

            instance.update_param(instance, params)
            result = instance.spooler_process(instance)
            self.logger.info(f"Resultado: {result}")
            if result == False:
                print("Error salida del app")
                self.logger.error(f"Error salida del app: {self.current_job}")                
                raise Exception("Error salida del app: ", self.current_job)
                # sys.exit()
            else:
                print("Proceso exitoso...!")
                self.logger.info(f"Proceso exitoso: {self.current_job}")
                self.current_job = job['next']
                print("")
        except ImportError as err:
            print(f"Error: {err}")
            self.logger.error(f"Error: {err}")
            print("")
            raise (err)


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
    spooler.logger.info("JOBS ==> " + str(spooler.current_chains))
    spooler.logger.info("Tarea inicial ==> " + spooler.current_job)

    spooler.process()
