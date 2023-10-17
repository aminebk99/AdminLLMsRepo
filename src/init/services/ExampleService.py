from init.models import Example
from init.database import db
from flask import jsonify


class ExampleService:
    @staticmethod
    def get_all():
        return jsonify([e.to_dict() for e in Example.query.all()])
    


    @staticmethod
    def get_by_id(id):
        return jsonify(Example.query.get(id).to_dict())
    

    @staticmethod
    def create(data):
        example = Example(example=data['example'], text=data['text'])
        db.session.add(example)
        db.session.commit()
        return jsonify(example.to_dict())

    

    @staticmethod
    def update(id, data):
        example = Example.query.get(id)
        example.example = data['example']
        example.text = data['text']
        db.session.commit()
        return jsonify(example.to_dict())
    

    @staticmethod

    def delete(id):
        example = Example.query.get(id)
        db.session.delete(example)
        db.session.commit()
        return jsonify(example.to_dict())