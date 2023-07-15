"""
    El módulo abc es el módulo de la biblioteca estándar de Python que proporciona soporte
    para la creación de clases abstractas.
"""
from abc import ABC, abstractmethod


class TemplateInterface(ABC):
    """
        Plantilla para crear CRUD con MongoDB
    """

    def __init__(self, mongo_db_connection, COLLECTION_NAME):
        self.mongo_db_connection = mongo_db_connection
        self.collection = mongo_db_connection[COLLECTION_NAME]

    @abstractmethod
    def get():
        """
            Consultar todos los items de la base de datos.
        Author: 
            wlopera
        Return:
            dict: Carpetas de una ruta
        """
        pass

    @abstractmethod
    def add(self, name):
        """
           Agregar item de lqa base de datos.       
        Author:
            wlopera
        Return:
                dict: Resultado del procesamiento
        """
        pass

    @abstractmethod
    def modify(self, old_item, new_item):
        """
            Modificar nombre del item en base de datos.
        Args:
            old_item (str): Nombre del item a modificar
            new_item (str): Nombre del nuevo item
        Author:
            wlopera
        Return:
                dict: Resultado del procesamiento
        """
        pass

    @abstractmethod
    def delete(self, item_id):
        """
            Eliminar item de base de datos.
        Args:
            item_id (str): Identificador de la carpeta a eliminar.
        Author:
            wlopera
        Return:
                dict: Resultado del procesamiento
        """
        pass

    def activate(self, items, item_id):
        """
            Recorrer y activa el item actual.
        Args:
            items(str): Lista de registros en la tabla
            item_id (str): Identificador del campo a seleccionar como activo
        Author:
            wlopera
        """
        for item in items:
            if str(item['id']) == str(item_id):
                item["active"] = True
            else:
                item.pop("active", None)
                
        return items
