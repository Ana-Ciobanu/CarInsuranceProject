from flask_smorest import Blueprint
from flask.views import MethodView
from app.db.session import get_session
from app.services.history_service import get_car_history

blp = Blueprint("history", "history", url_prefix="/api/cars/<int:carId>/history", description="History endpoints")

@blp.route("/")
class CarHistory(MethodView):
    def get(self, carId):
        with get_session() as db_session:
            history, status = get_car_history(db_session, carId)
            if status == 404:
                return {"message": "Car not found"}, 404
            return history, 200
