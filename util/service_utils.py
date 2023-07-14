from flask import jsonify
import traceback


class ServiceUtils:

    @staticmethod
    def success(response):
        response['code'] = 200
        response['status'] = 'SUCCESS'
        response['error'] = None
        response['message'] = "Operación exitosa"
        return jsonify(response)

    @staticmethod
    def error(err):
        response = {
            "code": 400,
            "message": "Error en servicio",
            "error": str(err),
            "status": "ERROR"
        }
        trace = traceback.format_exc()
        print(f"Error.........................: {str(err)}\n{trace}")
        return jsonify(response)
