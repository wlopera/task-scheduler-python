from flask import request
from bson import ObjectId
import json

from .template_interface import TemplateInterface


class OrderService(TemplateInterface):

    def get(self):
        reponse = self.collection.find()
        json_response = [json.dumps(item, default=str) for item in reponse]
        orders = []
        for item in json_response:
            obj = json.loads(item)
            orders.append({"id": obj["_id"], "name": obj["name"]})

        return orders

    def add(self, name):
        result = self.collection.insert_one({
            "name": name,
            "chains": [],
            "jobs": []
        })

        orders = self.get()
        # print("Documento creado con el ID:", result.inserted_id, orders)

        self.activate(orders, result.inserted_id)

        # print("ordenes nuevas: ", orders)

        return orders

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
