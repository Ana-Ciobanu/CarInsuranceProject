from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, current_app
from api.schemas import PolicyIn, PolicyOut
from services.policy_service import create_policy

blp = Blueprint("policies", "policies", url_prefix="/api/cars/<int:carId>/policies", description="Policy endpoints")

@blp.route("/", methods=["POST"])
class PolicyCreate(MethodView):
	def post(self, carId):
		data = request.get_json()
		try:
			policy_in = PolicyIn(**data)
		except Exception as e:
			return {"message": str(e)}, 400
		db_session = current_app.session()
		policy, status = create_policy(db_session, carId, policy_in.startDate, policy_in.endDate, policy_in.provider)
		if status == 404:
			db_session.close()
			return {"message": "Car not found"}, 404
		if status == 400:
			db_session.close()
			return {"message": "Invalid policy data"}, 400
		out = PolicyOut(
			id=policy.id,
			carId=policy.car_id,
			startDate=policy.start_date,
			endDate=policy.end_date,
			provider=policy.provider
		)
		db_session.close()
		return out.model_dump(by_alias=True), 201
