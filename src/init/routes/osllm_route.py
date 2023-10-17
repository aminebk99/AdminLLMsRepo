# init/routes/osllm_route.py

from flask import Blueprint, request, jsonify
from init.controllers.osllm_controller import OSLLMController

osllm_blueprint = Blueprint('osllm', __name__)
osllm_controller = OSLLMController()

@osllm_blueprint.route('/osllm/<osllm_id>', methods=['GET'])
def get_osllm(osllm_id):
    osllm = osllm_controller.get_osllm(osllm_id)
    if osllm:
        return jsonify(osllm.__dict__), 200
    return "OSLLM not found", 404

@osllm_blueprint.route('/osllm/<osllm_id>', methods=['DELETE'])
def delete_osllm(osllm_id):
    success = osllm_controller.delete_osllm(osllm_id)
    if success:
        return "OSLLM deleted", 200
    return "OSLLM not found", 404

@osllm_blueprint.route('/osllm/<osllm_id>', methods=['PUT'])
def change_osllm_status(osllm_id):
    data = request.get_json()
    if 'status' in data:
        status = data['status']
        success = osllm_controller.change_osllm_status(osllm_id, status)
        if success:
            return "OSLLM status changed", 200
    return "Invalid request", 400
