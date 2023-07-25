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
        # Iniciar una sesión transaccional de MongoDB
        session = self.clientMongoDB.start_session()

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

    def get_params(self, order_id, job_id):

        # Consulta el documento que contiene el orden y el job específicos
        filter = {"_id":  ObjectId(order_id)}
        pipeline = [
            {"$match": filter},
            {"$unwind": "$jobs"},
            {"$match": {"jobs._id": ObjectId(job_id)}},
            {"$project": {"jobs._id": 1, "jobs.name": 1, "jobs.params": 1}}
        ]

        cursor = self.collection.aggregate(pipeline)

        # Obtener los documentos como diccionarios directamente sin convertirlos a JSON
        records = [document for document in cursor]

        if records:
            # Puedes acceder a los campos de los documentos directamente como diccionarios
            record = records[0]
            result = {
                "id": str(record["_id"]),
                "jobs": {
                    "id": str(record["jobs"]["_id"]),
                    "name": record["jobs"]["name"],
                    "params": record["jobs"]["params"]
                }
            }
            return result
        else:
            print("No se encontró el registro con los _ids especificados.")
            return []

    def update_params(self, order_id, job_id, params):
        # Iniciar una sesión transaccional de MongoDB
        session = self.clientMongoDB.start_session()

        try:
            with session.start_transaction():  # Iniciar una transacción

                # Construir el filtro para encontrar la orden y el trabajo específicos
                filter = {'_id': ObjectId(
                    order_id), 'jobs._id': ObjectId(job_id)}

                # Verificar que el job_id corresponde al trabajo dentro de la orden
                job_exists = self.collection.count_documents(filter) > 0
                if not job_exists:
                    print(
                        "El job_id proporcionado no corresponde a ningún trabajo en la orden.")
                    return

                # Borrar parámetros del trabajo
                update = {"$pull": {"jobs.$.params": {}}}
                self.collection.update_one(filter, update)

                # Agregar nuevos parámetros al trabajo
                # Aquí asumimos que params es una lista de parámetros que deseas agregar
                # Puedes ajustar este código según la estructura de tus datos.
                if params:
                    update = {"$push": {"jobs.$.params": {"$each": params}}}
                    self.collection.update_one(filter, update)

                print("Actualización de parámetros completada con éxito.")

                return self.get_params(order_id, job_id)
        except Exception as e:
            session.abort_transaction()  # Abortar la transacción en caso de error
            raise e
        finally:
            session.end_session()  # Finalizar la sesión
