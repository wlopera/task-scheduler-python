import json
class Scheduler:

    def __init__(self, order):
        self.order = order
        self.logger=None
        
    def update_param(self, params):
        for item in params:
            filter = [objeto for objeto in self.order if objeto["name"] == item['name']]
            if len(filter) > 0:                
                for objeto in filter:
                    objeto["value"] = item['value']
            else:
                self.order.append(item)

    def find_field(self, field):
        response = next((item['value'] for item in self.order if item['name'] == field), None)
        return response