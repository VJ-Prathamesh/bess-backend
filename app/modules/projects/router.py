from fastapi import APIRouter, HTTPException

from .schemas import ProjectCreate
from .service import (
    create_project,
    get_all_projects,
    get_project,
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post("/")
def create(project: ProjectCreate):
    return create_project(project)


@router.get("/")
def get_projects():
    return get_all_projects()


@router.get("/{project_id}")
def get_single_project(project_id: str):
    project = get_project(project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project Not Found",
        )

    return project
