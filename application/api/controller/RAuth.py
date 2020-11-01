from flask_restful import Resource
from flask import jsonify, request
from application.api.access_control import Security
from application.api.model import Accounts


class RAuth(Resource):
    def post(self):
        try:
            auth = request.authorization
            accounts = Accounts().accounts
            if not auth or not auth.username or not auth.password:
                return 401

            if usr := [account for account in accounts if account.firstname == auth.username][0]:
                if Security.verify_hash(user=usr, auth_pass=auth.password):
                    return jsonify({"Access token": Security.token.encode_token(usr.identifier).decode("utf-8")})
            else:
                return 401
        except: pass