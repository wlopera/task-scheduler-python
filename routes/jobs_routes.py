from flask import Blueprint, request
from util.folder_utils import FolderUtils
from util.json_utils import JsonUtils
from util.service_utils import ServiceUtils
from util.constants import PATH_FOLDERS_ORDER, FILE_PARAM_JSON, NAME_JOBS

jobs_routes = Blueprint('jobs_routes', __name__, url_prefix='/api/jobs')


@jobs_routes.route('/<string:name>', methods=['POST'])
def jobs(name):
    try:
        jobs = []
        if name:
            jobs = get_jobs(name)
        return ServiceUtils.success({"data": jobs})
    except Exception as e:
        return ServiceUtils.error(e)


@jobs_routes.route('/fromJson/<string:name>', methods=['POST'])
def jobs_from_json(name):
    try:
        jobs = []
        if name:
            jobs = get_jobs_from_json(name)
        return ServiceUtils.success({"data": jobs})
    except Exception as e:
        return ServiceUtils.error(e)


@jobs_routes.route('/add', methods=['POST'])
def add_job():
    try:
        param = request.get_json()
        order_id = param['order_id']
        job_id = param['job_id']

        create_job_folders(order_id, job_id)
        add_job_to_order(order_id, job_id)

        jobs = get_jobs(order_id)

        activate_job(jobs, job_id)

        return ServiceUtils.success({"data": jobs})
    except Exception as e:
        return ServiceUtils.error(e)


@jobs_routes.route('/modify', methods=['POST'])
def modify_job():
    try:
        param = request.get_json()
        order_id = param['order_id']
        old_job = param['old_value']
        new_job = param['new_value']

        rename_job_folders(order_id, old_job, new_job)
        update_job_in_order(order_id, old_job, new_job)

        jobs = get_jobs(order_id)
        activate_job(jobs, new_job)

        return ServiceUtils.success({"data": jobs})
    except Exception as e:
        return ServiceUtils.error(e)


@jobs_routes.route('/delete', methods=['POST'])
def delete_job():
    try:
        param = request.get_json()
        order_id = param['order_id']
        job_id = param['job_id']

        delete_job_folders(order_id, job_id)
        remove_job_from_order(order_id, job_id)

        jobs = get_jobs(order_id)

        return ServiceUtils.success({"data": jobs})
    except Exception as e:
        return ServiceUtils.error(e)


def get_jobs(order_id):
    response = FolderUtils.get_folders(
        f"{PATH_FOLDERS_ORDER}/{order_id}/{NAME_JOBS}")

    jobs = [{"id": index, "name": value}
            for index, value in enumerate(response)]

    return jobs


def get_jobs_from_json(order_id):
    response = JsonUtils.read_json(
        f"{PATH_FOLDERS_ORDER}/{order_id}/{FILE_PARAM_JSON}")

    jobs = [{"id": index, "name": data['name']}
            for index, data in enumerate(response)]

    return jobs


def create_job_folders(order_id, job_id):
    FolderUtils.create_folder(
        PATH_FOLDERS_ORDER + "/" + order_id + "/"+NAME_JOBS+"/", job_id)

    JsonUtils.write_json(
        f"{PATH_FOLDERS_ORDER}/{order_id}/{NAME_JOBS}/{job_id}/{FILE_PARAM_JSON}", {"params": []})


def update_job_in_order(order_id, old_job, new_job):
    JsonUtils.update_item(
        f"{PATH_FOLDERS_ORDER}/{order_id}/{FILE_PARAM_JSON}", 'name', old_job, new_job)


def rename_job_folders(order_id, old_job, new_job):
    FolderUtils.rename_folder(
        f"{PATH_FOLDERS_ORDER}/{order_id}/{NAME_JOBS}", old_job, new_job)
    JsonUtils.update_item(
        f"{PATH_FOLDERS_ORDER}/{order_id}/{FILE_PARAM_JSON}", 'name', old_job, new_job)


def delete_job_folders(order_id, job_id):
    FolderUtils.delete_folder(
        f"{PATH_FOLDERS_ORDER}/{order_id}/{NAME_JOBS}/{job_id}")


def add_job_to_order(order_id, job_id):
    values = {
        "name": job_id,
        "package": "",
        "class": "",
        "next": "success",
        "error": "error"
    }
    JsonUtils.add_item(
        f"{PATH_FOLDERS_ORDER}/{order_id}/{FILE_PARAM_JSON}", values)


def remove_job_from_order(order_id, job_id):
    JsonUtils.remove_item_by_identifier(
        f"{PATH_FOLDERS_ORDER}/{order_id}/{FILE_PARAM_JSON}", 'name', job_id)


def activate_job(jobs, job_id):
    for job in jobs:
        if job["name"] == job_id:
            job["active"] = True
        else:
            job.pop("active", None)
