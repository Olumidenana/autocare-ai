"""
Database Models for AutoCare AI using SQLModel.
Supports customer profile, vehicle identity, fuel & oil logs, and diagnostic sessions.
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone_number: str = Field(unique=True, index=True)
    full_name: str = Field(default="Valued Driver")
    preferred_language: str = Field(default="pidgin")  # english, pidgin, yoruba, igbo
    primary_city: str = Field(default="Lagos")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    vehicles: List["Vehicle"] = Relationship(back_populates="customer")


class Vehicle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    
    vin: Optional[str] = Field(default=None, index=True)
    make: str  # Toyota, Lexus, Mercedes-Benz, etc.
    model: str  # C300, ES350, Camry, etc.
    year: int  # 2022
    engine_code: Optional[str] = None  # M274, 2GR-FE, etc.
    license_plate: Optional[str] = None
    
    # Odometer tracking without hardware
    verified_odometer_km: float = Field(default=0.0)
    last_odometer_verified_at: datetime = Field(default_factory=datetime.utcnow)
    estimated_daily_km: float = Field(default=35.0)  # Average daily commute
    
    # Oil & Fuel specs
    recommended_oil_spec: Optional[str] = None  # e.g., "0W-20 Full Synthetic"
    fuel_tank_capacity_liters: float = Field(default=60.0)
    
    customer: Optional[Customer] = Relationship(back_populates="vehicles")
    fuel_logs: List["FuelLog"] = Relationship(back_populates="vehicle")
    service_logs: List["ServiceLog"] = Relationship(back_populates="vehicle")


class FuelLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    vehicle_id: int = Field(foreign_key="vehicle.id")
    
    liters: float
    cost_naira: float
    station_brand: Optional[str] = None  # e.g., Total, Mobil, NNPC, Ardova
    odometer_reading: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    vehicle: Optional[Vehicle] = Relationship(back_populates="fuel_logs")


class ServiceLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    vehicle_id: int = Field(foreign_key="vehicle.id")
    
    service_type: str  # e.g. "Engine Oil & Filter", "Front Brake Pads", "Transmission Flush"
    odometer_km: float
    performed_at: datetime = Field(default_factory=datetime.utcnow)
    workshop_name: Optional[str] = None
    parts_replaced: Optional[str] = None
    notes: Optional[str] = None
    
    vehicle: Optional[Vehicle] = Relationship(back_populates="service_logs")


class DiagnosticSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone_number: str = Field(index=True)
    
    current_state: str = Field(default="idle")  # idle, awaiting_differential_answer, awaiting_photo
    active_vehicle_id: Optional[int] = None
    pending_question: Optional[str] = None
    differential_options: Optional[str] = None  # JSON string of options
    preliminary_fault: Optional[str] = None
    conversation_summary: Optional[str] = None
    last_interaction: datetime = Field(default_factory=datetime.utcnow)
