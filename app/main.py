from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from db.session import SessionLocal, engine
from dotenv import load_dotenv
import os

from api.routers.health import blp as HealthBlueprint
from api.routers.cars import blp as CarsBlueprint
from api.routers.policies import blp as PoliciesBlueprint
from api.routers.claims import blp as ClaimsBlueprint
from api.routers.history import blp as HistoryBlueprint
from api.routers.validity import blp as ValidityBlueprint
from api.routers.owners import blp as owners_blp
from db.base import db
from core.logging import setup_logging
from core.scheduling import start_scheduler

def get_db_session():
    return SessionLocal()


def create_app(db_url=None):
    setup_logging()
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Car Insurance Project"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3" #Standard for API documentation
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    from db.models import Car, Owner, InsurancePolicy, Claim
    app.session = SessionLocal
    app.engine = engine

    api = Api(app)
    api.register_blueprint(HealthBlueprint)
    api.register_blueprint(CarsBlueprint)
    api.register_blueprint(PoliciesBlueprint)
    api.register_blueprint(ClaimsBlueprint)
    api.register_blueprint(HistoryBlueprint)
    api.register_blueprint(ValidityBlueprint)
    app.register_blueprint(owners_blp)

    if os.getenv("SCHEDULER_ENABLED", "True") == "True":
        start_scheduler()

    return app