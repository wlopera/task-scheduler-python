from flask import request
from bson import ObjectId
import json

from .template_interface import TemplateInterface


class JobService(TemplateInterface):

    def get(self, order_id):
        print(2222, order_id)
        filter = {"_id": ObjectId(order_id)}
        reponse = self.collection.find(filter)
        json_response = [json.dumps(item, default=str) for item in reponse]
        print("JOBS:", json_response)
        jobs = []
        for item in json_response['jobs']:
            obj = json.loads(item)
            jobs.append({"id": obj["_id"], "name": obj["name"]})

            # obj = json.loads(item)['jobs']
            # print(3333, obj)
            # if(len(obj) > 0):
            #     jobs.append(obj[0])

        return jobs

    def add(self, name, order_id):

        # -----  NUEVO JOB

        # Filtra el documento con la orden "id":
        filter = {"_id": ObjectId(order_id)}

        # Define el nuevo objeto "job"
        new_job = {
            "_id": ObjectId(),
            "name": name,
            "params": []
        }

        # Agrega el nuevo objeto "job" al arreglo "jobs"
        update = {"$push": {"jobs": new_job}}

        # Actualiza el documento en la base de datos
        self.collection.update_one(filter, update)
        print("Creando tarea: ")

        # -----  NUEVO CHAIN

        # Define el nuevo objeto "chain"
        new_chain = {
            "_id":ObjectId(),
            "name": name,
            "package": "",
            "class": "",
            "next": "success",
            "error": "error"
        }

        # Agrega el nuevo objeto "job" al arreglo "jobs"
        update = {"$push": {"chains": new_chain}}

        # Actualiza el documento en la base de datos
        self.collection.update_one(filter, update)
        print("Creando chain: ")

        # print("ordenes nuevas: ", orders)

        return self.get(order_id)

    def modify(self, old_item, new_item):

        # Definir los criterios de búsqueda para encontrar los documentos a actualizar
        filtro = {"_id": ObjectId(old_item['id'])}

        # Actualizar el valor en la tabla utilizando el método update_one()
        result = self.collection.update_one(
            filtro, {"$set": {"name": new_item['name']}})

        if result.modified_count:
            print("Documento modificado exitosamente.")
        else:
            print("No se encontró el documento con el ID:", old_item['id'])

        orders = self.get()

        # print("Documento modificado:", old_item['id'],  orders)

        self.activate(orders, old_item['id'])

        # print("ordenes modificadfas: ", orders)

        return orders

    def delete(self, item_id):
        result = self.collection.delete_one({'_id': ObjectId(item_id)})

        # if result.deleted_count > 0:
        #     print("Documento eliminado exitosamente.")
        # else:
        #     print("No se encontró el documento con el ID:", item_id)

        orders = self.get()

        return orders
