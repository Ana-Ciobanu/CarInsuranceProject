from flask_smorest import Blueprint
from flask.views import MethodView
from flask import current_app
from app.api.schemas import ClaimIn, ClaimOut
from app.services.claim_service import create_claim
import structlog

blp = Blueprint("claims", "claims", url_prefix="/api/cars/<int:carId>/claims", description="Claims endpoints")

@blp.route("/", methods=["POST"])
class ClaimCreate(MethodView):
    def post(self, carId):
        from flask import request
        from pydantic import ValidationError
        db_session = current_app.session()
        try:
            claim_in = ClaimIn.model_validate(request.get_json())
        except ValidationError as e:
            db_session.close()
            return {"message": "Invalid input", "errors": e.errors()}, 400

        claim, status = create_claim(
            db_session, carId, claim_in.claim_date, claim_in.description, float(claim_in.amount)
        )
        if status == 404:
            db_session.close()
            return {"message": "Car not found"}, 404
        if status == 400:
            db_session.close()
            return {"message": "Invalid claim data"}, 400
        structlog.get_logger().info(
            "Claim created",
            claim_id=claim.id,
            car_id=claim.car_id,
            claim_date=str(claim.claim_date),
            amount=claim.amount,
            description=claim.description
        )
        out = ClaimOut.model_validate(claim, from_attributes=True)
        db_session.close()
        return out.model_dump(by_alias=True), 201
