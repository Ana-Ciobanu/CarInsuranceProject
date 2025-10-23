from flask_smorest import Blueprint
from flask.views import MethodView
from flask import current_app, request
from app.api.schemas import CarOut, CarIn, OwnerOut
from app.db.repositories import CarRepo
from app.db.models import Car, Owner
from pydantic import ValidationError

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
	
	def post(self):
		data = request.get_json()
		try:
			car_in = CarIn(**data)
		except Exception as e:
			return {"message": str(e)}, 400
		db_session = current_app.session()
		owner = db_session.get(Owner, car_in.ownerId)
		if not owner:
			db_session.close()
			return {"message": "Owner not found"}, 404
		car = Car(
			vin=car_in.vin,
			make=car_in.make,
			model=car_in.model,
			year_of_manufacture=car_in.yearOfManufacture,
			owner_id=car_in.ownerId
		)
		db_session.add(car)
		db_session.commit()
		out = CarOut(
			id=car.id,
			vin=car.vin,
			make=car.make,
			model=car.model,
			yearOfManufacture=car.year_of_manufacture,
			owner=OwnerOut(id=owner.id, name=owner.name, email=owner.email)
		)
		db_session.close()
		return out.model_dump(by_alias=True), 201

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