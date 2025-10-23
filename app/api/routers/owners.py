from flask_smorest import Blueprint
from flask.views import MethodView
from flask import current_app
from app.api.schemas import OwnerIn, OwnerOut
from app.db.models import Owner

blp = Blueprint("owners", "owners", url_prefix="/api/owners", description="Owner endpoints")

@blp.route("/", methods=["POST"])
class OwnerCreate(MethodView):
    @blp.arguments(OwnerIn)
    @blp.response(201, lambda: OwnerOut)
    def post(self, owner_in):
        db_session = current_app.session()
        owner = Owner(name=owner_in.name, email=owner_in.email)
        db_session.add(owner)
        db_session.commit()
        out = OwnerOut.model_validate(owner, from_attributes=True)
        db_session.close()
        return out
