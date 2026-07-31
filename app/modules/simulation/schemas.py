"""
Simulation Module - Pydantic Schemas

Defines request and response models for the Simulation module.

This module contains no business logic.
It is responsible only for validating API requests and
serializing API responses.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# Base Response Models
# ============================================================

class SimulationRunResponse(BaseModel):
    """
    Response returned after successfully running a simulation.
    """

    model_config = ConfigDict(from_attributes=True)

    project_id: int

    pv_daily_avg_kwh: float
    pv_monthly_avg_kwh: float
    pv_annual_kwh: float

    pv_specific_production_kwh_per_kwp_year: float
    capacity_factor_pct: float

    energy_consumption_daily_kwh: float
    energy_consumption_monthly_kwh: float
    energy_consumption_annual_kwh: float

    peak_load_kw: float

    battery_daily_throughput_kwh: float
    battery_usable_capacity_kwh: float
    battery_annual_losses_kwh: float
    battery_round_trip_efficiency_pct: float

    total_system_losses_pct: float

    self_consumption_pct: float
    self_sufficiency_pct: float

    grid_import_kwh: float
    grid_export_kwh: float

    co2_savings_kg: float

    simulated_at: datetime


# ============================================================
# Simulation Summary
# ============================================================

class SimulationSummaryResponse(BaseModel):
    """
    Summary shown on the Simulation Dashboard.
    """

    model_config = ConfigDict(from_attributes=True)

    project_id: int

    pv_daily_avg_kwh: float
    pv_monthly_avg_kwh: float
    pv_annual_kwh: float

    pv_specific_production_kwh_per_kwp_year: float
    capacity_factor_pct: float

    energy_consumption_daily_kwh: float
    energy_consumption_monthly_kwh: float
    energy_consumption_annual_kwh: float

    peak_load_kw: float

    battery_daily_throughput_kwh: float
    battery_usable_capacity_kwh: float
    battery_annual_losses_kwh: float
    battery_round_trip_efficiency_pct: float

    total_system_losses_pct: float

    self_consumption_pct: float
    self_sufficiency_pct: float

    grid_import_kwh: float
    grid_export_kwh: float

    co2_savings_kg: float


# ============================================================
# Monthly Simulation
# ============================================================

class MonthlySimulationItem(BaseModel):
    """
    Monthly energy statistics.
    """

    model_config = ConfigDict(from_attributes=True)

    month: str = Field(
        examples=["Jan"]
    )

    pv_generation_kwh: float

    load_consumption_kwh: float

    battery_throughput_kwh: float


class MonthlySimulationResponse(BaseModel):

    project_id: int

    monthly_data: list[MonthlySimulationItem]


# ============================================================
# Daily Profile
# ============================================================

class HourlySimulationItem(BaseModel):
    """
    Represents one hourly simulation point.
    """

    model_config = ConfigDict(from_attributes=True)

    hour: str = Field(
        examples=["13:00"]
    )

    pv_generation_kwh: float

    load_consumption_kwh: float

    battery_charge_kwh: float

    battery_discharge_kwh: float


class DailyProfileResponse(BaseModel):

    project_id: int

    hourly_profile: list[HourlySimulationItem]


# ============================================================
# Error Response
# ============================================================

class ErrorResponse(BaseModel):
    """
    Standard API error response.
    """

    error: str

    message: str

    fields: dict | None = None