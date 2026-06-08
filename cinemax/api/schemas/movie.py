# cinemax/api/schemas/movie.py
"""
DTOs / Schemas Pydantic para películas.
Principio: separación de capas — el API solo expone estos modelos.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


# ── Shared / Base ─────────────────────────────────────────────────────────────
class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    genre: Optional[str] = Field(None, max_length=100)
    duration: Optional[int] = Field(None, gt=0, description="Duración en minutos")
    classification: Optional[str] = Field(None, max_length=20)
    director: Optional[str] = Field(None, max_length=255)
    release_date: Optional[date] = None
    poster_url: Optional[str] = Field(None, max_length=500)
    trailer_url: Optional[str] = Field(None, max_length=500)
    price: Decimal = Field(default=Decimal("0.00"), ge=0)


# ── Create ────────────────────────────────────────────────────────────────────
class MovieCreate(MovieBase):
    active: bool = True


# ── Update ────────────────────────────────────────────────────────────────────
class MovieUpdate(BaseModel):
    """Todos los campos opcionales para PATCH/PUT parcial."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    genre: Optional[str] = None
    duration: Optional[int] = Field(None, gt=0)
    classification: Optional[str] = None
    director: Optional[str] = None
    release_date: Optional[date] = None
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    active: Optional[bool] = None


# ── Status toggle ─────────────────────────────────────────────────────────────
class MovieStatusUpdate(BaseModel):
    active: bool


# ── Response ──────────────────────────────────────────────────────────────────
class MovieResponse(MovieBase):
    id: int
    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
