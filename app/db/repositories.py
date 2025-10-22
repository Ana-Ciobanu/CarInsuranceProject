from sqlalchemy import select, and_, func
from sqlalchemy.orm import Session
from datetime import date
from db.models import Car, InsurancePolicy, Claim

class CarRepo:
    def __init__(self, db: Session): self.db = db

    def get(self, car_id: int) -> Car | None:
        return self.db.get(Car, car_id)

    def list_with_owner(self) -> list[Car]:
        # eager load owner
        stmt = select(Car).join(Car.owner).order_by(Car.id)
        return list(self.db.scalars(stmt))

class PolicyRepo:
    def __init__(self, db: Session): self.db = db

    def create(self, car_id: int, start: date, end: date, provider: str | None):
        p = InsurancePolicy(car_id=car_id, start_date=start, end_date=end, provider=provider)
        self.db.add(p)
        return p
    
    def list_for_car(self, car_id: int) -> list[InsurancePolicy]:
        stmt = select(InsurancePolicy).where(InsurancePolicy.car_id == car_id).order_by(InsurancePolicy.start_date.asc(), InsurancePolicy.id.asc())
        return list(self.db.scalars(stmt))

    def active_on(self, car_id: int, d: date) -> bool:
        stmt = select(func.count(InsurancePolicy.id)).where(
            and_(InsurancePolicy.car_id==car_id,
                 InsurancePolicy.start_date <= d,
                 InsurancePolicy.end_date >= d)
        )
        return self.db.scalar(stmt) > 0

    def due_to_expire_today_and_unlogged(self, today: date):
        stmt = select(InsurancePolicy).where(
            and_(InsurancePolicy.end_date == today,
                 InsurancePolicy.logged_expiry_at.is_(None))
        )
        return list(self.db.scalars(stmt))

class ClaimRepo:
    def __init__(self, db: Session): self.db = db
    def create(self, car_id: int, d: date, desc: str, amount):
        c = Claim(car_id=car_id, claim_date=d, description=desc, amount=amount, created_at=func.now())
        self.db.add(c)
        return c

    def list_for_car(self, car_id: int) -> list[Claim]:
        stmt = select(Claim).where(Claim.car_id==car_id).order_by(Claim.claim_date.asc(), Claim.id.asc())
        return list(self.db.scalars(stmt))
