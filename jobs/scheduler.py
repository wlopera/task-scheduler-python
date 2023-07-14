import json
class Scheduler:

    def __init__(self, order):
        self.order = order
        self.logger=None
        
    def update_param(self, path_param):
        param={}
        #self.logger.info('Mensaje desde Scheduler')
        # Abrir el archivo JSON en modo lectura
        with open(path_param + "/param.json", 'r') as file:
            # Cargar el contenido del archivo JSON
            param = json.load(file)
        
        for item in param['params']:
            filter = [objeto for objeto in self.order if objeto["name"] == item['name']]
            if len(filter) > 0:                
                for objeto in filter:
                    objeto["value"] = item['value']
            else:
                self.order.append(item)

    def find_field(self, field):
        response = next((item['value'] for item in self.order if item['name'] == field), None)
        return response