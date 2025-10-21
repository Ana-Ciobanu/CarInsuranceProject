from db.repositories import PolicyRepo, CarRepo
from sqlalchemy.orm import Session

def create_policy(db: Session, car_id: int, start, end, provider):
	car = CarRepo(db).get(car_id)
	if not car:
		return None, 404
	if end < start:
		return None, 400
	policy = PolicyRepo(db).create(car_id, start, end, provider)
	db.commit()
	return policy, 201

def get_active_policy(db: Session, car_id: int, date):
	return PolicyRepo(db).active_on(car_id, date)
