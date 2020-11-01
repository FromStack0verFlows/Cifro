from flask import jsonify
from flask_restful import Resource
from application.api.access_control.Permission import permission
from application.model.GlobalApplicationModel import GlobalApplicationModel


class RDocumentByID(Resource):

    @permission
    def get(self, id):
        model = GlobalApplicationModel()
        if byID := [doc for doc in model.documents if int(id) == int(doc.id)]:
            return jsonify({'document': byID[0].json()})
        else:
            return jsonify({'document': None})