"""
BOQ Module - FastAPI Router

Provides HTTP API routes for generating and retrieving Bill of Quantities (BOQ).

Rules:
- Extremely thin router
- No calculations
- No SQL
- No business logic
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.boq.repository import BOQRepository
from app.modules.boq.schemas import (
    BOQGenerateResponse,
    BOQItemResponse,
    BOQListResponse,
)
from app.modules.boq.service import BOQService

router = APIRouter(prefix="", tags=["BOQ"])


def get_boq_service(db: Session = Depends(get_db)) -> BOQService:
    """
    Dependency injection provider for BOQService.
    """
    repository = BOQRepository(db)
    return BOQService(repository)


@router.post(
    "/projects/{id}/boq/generate",
    response_model=BOQGenerateResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate BOQ",
    description="Generates a structured Bill of Quantities (BOQ) from engineering inputs for the specified project.",
)
def generate_boq(
    id: int,
    service: BOQService = Depends(get_boq_service),
) -> BOQGenerateResponse:
    """
    Triggers BOQ generation and persistence.
    """
    boq_items = service.generate_boq(id)
    items_response = [BOQItemResponse.model_validate(item) for item in boq_items]
    return BOQGenerateResponse(
        project_id=id,
        message="BOQ generated successfully",
        total_items=len(items_response),
        items=items_response,
    )


@router.get(
    "/projects/{id}/boq",
    response_model=BOQListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get BOQ",
    description="Retrieves the generated Bill of Quantities (BOQ) for the specified project.",
)
def get_boq(
    id: int,
    service: BOQService = Depends(get_boq_service),
) -> BOQListResponse:
    """
    Retrieves stored BOQ for a project.
    """
    boq_items = service.get_boq(id)
    if not boq_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"BOQ for project {id} not found. Please generate the BOQ first.",
        )

    items_response = [BOQItemResponse.model_validate(item) for item in boq_items]
    return BOQListResponse(
        project_id=id,
        total_items=len(items_response),
        items=items_response,
    )
