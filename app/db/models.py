from datetime import date, datetime
from sqlalchemy import String, Integer, Date, DateTime, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import db

class Owner(db.Model):
    __tablename__ = "owner"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)


    cars: Mapped[list["Car"]] = relationship(back_populates="owner", cascade="all, delete-orphan")

class Car(db.Model):
    __tablename__ = "car"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vin: Mapped[str] = mapped_column(String(17), nullable=False, unique=True)
    make: Mapped[str | None] = mapped_column(String(100))
    model: Mapped[str | None] = mapped_column(String(100))
    year_of_manufacture: Mapped[int | None] = mapped_column(Integer)

    owner_id: Mapped[int] = mapped_column(ForeignKey("owner.id", ondelete="RESTRICT"), nullable=False)
    owner: Mapped[Owner] = relationship(back_populates="cars")

    claims: Mapped[list["Claim"]] = relationship("Claim", back_populates="car", cascade="all, delete-orphan")
    policies: Mapped[list["InsurancePolicy"]] = relationship("InsurancePolicy", back_populates="car", cascade="all, delete-orphan")

class Claim(db.Model):
    __tablename__ = "claim"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id", ondelete="CASCADE"), nullable=False, index=True)
    claim_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


    car: Mapped[Car] = relationship(back_populates="claims")

class InsurancePolicy(db.Model):
    __tablename__ = "insurance_policy"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id", ondelete="CASCADE"), nullable=False, index=True)
    provider: Mapped[str | None] = mapped_column(String(255))
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    logged_expiry_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


    car: Mapped[Car] = relationship(back_populates="policies")


    __table_args__ = (
    UniqueConstraint("car_id", "start_date", "end_date", name="uq_policy_span"),
    )
