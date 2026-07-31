"""
Simulation Module - SQLAlchemy Models

Defines database tables for storing deterministic
simulation results.

Tables
------
1. simulation_results
2. monthly_simulation_data
3. hourly_simulation_profile
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base


# ============================================================
# Simulation Summary
# ============================================================

class SimulationResult(Base):
    """
    Stores one complete simulation summary for a project.
    """

    __tablename__ = "simulation_results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
        index=True
    )

    pv_daily_avg_kwh: Mapped[float] = mapped_column(Float)
    pv_monthly_avg_kwh: Mapped[float] = mapped_column(Float)
    pv_annual_kwh: Mapped[float] = mapped_column(Float)

    pv_specific_production_kwh_per_kwp_year: Mapped[float] = mapped_column(Float)

    capacity_factor_pct: Mapped[float] = mapped_column(Float)

    energy_consumption_daily_kwh: Mapped[float] = mapped_column(Float)
    energy_consumption_monthly_kwh: Mapped[float] = mapped_column(Float)
    energy_consumption_annual_kwh: Mapped[float] = mapped_column(Float)

    peak_load_kw: Mapped[float] = mapped_column(Float)

    battery_daily_throughput_kwh: Mapped[float] = mapped_column(Float)
    battery_usable_capacity_kwh: Mapped[float] = mapped_column(Float)
    battery_annual_losses_kwh: Mapped[float] = mapped_column(Float)
    battery_round_trip_efficiency_pct: Mapped[float] = mapped_column(Float)

    total_system_losses_pct: Mapped[float] = mapped_column(Float)

    self_consumption_pct: Mapped[float] = mapped_column(Float)
    self_sufficiency_pct: Mapped[float] = mapped_column(Float)

    grid_import_kwh: Mapped[float] = mapped_column(Float)
    grid_export_kwh: Mapped[float] = mapped_column(Float)

    co2_savings_kg: Mapped[float] = mapped_column(Float)

    simulated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    monthly_results = relationship(
        "MonthlySimulationData",
        back_populates="simulation",
        cascade="all, delete-orphan"
    )

    hourly_results = relationship(
        "HourlySimulationProfile",
        back_populates="simulation",
        cascade="all, delete-orphan"
    )


# ============================================================
# Monthly Results
# ============================================================

class MonthlySimulationData(Base):
    """
    Stores monthly energy values.
    """

    __tablename__ = "monthly_simulation_data"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    simulation_id: Mapped[int] = mapped_column(
        ForeignKey("simulation_results.id"),
        nullable=False,
        index=True
    )

    month: Mapped[str] = mapped_column(String(10))

    pv_generation_kwh: Mapped[float] = mapped_column(Float)

    load_consumption_kwh: Mapped[float] = mapped_column(Float)

    battery_throughput_kwh: Mapped[float] = mapped_column(Float)

    simulation = relationship(
        "SimulationResult",
        back_populates="monthly_results"
    )


# ============================================================
# Hourly Profile
# ============================================================

class HourlySimulationProfile(Base):
    """
    Stores representative hourly profile.
    """

    __tablename__ = "hourly_simulation_profile"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    simulation_id: Mapped[int] = mapped_column(
        ForeignKey("simulation_results.id"),
        nullable=False,
        index=True
    )

    hour: Mapped[str] = mapped_column(String(5))

    pv_generation_kwh: Mapped[float] = mapped_column(Float)

    load_consumption_kwh: Mapped[float] = mapped_column(Float)

    battery_charge_kwh: Mapped[float] = mapped_column(Float)

    battery_discharge_kwh: Mapped[float] = mapped_column(Float)

    simulation = relationship(
        "SimulationResult",
        back_populates="hourly_results"
    )