"""
Simulation Module - Service Layer

Orchestrates business logic for the Simulation module.

Rules:
- Business logic only
- No raw SQL
- No engineering formulas
- No HTTP responses or HTTPException
- Uses repository for database persistence
- Uses calculation.py for deterministic engineering calculations
"""

import logging
from typing import List, Optional

from app.modules.simulation.calculation import run_simulation
from app.modules.simulation.models import (
    HourlySimulationProfile,
    MonthlySimulationData,
    SimulationResult,
)
from app.modules.simulation.repository import SimulationRepository

logger = logging.getLogger(__name__)


class SimulationService:
    """
    Orchestration layer for executing and retrieving simulation results.
    """

    def __init__(self, repository: SimulationRepository):
        self.repository = repository

    def run_simulation(self, project_id: int) -> SimulationResult:
        """
        Executes complete simulation workflow for a project.

        1. Removes previous simulation for project_id if existing.
        2. Loads engineering inputs from repository.
        3. Executes calculation.run_simulation.
        4. Saves SimulationResult, MonthlySimulationData, and HourlySimulationProfile.
        5. Returns saved SimulationResult.
        """
        logger.info(f"Initiating simulation run for project_id={project_id}")

        # Check and remove existing simulation run for project_id
        existing = self.repository.get_simulation(project_id)
        if existing:
            logger.info(f"Deleting previous simulation for project_id={project_id}")
            self.repository.delete_simulation(existing)

        # 1 & 2 & 3. Load required engineering inputs
        simulation_input = self.repository.get_simulation_inputs(project_id)

        # 4. Call run_simulation from calculation engine
        kpis = run_simulation(simulation_input)

        # 5. Build and persist SimulationResult
        simulation_result = SimulationResult(
            project_id=project_id,
            pv_daily_avg_kwh=kpis["pv_daily_avg_kwh"],
            pv_monthly_avg_kwh=kpis["pv_monthly_avg_kwh"],
            pv_annual_kwh=kpis["pv_annual_kwh"],
            pv_specific_production_kwh_per_kwp_year=kpis[
                "pv_specific_production_kwh_per_kwp_year"
            ],
            capacity_factor_pct=kpis["capacity_factor_pct"],
            energy_consumption_daily_kwh=kpis["energy_consumption_daily_kwh"],
            energy_consumption_monthly_kwh=kpis["energy_consumption_monthly_kwh"],
            energy_consumption_annual_kwh=kpis["energy_consumption_annual_kwh"],
            peak_load_kw=kpis["peak_load_kw"],
            battery_daily_throughput_kwh=kpis["battery_daily_throughput_kwh"],
            battery_usable_capacity_kwh=kpis["battery_usable_capacity_kwh"],
            battery_annual_losses_kwh=kpis["battery_annual_losses_kwh"],
            battery_round_trip_efficiency_pct=kpis[
                "battery_round_trip_efficiency_pct"
            ],
            total_system_losses_pct=kpis["total_system_losses_pct"],
            self_consumption_pct=kpis["self_consumption_pct"],
            self_sufficiency_pct=kpis["self_sufficiency_pct"],
            grid_import_kwh=kpis["grid_import_kwh"],
            grid_export_kwh=kpis["grid_export_kwh"],
            co2_savings_kg=kpis["co2_savings_kg"],
        )

        saved_simulation = self.repository.save_simulation(simulation_result)

        # Build and persist MonthlySimulationData
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        monthly_records = [
            MonthlySimulationData(
                simulation_id=saved_simulation.id,
                month=month,
                pv_generation_kwh=kpis["pv_monthly_avg_kwh"],
                load_consumption_kwh=kpis["energy_consumption_monthly_kwh"],
                battery_throughput_kwh=round(
                    kpis["battery_daily_throughput_kwh"] * 30, 2
                ),
            )
            for month in months
        ]
        self.repository.save_monthly_results(monthly_records)

        # Build and persist HourlySimulationProfile (24 hours)
        daily_pv = kpis["pv_daily_avg_kwh"]
        daily_load = kpis["energy_consumption_daily_kwh"]
        hourly_load = round(daily_load / 24.0, 2)

        hourly_records = []
        for hour_idx in range(24):
            # Model solar generation hours (07:00 to 16:00)
            if 7 <= hour_idx <= 16:
                pv_gen = round(daily_pv / 10.0, 2)
            else:
                pv_gen = 0.0

            if pv_gen > hourly_load:
                batt_charge = round(pv_gen - hourly_load, 2)
                batt_discharge = 0.0
            elif pv_gen < hourly_load and hour_idx >= 17:
                batt_charge = 0.0
                batt_discharge = round(hourly_load - pv_gen, 2)
            else:
                batt_charge = 0.0
                batt_discharge = 0.0

            hourly_records.append(
                HourlySimulationProfile(
                    simulation_id=saved_simulation.id,
                    hour=f"{hour_idx:02d}:00",
                    pv_generation_kwh=pv_gen,
                    load_consumption_kwh=hourly_load,
                    battery_charge_kwh=batt_charge,
                    battery_discharge_kwh=batt_discharge,
                )
            )

        self.repository.save_hourly_profile(hourly_records)

        logger.info(
            f"Successfully executed and saved simulation results for project_id={project_id}"
        )
        # 6. Return saved simulation result
        return saved_simulation

    def get_simulation(self, project_id: int) -> Optional[SimulationResult]:
        """
        Retrieves saved simulation summary for a project.
        """
        logger.info(f"Retrieving simulation summary for project_id={project_id}")
        return self.repository.get_simulation(project_id)

    def get_monthly_results(self, project_id: int) -> List[MonthlySimulationData]:
        """
        Retrieves monthly simulation breakdown for a project.
        """
        logger.info(f"Retrieving monthly simulation results for project_id={project_id}")
        simulation = self.repository.get_simulation(project_id)
        if not simulation:
            return []
        return self.repository.get_monthly_results(simulation.id)

    def get_daily_profile(self, project_id: int) -> List[HourlySimulationProfile]:
        """
        Retrieves representative daily hourly profile for a project.
        """
        logger.info(f"Retrieving daily profile for project_id={project_id}")
        simulation = self.repository.get_simulation(project_id)
        if not simulation:
            return []
        return self.repository.get_hourly_profile(simulation.id)
