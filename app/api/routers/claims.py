from flask_smorest import Blueprint
from flask.views import MethodView
from flask import current_app
from app.api.schemas import ClaimIn, ClaimOut
from app.services.claim_service import create_claim
import structlog

blp = Blueprint("claims", "claims", url_prefix="/api/cars/<int:carId>/claims", description="Claims endpoints")

@blp.route("/", methods=["POST"])
class ClaimCreate(MethodView):
    @blp.arguments(ClaimIn)
    @blp.response(201, lambda: ClaimOut)
    def post(self, claim_in, carId):
        db_session = current_app.session()
        claim, status = create_claim(
            db_session, carId, claim_in.claimDate, claim_in.description, float(claim_in.amount)
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
        # location = f"/api/cars/{carId}/claims/{claim.id}"
        out = ClaimOut.model_validate(claim, from_attributes=True)
        db_session.close()
        return out
