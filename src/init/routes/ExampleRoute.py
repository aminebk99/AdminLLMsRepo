from init.controllers import ExampleController
from flask import request
from flask import Blueprint

example_route = Blueprint('example_route', __name__)


@example_route.route('/example', methods=['GET', 'POST'])
def example():
    if request.method == 'GET':
        return ExampleController.get_all()
    elif request.method == 'POST':
        return ExampleController.create(request.json)

