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
        # Iniciar una sesión transaccional de MongoDB
        session = self.clientMongoDB.start_session()
        print(111, order_id, session)
        try:
            print(111222, order_id, session)
            
            with session.start_transaction():  # Iniciar una transacción

                # -----  NUEVO JOB
                print(2222, order_id)

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

                print(3333, order_id)
                # Agrega el nuevo objeto "job" al arreglo "jobs"
                update = {"$push": {"chains": new_chain}}

                # Actualiza el documento en la base de datos
                self.collection.update_one(filter, update)

                jobs = self.get(order_id)
                self.activate(jobs, item_id[0])
                return jobs
        except Exception as e:
            print(444444)
            session.abort_transaction()  # Abortar la transacción en caso de error
            raise e
        finally:
            print(55555)
            session.end_session()  # Finalizar la sesión

    def modify(self, order_id, old_item, new_item):
        # Iniciar una sesión transaccional de MongoDB
        session = self.clientMongoDB.start_session()

        try:
            with session.start_transaction():  # Iniciar una transacción

                old_name = old_item['name']
                new_name = new_item['name']

                # Construir el filtro y la actualización
                filter = {"_id": ObjectId(order_id)}

                # -----  Modificar JOB
                update = {
                    "$set": {
                        "jobs.$[job].name": new_name
                    }
                }
                array_filters = [{'job._id': ObjectId(new_item['id'])}]

                # Ejecutar la actualización
                self.collection.update_one(
                    filter, update, array_filters=array_filters)

                # Actualizar el campo "next" en las cadenas
                filter1 = {"_id": ObjectId(order_id), "chains.next": old_name}
                update1 = {"$set": {"chains.$[elem].next": new_name}}
                array_filters1 = [{"elem.next": old_name}]
                self.collection.update_many(
                    filter1, update1, array_filters=array_filters1)

                # Actualizar el campo "name" en las cadenas
                filter2 = {"_id": ObjectId(order_id), "chains.name": old_name}
                update2 = {"$set": {"chains.$[elem].name": new_name}}
                array_filters2 = [{"elem.name": old_name}]
                self.collection.update_many(
                    filter2, update2, array_filters=array_filters2)

                jobs = self.get(order_id)
                self.activate(jobs, new_item['id'])
                return jobs
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

    def get_chains(self, order_id):
        filter = {"_id": ObjectId(order_id)}
        result = self.collection.find(filter)
        json_response = [json.dumps(item, default=str) for item in result]

        data = json.loads(json_response[0])

        chains = [{"id": index, "name": item['name']}
                  for index, item in enumerate(data['chains'])]

        return chains
