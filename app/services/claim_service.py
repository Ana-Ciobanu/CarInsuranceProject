from db.repositories import ClaimRepo, CarRepo
from sqlalchemy.orm import Session

def create_claim(db: Session, car_id: int, claim_date, description, amount):
	car = CarRepo(db).get(car_id)
	if not car:
		return None, 404
	if not description or amount <= 0:
		return None, 400
	claim = ClaimRepo(db).create(car_id, claim_date, description, amount)
	db.commit()
	return claim, 201
