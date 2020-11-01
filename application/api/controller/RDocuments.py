from flask import jsonify, request
from flask_restful import Resource
from application.api.access_control.Permission import permission
from application.model.GlobalApplicationModel import GlobalApplicationModel


class RDocuments(Resource):

    @permission
    def get(self):
        model = GlobalApplicationModel()
        if category := request.args.get('type', default=None, type=str):
            if match := [doc for doc in model.documents if doc.class_id == category]:
                return jsonify({'type': category, 'Documents': [x.json() for x in match]})
            else:
                return jsonify({'type': category, 'Documents': None})
        else:
            return jsonify({'documents': [x.json() for x in model.documents]})

    @permission
    def post(self):
        pass
