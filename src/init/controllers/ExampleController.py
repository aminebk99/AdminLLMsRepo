from init.services import ExampleService


class ExampleController:
    @staticmethod
    def get_all():
        return ExampleService.get_all()

    @staticmethod
    def get_by_id(id):
        return ExampleService.get_by_id(id)

    @staticmethod
    def create(data):
        return ExampleService.create(data)

    @staticmethod
    def update(id, data):
        return ExampleService.update(id, data)

    @staticmethod
    def delete(id):
        return ExampleService.delete(id)