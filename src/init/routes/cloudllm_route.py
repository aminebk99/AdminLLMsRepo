from flask import request
from flask import Blueprint
from init.controllers import CloudLLMController
from ..middleware.auth_middleware import token_required


cloudllm_route = Blueprint('cloudllm_route', __name__)

@cloudllm_route.route('/cloudllm', methods=['GET'])
@token_required
def cloudllm():
    if request.method == 'GET':
        return CloudLLMController.getAllCloudLLMs()

@cloudllm_route.route('/cloudllm/<cloudllm_id>', methods=['GET', 'DELETE', 'PUT'])
def cloudllm_id(cloudllm_id):
    if request.method == 'GET':
        return CloudLLMController.getCloudLLM(cloudllm_id)
    elif request.method == 'DELETE':
        return CloudLLMController.deleteCloudLLM(cloudllm_id)
    elif request.method == 'PUT':
        return CloudLLMController.changeCloudLLMStatus(cloudllm_id, request.json['status'])