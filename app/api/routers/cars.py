from flask_smorest import Blueprint
from flask.views import MethodView
from flask import current_app, request
from api.schemas import CarOut, OwnerOut, CarIn
from db.repositories import CarRepo
from db.models import Car, Owner

blp = Blueprint("cars", "cars", url_prefix="/api/cars", description="Car endpoints")

@blp.route("/")
class CarsList(MethodView):
	def get(self):
		# Get DB session
		db_session = current_app.session()
		repo = CarRepo(db_session)
		cars = repo.list_with_owner()
		result = []
		for car in cars:
			owner = car.owner
			owner_data = OwnerOut(id=owner.id, name=owner.name, email=owner.email)
			car_data = CarOut(
				id=car.id,
				vin=car.vin,
				make=car.make,
				model=car.model,
				yearOfManufacture=car.year_of_manufacture,
				owner=owner_data
			)
			result.append(car_data.model_dump(by_alias=True))
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
