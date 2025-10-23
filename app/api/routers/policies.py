from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from app.db.session import get_session
from app.api.schemas import PolicyIn, PolicyOut
from app.services.policy_service import create_policy

blp = Blueprint("policies", "policies", url_prefix="/api/cars/<int:carId>/policies", description="Policy endpoints")

@blp.route("/", methods=["POST"])
class PolicyCreate(MethodView):
	def post(self, carId):
		data = request.get_json()
		try:
			policy_in = PolicyIn(**data)
		except Exception as e:
			return {"message": str(e)}, 400
		
		with get_session() as db_session:
			policy, status = create_policy(db_session, carId, policy_in.startDate, policy_in.endDate, policy_in.provider)
			if status == 404:
				return {"message": "Car not found"}, 404
			if status == 400:
				return {"message": "Invalid policy data"}, 400
			out = PolicyOut(
				id=policy.id,
				carId=policy.car_id,
				startDate=policy.start_date,
				endDate=policy.end_date,
				provider=policy.provider
			)
			return out.model_dump(by_alias=True), 201