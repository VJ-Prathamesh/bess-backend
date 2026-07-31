"""
Simulation Calculation Engine

This module contains ONLY deterministic engineering calculations.

Rules:
- No database access
- No FastAPI imports
- No SQLAlchemy
- No repository calls
- No HTTP exceptions

Input:
    Aggregated engineering data from previous modules.

Output:
    Simulation KPIs.
"""

from dataclasses import dataclass
from typing import Dict

# ==========================================================
# Constants
# ==========================================================

DAYS_PER_MONTH = 30
MONTHS_PER_YEAR = 12
HOURS_PER_YEAR = 8760

# Average India Grid Emission Factor
GRID_CO2_FACTOR = 0.82  # kg CO₂ / kWh


# ==========================================================
# Input Models
# ==========================================================

@dataclass
class PVInput:
    capacity_kwp: float
    average_sun_hours: float
    performance_ratio: float


@dataclass
class BatteryInput:
    capacity_kwh: float
    depth_of_discharge: float
    round_trip_efficiency: float


@dataclass
class LoadInput:
    daily_energy_kwh: float
    peak_load_kw: float


@dataclass
class LossInput:
    total_system_losses_pct: float


@dataclass
class SimulationInput:
    pv: PVInput
    battery: BatteryInput
    load: LoadInput
    losses: LossInput


# ==========================================================
# PV Calculations
# ==========================================================

def calculate_pv_daily_generation(
    pv: PVInput,
) -> float:
    """
    Daily PV Generation

    Formula:
        PV Capacity × Sun Hours × Performance Ratio
    """

    return (
        pv.capacity_kwp
        * pv.average_sun_hours
        * pv.performance_ratio
    )


def calculate_pv_monthly_generation(
    daily_generation: float,
) -> float:

    return daily_generation * DAYS_PER_MONTH


def calculate_pv_annual_generation(
    monthly_generation: float,
) -> float:

    return monthly_generation * MONTHS_PER_YEAR


def calculate_specific_production(
    annual_generation: float,
    installed_capacity: float,
) -> float:

    if installed_capacity == 0:
        return 0

    return annual_generation / installed_capacity


def calculate_capacity_factor(
    annual_generation: float,
    installed_capacity: float,
) -> float:

    if installed_capacity == 0:
        return 0

    return (
        annual_generation
        / (installed_capacity * HOURS_PER_YEAR)
    ) * 100


# ==========================================================
# Load Calculations
# ==========================================================

def calculate_monthly_load(
    load: LoadInput,
) -> float:

    return load.daily_energy_kwh * DAYS_PER_MONTH


def calculate_annual_load(
    monthly_load: float,
) -> float:

    return monthly_load * MONTHS_PER_YEAR


# ==========================================================
# Battery Calculations
# ==========================================================

def calculate_usable_capacity(
    battery: BatteryInput,
) -> float:

    return (
        battery.capacity_kwh
        * battery.depth_of_discharge
    )


def calculate_daily_throughput(
    usable_capacity: float,
    battery: BatteryInput,
) -> float:

    return (
        usable_capacity
        * battery.round_trip_efficiency
    )


def calculate_annual_battery_losses(
    throughput: float,
    battery: BatteryInput,
) -> float:

    return (
        throughput
        * (1 - battery.round_trip_efficiency)
        * 365
    )


# ==========================================================
# Grid Calculations
# ==========================================================

def calculate_grid_import(
    annual_load: float,
    annual_generation: float,
) -> float:

    return max(
        annual_load - annual_generation,
        0,
    )


def calculate_grid_export(
    annual_generation: float,
    annual_load: float,
) -> float:

    return max(
        annual_generation - annual_load,
        0,
    )


def calculate_self_consumption(
    annual_generation: float,
    grid_export: float,
) -> float:

    if annual_generation == 0:
        return 0

    return (
        (annual_generation - grid_export)
        / annual_generation
    ) * 100


