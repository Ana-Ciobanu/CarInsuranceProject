from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, current_app
from api.schemas import InsuranceValidityOut
from datetime import date
from services.validity_service import check_insurance_validity

blp = Blueprint("validity", "validity", url_prefix="/api/cars/<int:carId>/insurance-valid", description="Insurance validity endpoints")

@blp.route("/")
class InsuranceValid(MethodView):
    def get(self, carId):
        d = request.args.get("date")
        if not d:
            return {"message": "Missing date parameter"}, 400
        try:
            d_parsed = date.fromisoformat(d)
        except Exception:
            return {"message": "Invalid date format, expected YYYY-MM-DD"}, 400
        # Validate date range
        if not (date(1900,1,1) <= d_parsed <= date(2100,12,31)):
            return {"message": "Date out of allowed range (1900-2100)"}, 400
        db_session = current_app.session()
        valid, status = check_insurance_validity(db_session, carId, d_parsed)
        db_session.close()
        if status == 404:
            return {"message": "Car not found"}, 404
        resp = InsuranceValidityOut(carId=carId, date=d_parsed, valid=valid)
        return resp.model_dump(by_alias=True), 200
