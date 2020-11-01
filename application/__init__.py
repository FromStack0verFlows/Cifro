from application.api import controller
from application.config import Config
from application.dashboard import dashboard_page, index_page
from flask import Flask
from flask_restful import Api

app = Flask(__name__)

service = Api(app)

app.config.from_object(Config)

""" REST API Service Resources"""
service.add_resource(controller.RAuth, '/api/auth')
service.add_resource(controller.RDocuments, '/api/documents')
service.add_resource(controller.RDocumentByID, '/api/documents/<string:id>')

""" WEB-Application Resources"""
app.register_blueprint(dashboard_page)
app.register_blueprint(index_page)
