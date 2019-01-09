from flask import Blueprint

main = Blueprint('main',__name__)

from . import views ,errors
from ..models import Permission

def create_app(config_name):
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
