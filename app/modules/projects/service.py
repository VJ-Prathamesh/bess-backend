import uuid

from .repository import read_projects, save_projects


def create_project(project):
    projects = read_projects()
    new_project = project.model_dump()
    new_project["project_id"] = str(uuid.uuid4())
    new_project["current_step"] = 1
    projects.append(new_project)
    save_projects(projects)
    return new_project


def get_all_projects():
    return read_projects()


def get_project(project_id):
    projects = read_projects()
    for project in projects:
        if project["project_id"] == project_id:
            return project
    return None


def update_project(project_id, data):
    projects = read_projects()
    for project in projects:
        if project["project_id"] == project_id:
            project.update(data)
            save_projects(projects)
            return project
    return None
