from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, current_app
from api.schemas import OwnerIn, OwnerOut
from db.models import Owner

blp = Blueprint("owners", "owners", url_prefix="/api/owners", description="Owner endpoints")

@blp.route("/", methods=["POST"])
class OwnerCreate(MethodView):
    def post(self):
        data = request.get_json()
        try:
            owner_in = OwnerIn(**data)
        except Exception as e:
            return {"message": str(e)}, 400
        db_session = current_app.session()
        owner = Owner(name=owner_in.name, email=owner_in.email)
        db_session.add(owner)
        db_session.commit()
        out = OwnerOut(id=owner.id, name=owner.name, email=owner.email)
        db_session.close()
        return out.model_dump(), 201
