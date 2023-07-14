import os
import shutil


class FolderUtils:

    @staticmethod
    def get_folders(path):
        """
            Lee los directorios de la carpeta requerida.
        Args:
            path (str): Ruta de la carpetas
        Author: 
            wlopera
        Return:
            dict: Carpetas de una ruta
        """
        if os.path.exists(path) and os.path.isdir(path):
            folders = [name for name in os.listdir(
                path) if os.path.isdir(os.path.join(path, name))]
            return folders
        else:
            return []

    @staticmethod
    def delete_folder(path):
        """
            Elimina la carpeta y su contenido.
        Args:
            path (str): Ruta de la carpeta
        Author: 
            wlopera      
        """
        shutil.rmtree(path)

    @staticmethod
    def create_folder(path, folder_name):
        """
            Crea una nueva carpeta en la ruta especificada.
        Args:
            path (str): Ruta de la carpeta
        Author: 
            wlopera
        Return:
            dict: Carpeta de una ruta
        """
        new_folder = os.path.join(path, folder_name)
        os.mkdir(new_folder)
        return new_folder

    @staticmethod
    def rename_folder(path, old_folder_name, new_folder_name):
        """
            Renombra una carpeta en la ruta especificada.
        Args:
            path (str): Ruta de la carpeta
            old_folder_name (str): Nombre de carpeta actual 
            new_folder_name (str): Nuevo Nombre de carpeta 
        Author: 
            wlopera
        Return:
            dict: Carpetas de una ruta
        """
        old_folder = os.path.join(path, old_folder_name)
        new_folder = os.path.join(path, new_folder_name)
        os.rename(old_folder, new_folder)
        return new_folder
   