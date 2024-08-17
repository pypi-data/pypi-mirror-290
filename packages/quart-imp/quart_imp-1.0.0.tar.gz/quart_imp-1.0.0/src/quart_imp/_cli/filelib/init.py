def init_full_py(app_name: str, secret_key: str) -> str:
    return f"""\
from quart import Quart

from {app_name}.extensions import imp


def create_app():
    app = Quart(__name__, static_url_path="/")

    QuartConfig(
        secret_key="{secret_key}",
        app_instance=app
    )

    imp.init_app(app, ImpConfig(
        init_session={{"logged_in": False}},
    ))

    imp.import_app_resources()
    imp.import_blueprints("blueprints")
    imp.import_models("models")

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
"""


def init_slim_py(app_name: str, secret_key: str) -> str:
    return f"""\
from quart import Quart

from {app_name}.extensions import imp
from quart_imp.config import ImpConfig, QuartConfig


def create_app():
    app = Quart(__name__, static_url_path="/")

    QuartConfig(
        secret_key="{secret_key}",
        app_instance=app
    )

    imp.init_app(app, ImpConfig())
    imp.import_app_resources()
    imp.import_blueprint("www")

    return app
"""


def init_minimal_py(secret_key: str) -> str:
    return f"""\
from quart import Quart

from quart_imp import Imp
from quart_imp.config import ImpConfig, QuartConfig


def create_app():
    app = Quart(__name__, static_url_path="/")

    QuartConfig(
        secret_key="{secret_key}",
        app_instance=app
    )

    imp = Imp(app, ImpConfig())
    imp.import_app_resources()

    return app
"""
