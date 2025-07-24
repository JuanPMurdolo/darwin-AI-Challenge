from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import date


class AnalyticsRequest(BaseModel):
    user_id: str = Field(..., description="ID del usuario a analizar")
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
    average_by_category: Dict[str, float] = Field(default_factory=dict)
    monthly_variation_percentage: float = 0.0


class AnalyticsResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[AnalyticsResult] = None


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[AnalyticsResult] = None
    error: Optional[str] = None
