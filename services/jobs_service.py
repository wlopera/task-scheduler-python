from flask import request
from bson import ObjectId
import json

from .template_interface import TemplateInterface


class JobService(TemplateInterface):

    def get(self, order_id):
        filter = {"_id": ObjectId(order_id)}
        reponse = self.collection.find(filter)
        json_response = [json.dumps(item, default=str) for item in reponse]
        jobs = []
        for item in json_response:
            obj = json.loads(item)
            for record in obj['jobs']:
                jobs.append({"id": record["_id"], "name": record["name"]})

        return jobs

    def add(self, name, order_id):

        # -----  NUEVO JOB

        # Filtra el documento con la orden "id":
        filter = {"_id": ObjectId(order_id)}
        item_id = ObjectId(),

       # Define el nuevo objeto "job"
        new_job = {
            "_id": item_id[0],
            "name": name,
            "params": []
        }

        # Agrega el nuevo objeto "job" al arreglo "jobs"
        update = {"$push": {"jobs": new_job}}

        # Actualiza el documento en la base de datos
        self.collection.update_one(filter, update)

        # -----  NUEVO CHAIN

        # Define el nuevo objeto "chain"
        new_chain = {
            "_id": item_id[0],
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

        jobs = self.get(order_id)
        self.activate(jobs, item_id[0])
        return jobs

    def modify(self, order_id, new_item):
       # Construir el filtro y la actualización
        filter = {"_id": ObjectId(order_id)}
        
        # -----  Modificar JOB
        update = {
            "$set": {
                "jobs.$[job].name": new_item['name']
            }
        }
        array_filters = [{'job._id': ObjectId(new_item['id'])}]

        # Ejecutar la actualización
        self.collection.update_one(filter, update, array_filters=array_filters)

        jobs = self.get(order_id)
        self.activate(jobs, new_item['id'])
        return jobs

    def delete(self, order_id, item_id):

        # Construir el filtro y la actualización
        filter = {'_id': ObjectId(order_id)}
        
        # -----  Borrar JOB
        update = {"$pull": {"jobs": {"_id": ObjectId(item_id)}}}

        # Ejecutar la actualización
        self.collection.update_one(filter, update)

        # -----  Borrar Chain
        update = {"$pull": {"chains": {"_id": ObjectId(item_id)}}}

        # Ejecutar la actualización
        self.collection.update_one(filter, update)

        return self.get(order_id)
