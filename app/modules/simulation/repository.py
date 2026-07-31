"""
Simulation Module - Repository

Responsible for all database interactions for the Simulation module.

No business logic.
No engineering calculations.
"""

from sqlalchemy.orm import Session

from .calculation import (
    BatteryInput,
    LoadInput,
    LossInput,
    PVInput,
    SimulationInput,
)
from .models import (
    SimulationResult,
    MonthlySimulationData,
    HourlySimulationProfile,
)


class SimulationRepository:
    """
    Repository for Simulation module.
    """

    def __init__(self, db: Session):
        self.db = db

    # ==========================================================
    # INPUT DATA (MOCK / INTEGRATION)
    # ==========================================================

    def get_simulation_inputs(self, project_id: int) -> SimulationInput:
        """
        Retrieves engineering inputs for simulation calculation.
        Temporary mock repository method until preceding modules are connected.
        """
        pv_input = PVInput(
            capacity_kwp=100.0,
            average_sun_hours=5.5,
            performance_ratio=0.80,
        )
        battery_input = BatteryInput(
            capacity_kwh=200.0,
            depth_of_discharge=0.85,
            round_trip_efficiency=0.92,
        )
        load_input = LoadInput(
            daily_energy_kwh=450.0,
            peak_load_kw=60.0,
        )
        loss_input = LossInput(
            total_system_losses_pct=12.5,
        )
        return SimulationInput(
            pv=pv_input,
            battery=battery_input,
            load=load_input,
            losses=loss_input,
        )


    # ==========================================================
    # CREATE
    # ==========================================================

    def save_simulation(
        self,
        simulation: SimulationResult,
    ) -> SimulationResult:

        self.db.add(simulation)
        self.db.commit()
        self.db.refresh(simulation)

        return simulation

    def save_monthly_results(
        self,
        monthly_results: list[MonthlySimulationData],
    ) -> None:

        self.db.add_all(monthly_results)
        self.db.commit()

    def save_hourly_profile(
        self,
        hourly_profile: list[HourlySimulationProfile],
    ) -> None:

        self.db.add_all(hourly_profile)
        self.db.commit()

    # ==========================================================
    # READ
    # ==========================================================

    def get_simulation(
        self,
        project_id: int,
    ) -> SimulationResult | None:

        return (
            self.db.query(SimulationResult)
            .filter(
                SimulationResult.project_id == project_id
            )
            .first()
        )

    def get_monthly_results(
        self,
        simulation_id: int,
    ) -> list[MonthlySimulationData]:

        return (
            self.db.query(MonthlySimulationData)
            .filter(
                MonthlySimulationData.simulation_id == simulation_id
            )
            .order_by(
                MonthlySimulationData.month
            )
            .all()
        )

    def get_hourly_profile(
        self,
        simulation_id: int,
    ) -> list[HourlySimulationProfile]:

        return (
            self.db.query(HourlySimulationProfile)
            .filter(
                HourlySimulationProfile.simulation_id == simulation_id
            )
            .order_by(
                HourlySimulationProfile.hour
            )
            .all()
        )

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_simulation(
        self,
        simulation: SimulationResult,
    ) -> None:

        self.db.delete(simulation)
        self.db.commit()