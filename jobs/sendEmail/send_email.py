import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from ..scheduler import Scheduler

class SendEmail(Scheduler):
    def __init__(self):
        pass

    def spooler_process(self):
        self.logger.info("Enviar correo")

        to_mail = self.find_field(self, 'to_mail')
        subject = self.find_field(self, 'subject')
        message = self.find_field(self, 'message')
        self.send_email(self, to_mail, subject, message)

        return True

    def send_email(self, to_mail, subject, message):
        # Configuración del servidor SMTP y las credenciales - Puerto SMTP de Gmail (TLS): 587
        smtp_server = self.find_field(self, 'smtp_server')
        port = self.find_field(self, 'port')
        from_email = self.find_field(self, 'from_email')
        password = self.find_field(self, 'password')
        self.logger.info(f"send email: {smtp_server}")

        # Crear el objeto MIME para el mensaje
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_mail
        msg['Subject'] = subject

        # Agregar el cuerpo del mensaje
        body = MIMEText(message, 'plain')
        msg.attach(body)

        try:
            # Conexión al servidor SMTP - Puerto SMTP de Gmail (SSL): 465
            # with smtplib.SMTP_SSL(smtp_server, 465) as smtp_server:
            #     smtp_server.login(from_email, password)
            #     smtp_server.sendmail(from_email, to_mail, msg.as_string())

            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(from_email, password)

            # # # Envío del correo electrónico
            server.sendmail(from_email, to_mail, msg.as_string())
            self.logger.info("Correo enviado correctamente")

        except Exception as e:
            self.logger.error(f"Error al enviar el correo: {str(e)}")
            server.close

        finally:
            # Cerrar la conexión con el servidor SMTP
            self.logger.info("Finalizo el envio")
            # server.quit()

# if __name__ == "__main__":
#     email=SendEmail()
#     email.order=[]
#     print(email.order)
#     email.update_param("processBatchPython\\chain\\job\\email\\param.json")
#     email.spooler_process()
