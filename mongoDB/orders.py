# archivo crud.py

from connection_handler import ConnectionHandler

handler = ConnectionHandler("localhost", 27017, "orders", "jobs")
handler.start()

# Obtener la coleccion
collection = handler.collection

# Crea un nuevo documento
documento = {"nombre": "Juan Pérez", "edad": 30}

# Inserta el documento en la colección
collection.insert_one(documento)

# Encuentra todos los documentos en la colección
documentos = collection.find()

# Imprime todos los documentos
for documento in documentos:
    print(documento)

# Actualiza un documento
documento = collection.find_one({"nombre": "Juan Pérez"})
documento["edad"] = 31
collection.update_one(documento, {"$set": documento})

# Borra un documento
documento = collection.find_one({"nombre": "Juan Pérez"})
collection.delete_one(documento)

# Do some work

handler.close()
