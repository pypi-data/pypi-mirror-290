def api_blueprint_init_py(url_prefix: str, name: str) -> str:
    return f"""\
from quart_imp import ImpBlueprint
from quart_imp.config import ImpBlueprintConfig

bp = ImpBlueprint(__name__, ImpBlueprintConfig(
    enabled=True,
    url_prefix="/{url_prefix}",
    init_session={{"{name}_session_loaded": True}},
))

bp.import_resources("routes")
"""


def api_blueprint_routes_index_py() -> str:
    return """\
from .. import bp


@bp.route("/", methods=["GET"])
async def index():
    return await {"message": "Hello, World!"}
"""
