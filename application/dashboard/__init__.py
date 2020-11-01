from flask import Blueprint
from application.dashboard.view import index, dashboard

index_page = Blueprint('index', __name__)
dashboard_page = Blueprint('dashboard', __name__, template_folder="templates")

index_page.add_url_rule('/', view_func=index)
dashboard_page.add_url_rule('/dashboard', view_func=dashboard)

