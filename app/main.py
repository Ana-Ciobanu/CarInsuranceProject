from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from app.core.logging import setup_logging
from app.core.scheduling import start_scheduler
from app.core.config import settings
from app.db.base import db
from app.api.schemas import CarIn, CarOut, PolicyIn, PolicyOut, OwnerIn, OwnerOut,ClaimIn, ClaimOut
from app.db.session import SessionLocal, engine

from app.api.routers.health import blp as HealthBlueprint
from app.api.routers.cars import blp as CarsBlueprint
from app.api.routers.policies import blp as PoliciesBlueprint
from app.api.routers.claims import blp as ClaimsBlueprint
from app.api.routers.history import blp as HistoryBlueprint
from app.api.routers.validity import blp as ValidityBlueprint
from app.api.routers.owners import blp as OwnersBlueprint


def create_app():

    setup_logging()

    app = Flask(__name__)
    app.config.update(
        PROPAGATE_EXCEPTIONS=True,
        API_TITLE=settings.API_TITLE,
        API_VERSION=settings.API_VERSION,
        OPENAPI_VERSION=settings.OPENAPI_VERSION,
        OPENAPI_URL_PREFIX=settings.OPENAPI_URL_PREFIX,
        OPENAPI_SWAGGER_UI_PATH=settings.OPENAPI_SWAGGER_UI_PATH,
        OPENAPI_SWAGGER_UI_URL=settings.OPENAPI_SWAGGER_UI_URL,
        SQLALCHEMY_DATABASE_URI=settings.DATABASE_URL,
        SQLALCHEMY_TRACK_MODIFICATIONS=settings.SQLALCHEMY_TRACK_MODIFICATIONS,
    )

    db.init_app(app)
    Migrate(app, db)
    app.session = SessionLocal
    app.engine = engine


    api = Api(app)
    api.register_blueprint(HealthBlueprint)
    api.register_blueprint(CarsBlueprint)
    api.register_blueprint(PoliciesBlueprint)
    api.register_blueprint(ClaimsBlueprint)
    api.register_blueprint(HistoryBlueprint)
    api.register_blueprint(ValidityBlueprint)
    app.register_blueprint(OwnersBlueprint)

    if settings.SCHEDULER_ENABLED:
        with app.app_context():
            start_scheduler()

    for schema in [CarIn, CarOut, PolicyIn, PolicyOut, OwnerIn, OwnerOut, ClaimIn, ClaimOut]:
        api.spec.components.schema(schema.__name__, schema.model_json_schema())

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
