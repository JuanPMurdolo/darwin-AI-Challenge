from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class AnalyticsRequest(BaseModel):
    user_id: int = Field(..., description="ID del usuario a analizar")
    start_date: Optional[date] = Field(None, description="Fecha de inicio del análisis")
    end_date: Optional[date] = Field(None, description="Fecha de fin del análisis")


class CategoryBreakdown(BaseModel):
    category: str
    total: float


class AnalyticsResult(BaseModel):
    total_expenses: float
    start_date: date
    end_date: date
    category_breakdown: List[CategoryBreakdown]


class AnalyticsResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[AnalyticsResult] = None
