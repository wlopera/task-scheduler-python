# task-scheduler-python
Procesamiento de ordenes a través de tareas encadenadas - backend PYTHON - MongoDB 

- ver Frontend: https://github.com/wlopera/task_scheduler_react

***
----------------------------------------------------------------------
Backend: Python
----------------------------------------------------------------------
Crear proyceto y agregar librerias requeridas
----------------------------------------------------------------------

----------------------------------------------------------------------
Backend: Python - Flask
----------------------------------------------------------------------
> pip install Flask
> pip install schedule

> pip install flask-cors

app.py:
    from flask_cors import CORS
    ...
    
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    # CORS(app, resources={r"/api/*": {"origins": "*"}}) # Mas generico

----------------------------------------------------------------------

----------------------------------------------------------------------
Estructura caroetas y archivos
----------------------------------------------------------------------
Carpetas:
--------
    backend:
      doc: import.txt
      helpers
      jobs
      routes
      services
      util

ARchivos proyecto:
-----------------
app.py
cron.py
spooler_task.py

Archivos configuración:
----------------------
.gitignore
requirements.txt
vercel.json

----------------------------------------------------------------------
Subir a vercel
----------------------------------------------------------------------
- Crear archivo requirements.txt, con dependencias:
        Flask==2.3.2
        Flask-Cors==3.0.10
        paramiko==3.2.0
        pymongo==4.4.1
        schedule==1.2.0
  Nota:  $>  pip freeze > requirements.txt

- Instalar vercel si no esta instalado:
  $> npm install -g vercel

- vercel init o
- Cerar archivo vercel.json 
  {
    "version": 2,
    "builds": [
      {
        "src": "app.py",
        "use": "@vercel/python"
      }
    ],
    "routes": [
      {
        "src": "/(.*)",
        "dest": "/app.py"
      }
    ],
    "env": {
      "MONGO_DB_URI": "mongodb+srv://admin:admin@cluster0.fcz7lpr.mongodb.net/?retryWrites=true&w=majority",
      "MONGO_DB_PORT": "27017",
      "MONGO_DB_NAME":"scheduler"
    }
  }

  Nota: Esto configura Vercel para usar el runtime de Python y ejecutar app.py 
  como tu archivo principal de Flask.

  - Arrancar proceso vercel:
   D:\WorkSpace\WS_REACT_PRANICAL\JobScheduler\backend>vercel
    Vercel CLI 31.0.2
    ? Set up and deploy “D:\WorkSpace\WS_REACT_PRANICAL\JobScheduler\backend”? [Y/n] y
    ? Which scope do you want to deploy to? wlopera
    ? Link to existing project? [y/N] n
    ? What’s your project’s name? backend
    ? In which directory is your code located? ./
    Production: https://backend-one-nu.vercel.app [19s]
    Deployed to production. Run `vercel --prod` to overwrite later (https://vercel.link/2F).
    To change the domain or build command, go to https://vercel.com/wlopera/backend/settings


 Nota: https://vercel.com/wlopera/backend/7bNjVt7PnywhGhJs5MYBmHoSAfd8
       - Para ver detalles

      https://backend-tau-pied.vercel.app 
       - Para probarlo

       https://backend-one-nu.vercel.app/_logs
       - Para ver errores de compilación

para actualizar proceso vercel:

  $ vercel --prod
  Vercel CLI 31.0.2
  Retrieving project…
  Deploying wlopera/backend
  Uploading [--------------------] (0.0B/4.3KB)
  Uploading [====================] (4.3KB/4.3KB)
  Inspect: https://vercel.com/wlopera/backend/5B6iQTGM3NU5k3Nre7hx5b1DQrGu [3s]
  https://backend-nlvaf44wx-wlopera.vercel.appQueued
  Building
  Completing
  Production: https://backend-one-nu.vercel.app [24s]
  Due to `builds` existing in your configuration file, the Build and Development Settings defined in your Project Settings will not apply. Learn More: https://vercel.link/unused-build-settings

***
