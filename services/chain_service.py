from flask import request
from bson import ObjectId
import json

from .template_interface import TemplateInterface


class ChainService(TemplateInterface):

    def get(self, order_id):
        filter = {"_id": ObjectId(order_id)}
        response = self.collection.find(filter)
        json_response = [json.dumps(item, default=str) for item in response]
        chains = []
        for item in json_response:
            obj = json.loads(item)
            for record in obj['chains']:
                chains.append({"id": record["_id"], "name": record["name"], "package": record["package"],
                               "class": record["class"], "next": record["next"], "error": record["error"]})

        return chains

    def add(self, name):
        pass

    def modify(self, order_id, chains):
        session = self.clientMongoDB.start_session()  # Iniciar una sesión transaccional de MongoDB

        try:
            with session.start_transaction():  # Iniciar una transacción
                # Construir el filtro para identificar el documento
                filter = {"_id": ObjectId(order_id)}

                # Iterar sobre cada documento y realizar los cambios
                for chain in chains:
                    # Agregar el campo "_id" utilizando ObjectId
                    chain["_id"] = ObjectId(chain["id"])
                    del chain["id"]  # Eliminar el campo "id"

                # Construir la actualización para eliminar "chains" y agregar nuevos valores
                update_unset = {"$unset": {"chains": ""}}

                # Ejecutar la actualización
                result = self.collection.update_one(filter, update_unset)

                # Verificar si la actualización tuvo éxito
                if result.modified_count == 1:
                    # Construir la actualización para agregar los nuevos valores en "chains" utilizando "$push"
                    update_push = {"$push": {"chains": {"$each": chains}}}

                    # Ejecutar la segunda actualización para agregar los nuevos valores en "chains"
                    result = self.collection.update_one(filter, update_push)

                    # Número de documentos modificados
                    # print("Resultado: ", result.modified_count)

                chains = self.get(order_id)
                # self.activate(jobs, new_item['id'])
                return chains
        except Exception as e:
            session.abort_transaction()  # Abortar la transacción en caso de error
            raise e
        finally:
            session.end_session()  # Finalizar la sesión

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
