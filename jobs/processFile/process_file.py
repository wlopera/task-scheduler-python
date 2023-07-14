import paramiko
import os

from ..scheduler import Scheduler

class ProcessFile(Scheduler):
    def __init__(self):
        pass  

    def spooler_process(self):
        operation = self.find_field(self, 'operation')
        self.logger.info(f"Operacion: {operation}")
        if operation == "GetList":
            list = self.getListFiles(self)
            self.logger.info(f"Archivos: {list}")
            return True
        elif operation == "Copy":
            self.copyFiles(self)
            return True
            
        return False

    def getClient(self, server, port, user, password):
        # Crear una instancia del cliente SFTP
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conectar al servidor SFTP
        client.connect(server, port, username=user, password=password)

        return client

    def getListFiles(self):
        # Crear una instancia del cliente SFTP
        server = self.find_field(self, 'source_server')
        port = self.find_field(self, 'source_port')
        user = self.find_field(self, 'source_user')
        password = self.find_field(self, 'source_password')
        source_path = self.find_field(self, 'source_path')
        client = self.getClient(self, server, port, user, password)
        
        # Abrir una conexión SFTP
        sftp = client.open_sftp()
        # Cambiar al directorio deseado
        sftp.chdir(source_path)
        # Obtener el listado de archivos y directorios en el directorio remoto
        list = sftp.listdir()
        # Cerrar la conexión SFTP
        sftp.close()
        # Cerrar la conexión SSH
        client.close()
        # Retorna listado de archivos
        return list

    def copyFiles(self):
        # Crear una instancia del cliente SFTP
        source_server = self.find_field(self, 'source_server')
        source_port = self.find_field(self, 'source_port')
        source_user = self.find_field(self, 'source_user')
        source_password = self.find_field(self, 'source_password')
        source_path = self.find_field(self, 'source_path')

        target_server = self.find_field(self, 'target_server')
        target_port = self.find_field(self, 'target_port')
        target_user = self.find_field(self, 'target_user')
        target_password = self.find_field(self, 'target_password')
        target_path = self.find_field(self, 'target_path')

        # Abrir canales SFTP para ambos servidores
        source_client = self.getClient(self,
                                       source_server, source_port, source_user, source_password)
        target_client = self.getClient(self,
                                       target_server, target_port, target_user, target_password)

        # Abrir una conexión SFTP
        source_sftp = source_client.open_sftp()
        target_sftp = target_client.open_sftp()

        # Obtener la lista de archivos en el directorio del servidor A
        list_files = source_sftp.listdir(source_path)

        # Crear el directorio local si no existe
        os.makedirs(target_path, exist_ok=True)

        # Copiar todos los archivos de A a B
        filenames = []

        for file in list_files:
            source_path_file = os.path.join(source_path, file)
            target_path_file = os.path.join(target_path, file)
            source_sftp.get(source_path_file, target_path_file)
            target_sftp.put(target_path_file, target_path_file)

            filenames.append(file)
            self.logger.info(f"Archivo {file} copiado exitosamente.")

        self.order.append({
            "name": "result_filenames",
            "value": ','.join(filenames)
        })

        # Cerrar los canales SFTP
        source_sftp.close()
        target_sftp.close()

        # Cerrar las conexiones SSH
        source_client.close()
        target_client.close()

        self.logger.info("Archivos copiados exitosamente de A a B a través de SFTP.")


# if __name__ == "__main__":
#     try:
#         print("#------------------- ProcessFile")
#         process = ProcessFile()
#         process.get_param()

#         process.spooler_process()
#     except ValueError as error:
#         print("Se produjo un error:", str(error))
