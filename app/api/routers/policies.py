from flask_smorest import Blueprint
from flask.views import MethodView
from flask import current_app
from app.api.schemas import PolicyIn, PolicyOut
from app.services.policy_service import create_policy
from flask import request
from pydantic import ValidationError
import structlog

blp = Blueprint("policies", "policies", url_prefix="/api/cars/<int:carId>/policies", description="Policy endpoints")

@blp.route("/", methods=["POST"])
class PolicyCreate(MethodView):
	def post(self, carId):
		db_session = current_app.session()
		try:
			policy_in = PolicyIn.model_validate(request.get_json())
		except ValidationError as e:
			db_session.close()
			return {"message": "Invalid input", "errors": e.errors()}, 400

		policy, status = create_policy(db_session, carId, policy_in.start_date, policy_in.end_date, policy_in.provider)
		if status == 404:
			db_session.close()
			return {"message": "Car not found"}, 404
		if status == 400:
			db_session.close()
			return {"message": "Invalid policy data"}, 400
		structlog.get_logger().info(
			"Policy created",
			policy_id=policy.id,
			car_id=policy.car_id,
			start_date=str(policy.start_date),
			end_date=str(policy.end_date),
			provider=policy.provider
		)
		out = PolicyOut.model_validate(policy, from_attributes=True)
		db_session.close()
		return out.model_dump(by_alias=True), 201
