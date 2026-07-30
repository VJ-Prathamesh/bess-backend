# BESS Backend

This repository contains the backend for the BESS project. It is currently built with FastAPI and runs as a Python service.

## Current environment

- Python: 3.13.7
- OS: Windows
- Package manager: pip
- Virtual environment: venv

## Prerequisites

Make sure the following are installed on your machine:

- Git
- Python 3.13.x
- pip

## Project setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd BESS-backend
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

### 3. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

## Runtime and dependency versions

The project is currently using the following package versions:

- FastAPI 0.141.1
- Uvicorn 0.52.0
- SQLAlchemy 2.0.51
- Pydantic 2.13.4
- Pydantic Settings 2.14.2
- Pydantic Core 2.46.4
- Starlette 1.3.1
- python-dotenv 1.2.2
- SQLAlchemy 2.0.51

## Run the application

From the project root:

```powershell
uvicorn app.main:app --reload
```

Then open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## Project structure

- app/ - main FastAPI application
- app/modules/ - feature modules such as projects, BOQ, cable sizing, reports, and more
- tests/ - test folder

## Notes

- The current application entrypoint is app.main:app.
- The root endpoint returns a simple welcome message.



# BESS Backend - Module File Guide

complete flow of module 

Each module folder (e.g. /projects, /load_profile) contains 6 files:

- **router.py** — Defines the API routes (URL + method). Receives the 
  HTTP request, calls service.py, returns the response. No logic here.

- **schemas.py** — Pydantic classes. Validates incoming request JSON 
  and defines outgoing response shape. Rejects bad input automatically.

- **service.py** — The orchestrator. Called by router.py. Decides 
  what needs to happen (call calculation.py for math, call 
  repository.py for DB), combines results, returns to router.py.

- **calculation.py** — Pure formulas only (sizing math, ampacity, 
  DoD, etc). No DB, no HTTP. Easiest file to unit test.

- **repository.py** — All DB queries (SELECT/INSERT/UPDATE/DELETE) 
  live here only. service.py never talks to the DB directly.

- **models.py** — SQLAlchemy table definition for this module. 
  Can reference other modules' tables via ForeignKey.

Flow: router.py → service.py → (calculation.py + repository.py) → back up
