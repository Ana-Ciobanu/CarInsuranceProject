from flask_smorest import Blueprint
from flask.views import MethodView

blp = Blueprint("health", "health", url_prefix="/health", description="Health check endpoint")

@blp.route("/")
class HealthCheck(MethodView):
	def get(self):
		return {"status": "ok"}, 200
