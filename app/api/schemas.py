from pydantic import BaseModel, Field, field_validator
from datetime import date
from decimal import Decimal

def _check_date_range(d: date):
    if not (date(1900,1,1) <= d <= date(2100,12,31)):
        raise ValueError("Date out of allowed range (1900-2100).")
    return d

class OwnerIn(BaseModel):
    name: str
    email: str | None = None #provider is optional, defaults to None

class OwnerOut(BaseModel):
    id: int
    name: str
    email: str | None = None

class CarIn(BaseModel):
    vin: str
    make: str | None = None
    model: str | None = None
    yearOfManufacture: int | None = Field(default=None, alias="year_of_manufacture")
    ownerId: int = Field(alias="owner_id")

    @field_validator("yearOfManufacture")
    @classmethod
    def _range(cls, v):
        if v is not None and (v < 1900 or v > 2100):
            raise ValueError("year_of_manufacture out of allowed range (1900-2100).")
        return v

class CarOut(BaseModel):
    id: int
    vin: str
    make: str | None = None
    model: str | None = None
    yearOfManufacture: int | None = Field(default=None, alias="year_of_manufacture")
    owner: OwnerOut

    class Config:
        populate_by_name = True
        from_attributes = True

class InsuranceValidityOut(BaseModel):
    carId: int
    date: date
    valid: bool

    @field_validator("date", mode="before")
    @classmethod
    def _ensure_range(cls, v):
        return _check_date_range(v)

class ClaimIn(BaseModel):
    claimDate: date = Field(alias="claim_date")
    description: str
    amount: Decimal

    @field_validator("claimDate")
    @classmethod
    def _val_date(cls, v): return _check_date_range(v)

    @field_validator("amount")
    @classmethod
    def _val_amount(cls, v: Decimal):
        if v <= 0 or v > Decimal("100000000.00"):
            raise ValueError("Amount must be positive and reasonable.")
        return v

class ClaimOut(BaseModel):
    id: int
    carId: int
    claimDate: date
    description: str
    amount: Decimal

    class Config:
        from_attributes = True

class PolicyIn(BaseModel):
    startDate: date
    endDate: date
    provider: str | None = None

    @field_validator("endDate")
    @classmethod
    def _end_after_start(cls, v, info):
        start = info.data.get("startDate")
        if start and v < start:
            raise ValueError("endDate must not precede startDate.")
        _check_date_range(v)
        return v

    @field_validator("startDate")
    @classmethod
    def _range(cls, v): return _check_date_range(v)

class PolicyOut(BaseModel):
    id: int
    carId: int
    startDate: date
    endDate: date
    provider: str | None = None

    class Config:
        from_attributes = True

class HistoryItemPolicy(BaseModel):
    type: str = "POLICY"
    policyId: int
    startDate: date
    endDate: date
    provider: str | None = None

class HistoryItemClaim(BaseModel):
    type: str = "CLAIM"
    claimId: int
    claimDate: date
    amount: Decimal
    description: str
