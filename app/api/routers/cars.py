from flask_smorest import Blueprint
from flask.views import MethodView
from flask import current_app
from app.api.schemas import CarOut, CarIn
from app.db.repositories import CarRepo
from app.db.models import Car, Owner

blp = Blueprint("cars", "cars", url_prefix="/api/cars", description="Car endpoints")

@blp.route("/")
class CarsList(MethodView):
	def get(self):
		db_session = current_app.session()
		repo = CarRepo(db_session)
		cars = repo.list_with_owner()
		result = [CarOut.model_validate(c, from_attributes=True).model_dump(by_alias=True) for c in cars]
		db_session.close()
		return result, 200

	@blp.arguments(CarIn)
	@blp.response(201, lambda: CarOut)
	def post(self, car_in):
		db_session = current_app.session()
		owner = db_session.get(Owner, car_in.ownerId)
		if not owner:
			db_session.close()
			return {"message": "Owner not found"}, 404
		car = Car(**car_in.model_dump(by_alias=False))
		db_session.add(car)
		db_session.commit()
		out = CarOut.model_validate(car, from_attributes=True)
		db_session.close()
		return out

@blp.route("/<int:carId>", methods=["DELETE"])
class CarDelete(MethodView):
	def delete(self, carId):
		db_session = current_app.session()
		car = db_session.get(Car, carId)
		if not car:
			db_session.close()
			return {"message": "Car not found"}, 404
		db_session.delete(car)
		db_session.commit()
		db_session.close()
		return {"message": f"Car {carId} and related claims/policies deleted."}, 200
