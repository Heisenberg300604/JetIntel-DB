from pydantic import BaseModel, Field
from typing import List, Optional


class JetBase(BaseModel):
    id: str = Field(..., description="Slug-style unique ID, e.g. 'gulfstream-g650er'")
    manufacturer: str
    model: str
    category: str
    range_nm: int
    cruise_knots: int
    cruise_mach: float
    max_passengers: int
    price_new_million: float
    price_used_million: float
    fuel_efficiency_lph: int
    cost_per_hour: int
    annual_cost_total: int
    annual_cost_fuel: int
    annual_cost_maintenance: int
    annual_cost_crew: int
    runway_required_ft: int
    year_introduced: int
    description: str
    tags: List[str]
    image_url: str


class JetCreate(JetBase):
    """Schema for creating a new jet — all fields required."""
    pass


class JetUpdate(BaseModel):
    """Schema for updating a jet — all fields optional."""
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    category: Optional[str] = None
    range_nm: Optional[int] = None
    cruise_knots: Optional[int] = None
    cruise_mach: Optional[float] = None
    max_passengers: Optional[int] = None
    price_new_million: Optional[float] = None
    price_used_million: Optional[float] = None
    fuel_efficiency_lph: Optional[int] = None
    cost_per_hour: Optional[int] = None
    annual_cost_total: Optional[int] = None
    annual_cost_fuel: Optional[int] = None
    annual_cost_maintenance: Optional[int] = None
    annual_cost_crew: Optional[int] = None
    runway_required_ft: Optional[int] = None
    year_introduced: Optional[int] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None


class JetResponse(JetBase):
    """Schema for returning jet data — includes mongo _id as string."""
    mongo_id: Optional[str] = Field(None, alias="_id")