def calculate_self_sufficiency(
    annual_load: float,
    grid_import: float,
) -> float:

    if annual_load == 0:
        return 0

    return (
        (annual_load - grid_import)
        / annual_load
    ) * 100


# ==========================================================
# Loss Calculations
# ==========================================================

def calculate_total_system_losses(
    losses: LossInput,
) -> float:

    return losses.total_system_losses_pct


# ==========================================================
# Environmental Calculations
# ==========================================================

def calculate_co2_savings(
    annual_generation: float,
) -> float:

    return annual_generation * GRID_CO2_FACTOR


# ==========================================================
# Simulation Engine
# ==========================================================

def run_simulation(
    simulation: SimulationInput,
) -> Dict:
    """
    Runs complete deterministic simulation.

    Returns dictionary matching API response.
    """

    # -----------------------------
    # PV
    # -----------------------------

    pv_daily = calculate_pv_daily_generation(
        simulation.pv
    )

    pv_monthly = calculate_pv_monthly_generation(
        pv_daily
    )

    pv_annual = calculate_pv_annual_generation(
        pv_monthly
    )

    specific_production = calculate_specific_production(
        pv_annual,
        simulation.pv.capacity_kwp,
    )

    capacity_factor = calculate_capacity_factor(
        pv_annual,
        simulation.pv.capacity_kwp,
    )

    # -----------------------------
    # Load
    # -----------------------------

    monthly_load = calculate_monthly_load(
        simulation.load
    )

    annual_load = calculate_annual_load(
        monthly_load
    )

    # -----------------------------
    # Battery
    # -----------------------------

    usable_capacity = calculate_usable_capacity(
        simulation.battery
    )

    throughput = calculate_daily_throughput(
        usable_capacity,
        simulation.battery,
    )

    battery_losses = calculate_annual_battery_losses(
        throughput,
        simulation.battery,
    )

    # -----------------------------
    # Grid
    # -----------------------------

    grid_import = calculate_grid_import(
        annual_load,
        pv_annual,
    )

    grid_export = calculate_grid_export(
        pv_annual,
        annual_load,
    )

    self_consumption = calculate_self_consumption(
        pv_annual,
        grid_export,
    )

    self_sufficiency = calculate_self_sufficiency(
        annual_load,
        grid_import,
    )

    # -----------------------------
    # Environment
    # -----------------------------

    co2 = calculate_co2_savings(
        pv_annual
    )

    # -----------------------------
    # Final Result
    # -----------------------------

    return {

        "pv_daily_avg_kwh": round(pv_daily, 2),

        "pv_monthly_avg_kwh": round(pv_monthly, 2),

        "pv_annual_kwh": round(pv_annual, 2),

        "pv_specific_production_kwh_per_kwp_year":
            round(specific_production, 2),

        "capacity_factor_pct":
            round(capacity_factor, 2),

        "energy_consumption_daily_kwh":
            round(simulation.load.daily_energy_kwh, 2),

        "energy_consumption_monthly_kwh":
            round(monthly_load, 2),

        "energy_consumption_annual_kwh":
            round(annual_load, 2),

        "peak_load_kw":
            round(simulation.load.peak_load_kw, 2),

        "battery_daily_throughput_kwh":
            round(throughput, 2),

        "battery_usable_capacity_kwh":
            round(usable_capacity, 2),

        "battery_annual_losses_kwh":
            round(battery_losses, 2),

        "battery_round_trip_efficiency_pct":
            round(
                simulation.battery.round_trip_efficiency * 100,
                2,
            ),

        "total_system_losses_pct":
            round(
                calculate_total_system_losses(
                    simulation.losses
                ),
                2,
            ),

        "self_consumption_pct":
            round(self_consumption, 2),

        "self_sufficiency_pct":
            round(self_sufficiency, 2),

        "grid_import_kwh":
            round(grid_import, 2),

        "grid_export_kwh":
            round(grid_export, 2),

        "co2_savings_kg":
            round(co2, 2),
    }