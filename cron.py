import schedule
import time
import subprocess

running = True


def init_order():
    global running
    running = False

    # Lógica para copiar archivos de A a B
    subprocess.run(
        ['python', 'JobScheduler\spooler_task.py', "JobSchduler\\chains\\batch_files"])

    print("Detener cron")
    return schedule.CancelJob


print("#------------------- Cron")
# Programar la tarea para que se ejecute todos los días a las HH:MM:SS
schedule.every().day.at('12:32:30').do(init_order)

while running:
    schedule.run_pending()
    time.sleep(1)

print("Cron Finalizado")


# from flask import Flask
# import subprocess

# app = Flask(__name__)

# @app.route('/invoke_script', methods=['GET'])
# def invoke_script():
#     subprocess.run(['python', 'JobScheduler/spooler_task.py', 'JobSchduler/chains/batch_files'])
#     return "Script invoked successfully"

# if __name__ == '__main__':
#     app.run()