from app.db.repositories import ClaimRepo, PolicyRepo, CarRepo
from sqlalchemy.orm import Session

def get_car_history(db: Session, car_id: int):
	car = CarRepo(db).get(car_id)
	if not car:
		return None, 404
	claims = ClaimRepo(db).list_for_car(car_id)
	policies = PolicyRepo(db).list_for_car(car_id) if hasattr(PolicyRepo, 'list_for_car') else []
	history = []
	for p in policies:
		history.append({
			"type": "POLICY",
			"policyId": p.id,
			"startDate": p.start_date,
			"endDate": p.end_date,
			"provider": p.provider
		})
	for c in claims:
		history.append({
			"type": "CLAIM",
			"claimId": c.id,
			"claimDate": c.claim_date,
			"amount": c.amount,
			"description": c.description
		})
	history.sort(key=lambda x: x.get("startDate") or x.get("claimDate"))
	return history, 200
