"""
Simulation Module - Router

Provides HTTP API routes for running and retrieving simulation data.

Rules:
- Router remains extremely thin
- No calculations
- No SQL
- No business logic
- No manual input building
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.simulation.repository import SimulationRepository
from app.modules.simulation.schemas import (
    DailyProfileResponse,
    HourlySimulationItem,
    MonthlySimulationItem,
    MonthlySimulationResponse,
    SimulationRunResponse,
    SimulationSummaryResponse,
)
from app.modules.simulation.service import SimulationService

router = APIRouter(prefix="", tags=["Simulation"])


def get_simulation_service(db: Session = Depends(get_db)) -> SimulationService:
    """
    Dependency injection provider for SimulationService.
    """
    repository = SimulationRepository(db)
    return SimulationService(repository)


@router.post(
    "/projects/{id}/simulation/run",
    response_model=SimulationRunResponse,
    status_code=status.HTTP_200_OK,
    summary="Run Simulation",
    description="Executes complete deterministic engineering simulation for a project.",
)
def run_simulation(
    id: int,
    service: SimulationService = Depends(get_simulation_service),
) -> SimulationRunResponse:
    """
    Triggers simulation calculation and persists results.
    """
    result = service.run_simulation(id)
    return SimulationRunResponse.model_validate(result)


@router.get(
    "/projects/{id}/simulation",
    response_model=SimulationSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Simulation Summary",
    description="Fetches stored simulation summary KPIs for a project.",
)
def get_simulation(
    id: int,
    service: SimulationService = Depends(get_simulation_service),
) -> SimulationSummaryResponse:
    """
    Fetches simulation summary.
    """
    result = service.get_simulation(id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Simulation results for project {id} not found.",
        )
    return SimulationSummaryResponse.model_validate(result)


@router.get(
    "/projects/{id}/simulation/monthly",
    response_model=MonthlySimulationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Monthly Simulation Results",
    description="Fetches monthly energy breakdown for a project simulation.",
)
def get_monthly_results(
    id: int,
    service: SimulationService = Depends(get_simulation_service),
) -> MonthlySimulationResponse:
    """
    Fetches monthly simulation data.
    """
    simulation = service.get_simulation(id)
    if not simulation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Simulation results for project {id} not found.",
        )

    monthly_data = service.get_monthly_results(id)
    items = [MonthlySimulationItem.model_validate(item) for item in monthly_data]
    return MonthlySimulationResponse(project_id=id, monthly_data=items)


@router.get(
    "/projects/{id}/simulation/daily-profile",
    response_model=DailyProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Daily Simulation Profile",
    description="Fetches representative 24-hour simulation profile for a project.",
)
def get_daily_profile(
    id: int,
    service: SimulationService = Depends(get_simulation_service),
) -> DailyProfileResponse:
    """
    Fetches daily hourly simulation profile.
    """
    simulation = service.get_simulation(id)
    if not simulation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Simulation results for project {id} not found.",
        )

    hourly_data = service.get_daily_profile(id)
    items = [HourlySimulationItem.model_validate(item) for item in hourly_data]
    return DailyProfileResponse(project_id=id, hourly_profile=items)
