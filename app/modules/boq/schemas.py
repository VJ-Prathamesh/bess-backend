"""
BOQ Module - Pydantic Schemas

Defines request and response models for the BOQ module.

This module contains no business logic.
It is responsible only for validating API requests and
serializing API responses.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


# ============================================================
# BOQ Item Schema
# ============================================================

class BOQItemResponse(BaseModel):
    """
    Representation of a single Bill of Quantities line item.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    sl_no: int
    category: str
    description: str
    specification: str
    manufacturer: Optional[str] = None
    model_number: Optional[str] = None
    unit: str
    quantity: float
    remarks: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ============================================================
# BOQ Collection Responses
# ============================================================

class BOQGenerateResponse(BaseModel):
    """
    Response returned after successfully generating a BOQ.
    """

    project_id: int
    message: str = "BOQ generated successfully"
    total_items: int
    items: List[BOQItemResponse]


class BOQListResponse(BaseModel):
    """
    Response returned when retrieving a project's BOQ.
    """

    project_id: int
    total_items: int
    items: List[BOQItemResponse]
