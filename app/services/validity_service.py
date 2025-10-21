from db.repositories import CarRepo, PolicyRepo
from sqlalchemy.orm import Session

def check_insurance_validity(db: Session, car_id: int, date):
	car = CarRepo(db).get(car_id)
	if not car:
		return None, 404
	valid = PolicyRepo(db).active_on(car_id, date)
	return valid, 200
