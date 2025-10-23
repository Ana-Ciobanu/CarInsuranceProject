from flask_smorest import Blueprint
from flask.views import MethodView
from flask import current_app, request
from app.api.schemas import OwnerIn, OwnerOut
from app.db.models import Owner
from pydantic import ValidationError

blp = Blueprint("owners", "owners", url_prefix="/api/owners", description="Owner endpoints")

@blp.route("/", methods=["POST"])
class OwnerCreate(MethodView):
    def post(self):
        db_session = current_app.session()
        try:
            owner_in = OwnerIn.model_validate(request.get_json())
        except ValidationError as e:
            db_session.close()
            return {"message": "Invalid input", "errors": e.errors()}, 400

        owner = Owner(name=owner_in.name, email=owner_in.email)
        db_session.add(owner)
        db_session.commit()
        out = OwnerOut.model_validate(owner, from_attributes=True)
        db_session.close()
        return out.model_dump(by_alias=True), 201
