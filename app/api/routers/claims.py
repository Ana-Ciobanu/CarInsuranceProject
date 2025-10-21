from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, current_app
from api.schemas import ClaimIn, ClaimOut
from services.claim_service import create_claim

blp = Blueprint("claims", "claims", url_prefix="/api/cars/<int:carId>/claims", description="Claims endpoints")

@blp.route("/", methods=["POST"])
class ClaimCreate(MethodView):
	def post(self, carId):
		data = request.get_json()
		try:
			claim_in = ClaimIn(**data)
		except Exception as e:
			return {"message": str(e)}, 400
		db_session = current_app.session()
		claim, status = create_claim(db_session, carId, claim_in.claimDate, claim_in.description, float(claim_in.amount))
		if status == 404:
			db_session.close()
			return {"message": "Car not found"}, 404
		if status == 400:
			db_session.close()
			return {"message": "Invalid claim data"}, 400
		location = f"/api/cars/{carId}/claims/{claim.id}"
		out = ClaimOut(
			id=claim.id,
			carId=claim.car_id,
			claimDate=claim.claim_date,
			description=claim.description,
			amount=claim.amount
		)
		db_session.close()
		return out.model_dump(by_alias=True), 201, {"Location": location}
