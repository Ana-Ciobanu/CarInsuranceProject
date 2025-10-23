from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from app.db.session import get_session
from app.api.schemas import OwnerIn, OwnerOut
from app.db.models import Owner
from pydantic import ValidationError

blp = Blueprint("owners", "owners", url_prefix="/api/owners", description="Owner endpoints")

@blp.route("/", methods=["POST"])
class OwnerCreate(MethodView):
    def post(self):
        
        try:
            owner_in = OwnerIn.model_validate(request.get_json())
        except ValidationError as e:
            return {"message": "Invalid input", "errors": e.errors()}, 400

        with get_session() as db_session:
            owner = Owner(name=owner_in.name, email=owner_in.email)
            db_session.add(owner)
            db_session.commit()
            out = OwnerOut.model_validate(owner, from_attributes=True)
            return out.model_dump(by_alias=True), 201
