from flask_smorest import Blueprint
from flask.views import MethodView
from flask import current_app
from services.history_service import get_car_history

blp = Blueprint("history", "history", url_prefix="/api/cars/<int:carId>/history", description="History endpoints")

@blp.route("/")
class CarHistory(MethodView):
    def get(self, carId):
        db_session = current_app.session()
        history, status = get_car_history(db_session, carId)
        db_session.close()
        if status == 404:
            return {"message": "Car not found"}, 404
        return history, 200
