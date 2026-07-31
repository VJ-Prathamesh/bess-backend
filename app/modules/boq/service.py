"""
BOQ Module - Service Layer

Orchestrates business logic for generating and retrieving the Bill of Quantities.

Rules:
- Business logic only
- No raw SQL execution
- No engineering formulas
- No HTTP responses or HTTPException
- Uses repository for database persistence and engineering input retrieval
- Uses calculation.py for deterministic BOQ rule mapping
"""

import logging
from typing import List

from app.modules.boq.calculation import generate_boq as generate_boq_rules
from app.modules.boq.models import BOQItem
from app.modules.boq.repository import BOQRepository

logger = logging.getLogger(__name__)


class BOQService:
    """
    Orchestration layer for the BOQ module.
    """

    def __init__(self, repository: BOQRepository):
        self.repository = repository

    def generate_boq(self, project_id: int) -> List[BOQItem]:
        """
        Generates and persists a structured BOQ for the specified project.

        Workflow:
        1. Fetch aggregated engineering inputs from repository.
        2. Execute deterministic rule engine (calculation.generate_boq).
        3. Clear any existing BOQ entries for this project.
        4. Save generated BOQ items to database.
        5. Return persisted BOQ item models.
        """
        logger.info(f"Generating BOQ for project_id={project_id}")

        # 1. Fetch engineering inputs from upstream module data
        engineering_input = self.repository.get_engineering_input(project_id)

        # 2. Execute deterministic rule mapping
        calculated_items = generate_boq_rules(engineering_input)

        # 3. Convert calculated items into SQLAlchemy models
        boq_models = [
            BOQItem(
                project_id=project_id,
                sl_no=item.sl_no,
                category=item.category,
                description=item.description,
                specification=item.specification,
                manufacturer=item.manufacturer,
                model_number=item.model_number,
                unit=item.unit,
                quantity=item.quantity,
                remarks=item.remarks,
            )
            for item in calculated_items
        ]

        # 4. Clear prior BOQ entries for project_id
        logger.info(f"Removing prior BOQ entries for project_id={project_id}")
        self.repository.delete_existing_boq(project_id)

        # 5. Persist new BOQ items
        saved_items = self.repository.save_boq(project_id, boq_models)
        logger.info(
            f"Successfully generated and saved {len(saved_items)} BOQ items for project_id={project_id}"
        )
        return saved_items

    def get_boq(self, project_id: int) -> List[BOQItem]:
        """
        Retrieves the persisted BOQ for the specified project.
        """
        logger.info(f"Retrieving BOQ for project_id={project_id}")
        return self.repository.get_boq(project_id)
