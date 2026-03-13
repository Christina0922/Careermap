from pydantic import BaseModel
from typing import List, Optional
from app.schemas.user import RIASECScore


class JobResponse(BaseModel):
    id: int
    job_title: str
    category: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class JobRecommendation(BaseModel):
    job: JobResponse
    compatibility: float


class SkillInfo(BaseModel):
    id: int
    skill_name: str
    category: str
    importance_level: str

    class Config:
        from_attributes = True


class CareerPathStep(BaseModel):
    step_order: int
    step_title: str
    estimated_time: Optional[int] = None

    class Config:
        from_attributes = True


class JobDetail(BaseModel):
    id: int
    job_title: str
    category: str
    description: Optional[str] = None
    difficulty_level: Optional[str] = None
    avg_preparation_time: Optional[int] = None
    education_requirement: Optional[str] = None
    license_required: Optional[str] = None
    riasec: Optional[RIASECScore] = None
    skills: List[SkillInfo] = []
    career_paths: List[CareerPathStep] = []

    class Config:
        from_attributes = True


class GapAnalysis(BaseModel):
    job_id: int
    job_title: str
    missing_skills: List[SkillInfo] = []
    required_skills: List[SkillInfo] = []

