import json

class JsonUtils:
    @staticmethod
    def write_json(path, new_data):
        """
            Escribe los datos proporcionados en formato JSON en un archivo.
        Args:
            path (str): Ruta del archivo JSON
            new_data (dict): Nuevos datos a escribir en formato JSON
        Author: 
            wlopera
        """
        with open(path, 'w') as json_file:
            json.dump(new_data, json_file, indent=4)

    @staticmethod
    def read_json(path):
        """
            Lee los datos en formato JSON desde un archivo.
        Args:
            path (str): Ruta del archivo JSON
        Author: 
            wlopera
        Return:
            dict: Contenido del archivo de registro
        """
        with open(path, 'r') as file:
            rep = json.load(file)
            return rep

    @staticmethod
    def read_log_file(path):
        """
            Lee el contenido de un archivo log.
        Args:
            path (str): Ruta del archivo de registro
        Author: 
            wlopera
        Return:
            dict: Contenido del archivo log.
        """
        with open(path + ".log", 'r') as file:
            content = file.read().splitlines()
            return {'log': content}

    @staticmethod
    def add_item(path, item, position=None):
        """
            Agrega un elemento al archivo JSON.
        Args:
            path (str): Ruta del archivo JSON.
            item (dict): Trabajo a agregar en formato JSON
            position (int, optional): Posición en la que se desea insertar el trabajo. Si no se proporciona,
                se agrega al final de la lista existente
        Author: 
            wlopera
        """
        data = JsonUtils.read_json(path)
        if data is not None:
            if position is not None and position <= len(data):
                data.insert(position, item)
            else:
                data.append(item)
            JsonUtils.write_json(path, data)

    @staticmethod
    def update_item(path, identifier_field, identifier_value, new_data):
        """
            Modifica elemento en el archivo JSON basado en un campo identificador y su valor.
        Args:
            path (str): Ruta del archivo JSON.
            identifier_field (str): Nombre del campo identificador
            identifier_value: Valor del campo identificador para buscar el elemento a modificar
            new_data (dict): Nuevos datos para el elemento en formato JSON
        Author: 
            wlopera
        """
        data = JsonUtils.read_json(path)
        if data is not None:
            for item in data:
                if item.get(identifier_field) == identifier_value:
                    item.update(new_data)
                    break
            JsonUtils.write_json(path, data)

    @staticmethod
    def remove_item_by_position(path, position):
        """
            Elimina un elemento del archivo JSON basado en su posición en la lista.
        Args:
            path (str): Ruta del archivo JSON
            position (int): Posición del elemento a eliminar
        Author: 
            wlopera            
        """
        data = JsonUtils.read_json(path)
        if data is not None and position < len(data):
            del data[position]
            JsonUtils.write_json(path, data)

    @staticmethod
    def remove_item_by_identifier(path, identifier_field, identifier_value,):
        """
            Eliminar elemento en el archivo JSON basado en un campo identificador y su valor.
        Args:
            path (str): Ruta del archivo JSON
            identifier_field (str): Nombre del campo identificador
            identifier_value: Valor del campo identificador para buscar el elemento a eliminar
        Author: 
            wlopera
        """
        data = JsonUtils.read_json(path)
        if data is not None:
            data = [item for item in data if item.get(
                identifier_field) != identifier_value]
            JsonUtils.write_json(path, data)
