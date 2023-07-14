from datetime import datetime


class ChainsHelper:

    @staticmethod
    def getDataBase(param):
        return {
            "name": param['name'],
            "package": param['package'],
            "class": param['class'],
            "next": param['next'],
            "error": param['error']
        }

    @staticmethod
    def create_record(name, node, log):
        return {
            "id": datetime.now().strftime('%Y%m%d%H%M%S'),
            "order_id": name,
            "status": "iniciado",
            "startDate": datetime.now().strftime('%d/%m/%Y-%H:%M:%S'),
            "endDate": "",
            "duration": "",
            "node": node,
            "log": log
        }

    def update_record(data, status, node):
        endDate = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')

        startDate_time = datetime.strptime(
            data['startDate'], "%d/%m/%Y-%H:%M:%S")
        endDate_time = datetime.strptime(endDate, "%d/%m/%Y-%H:%M:%S")

        diff = endDate_time - startDate_time

        return {
            "id": data['id'],
            "order_id": data['order_id'],
            "status": status,
            "startDate": data['startDate'],
            "endDate": endDate,
            "duration": str(diff.total_seconds()) + " seg",
            "node": node,
            "log": data['log']
        }
