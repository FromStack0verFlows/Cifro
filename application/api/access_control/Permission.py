from functools import wraps
from flask import request, jsonify
from application.api.model import Accounts
from application.api.access_control import Security


def permission(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'Error': 'a valid token is missing'})

        try:
            identifier = Security.token.decode_token(auth_token=token)
            match = [account for account in Accounts().accounts if account.identifier == identifier][0]
            return function(*args, **kwargs) if match else jsonify({'Authentication': 'Invalid access token'})
        except:
            return jsonify({"Authentication": "Invalid access token"})

    return decorated
