"""
BOQ Module - Repository

Responsible for all database interactions for the BOQ module and for fetching
upstream engineering outputs required to generate the BOQ.

No business logic.
No engineering calculations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.modules.boq.calculation import (
    BESSConfigInfo,
    CableSizingInfo,
    EngineeringInput,
    LoadProfileInfo,
    ProjectInfo,
    PVSizingInfo,
    SimulationInfo,
    SystemLossesInfo,
)
from app.modules.boq.models import BOQItem


class BOQRepository:
    """
    Repository for BOQ database operations and upstream module data access.
    """

    def __init__(self, db: Session):
        self.db = db

    # ==========================================================
    # UPSTREAM ENGINEERING DATA FETCHERS (MOCK IMPLEMENTATIONS)
    # ==========================================================

    def get_project(self, project_id: int) -> ProjectInfo:
        # TODO: Replace this mock engineering data with actual PostgreSQL queries once the corresponding module has been implemented.
        return ProjectInfo(
            project_id=project_id,
            project_name=f"BESS Project #{project_id}",
            location="Solar Field Zone A",
        )

    def get_load_profile(self, project_id: int) -> LoadProfileInfo:
        # TODO: Replace this mock engineering data with actual PostgreSQL queries once the corresponding module has been implemented.
        return LoadProfileInfo(
            daily_energy_kwh=450.0,
            peak_load_kw=60.0,
        )

    def get_bess_configuration(self, project_id: int) -> BESSConfigInfo:
        # TODO: Replace this mock engineering data with actual PostgreSQL queries once the corresponding module has been implemented.
        return BESSConfigInfo(
            battery_capacity_kwh=200.0,
            battery_chemistry="LFP",
            rack_quantity=4,
            pcs_rating_kw=100.0,
        )

    def get_pv_configuration(self, project_id: int) -> PVSizingInfo:
        # TODO: Replace this mock engineering data with actual PostgreSQL queries once the corresponding module has been implemented.
        return PVSizingInfo(
            pv_capacity_kwp=100.0,
            pv_module_wattage_w=550.0,
            pv_module_count=182,
            mounting_type="Ground Mounted Fixed Tilt",
        )

    def get_cable_configuration(self, project_id: int) -> CableSizingInfo:
        # TODO: Replace this mock engineering data with actual PostgreSQL queries once the corresponding module has been implemented.
        return CableSizingInfo(
            dc_cable_length_m=500.0,
            dc_cable_sqmm=6.0,
            ac_cable_length_m=120.0,
            ac_cable_sqmm=95.0,
            cable_tray_length_m=150.0,
        )

    def get_system_losses(self, project_id: int) -> SystemLossesInfo:
        # TODO: Replace this mock engineering data with actual PostgreSQL queries once the corresponding module has been implemented.
        return SystemLossesInfo(
            dcdb_quantity=2,
            acdb_quantity=1,
        )

    def get_simulation_results(self, project_id: int) -> SimulationInfo:
        # TODO: Replace this mock engineering data with actual PostgreSQL queries once the corresponding module has been implemented.
        return SimulationInfo(
            annual_pv_generation_kwh=158400.0,
        )

    def get_engineering_input(self, project_id: int) -> EngineeringInput:
        """
        Aggregates all upstream engineering outputs for a project into an EngineeringInput DTO.
        """
        return EngineeringInput(
            project=self.get_project(project_id),
            load_profile=self.get_load_profile(project_id),
            bess_config=self.get_bess_configuration(project_id),
            pv_sizing=self.get_pv_configuration(project_id),
            cable_sizing=self.get_cable_configuration(project_id),
            system_losses=self.get_system_losses(project_id),
            simulation=self.get_simulation_results(project_id),
        )

    # ==========================================================
    # BOQ DATABASE PERSISTENCE (CRUD)
    # ==========================================================

    def delete_existing_boq(self, project_id: int) -> int:
        """
        Deletes all existing BOQ line items for a project.
        """
        deleted_count = (
            self.db.query(BOQItem)
            .filter(BOQItem.project_id == project_id)
            .delete(synchronize_session=False)
        )
        self.db.commit()
        return deleted_count

    def save_boq(self, project_id: int, boq_items: List[BOQItem]) -> List[BOQItem]:
        """
        Saves a list of BOQ line items for a project.
        """
        self.db.add_all(boq_items)
        self.db.commit()
        for item in boq_items:
            self.db.refresh(item)
        return boq_items

    def get_boq(self, project_id: int) -> List[BOQItem]:
        """
        Retrieves all BOQ line items for a project ordered by sl_no.
        """
        return (
            self.db.query(BOQItem)
            .filter(BOQItem.project_id == project_id)
            .order_by(BOQItem.sl_no.asc())
            .all()
        )
