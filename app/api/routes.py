from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.survey import SurveySubmitRequest, SurveyQuestionResponse
from app.schemas.job import JobRecommendation, JobDetail, GapAnalysis
from app.schemas.user import UserResponse, RIASECScore
from app.services.survey_service import SurveyService
from app.services.recommendation_service import RecommendationService
from app.services.job_service import JobService
from app.models.user import User

router = APIRouter()


@router.post("/api/survey/submit", response_model=RIASECScore)
def submit_survey(request: SurveySubmitRequest, db: Session = Depends(lambda: __import__('app.database', fromlist=['get_db']).get_db().__next__())):
    """
    설문 제출
    
    사용자의 설문 답변을 받아 RIASEC 점수를 계산하고 저장합니다.
    """
    user_riasec = SurveyService.submit_survey(db, request)
    return RIASECScore(
        R=user_riasec.R,
        I=user_riasec.I,
        A=user_riasec.A,
        S=user_riasec.S,
        E=user_riasec.E,
        C=user_riasec.C
    )


@router.get("/api/survey/questions", response_model=List[SurveyQuestionResponse])
def get_survey_questions(db: Session = Depends(get_db_dependency)):
    """설문 문항 조회"""
    return SurveyService.get_all_questions(db)


@router.get("/api/jobs/recommendations", response_model=List[JobRecommendation])
def get_job_recommendations(
    email: str,
    top_n: int = 10,
    db: Session = Depends(get_db_dependency)
):
    """
    직업 추천
    
    사용자의 RIASEC 점수를 기반으로 적합한 직업을 추천합니다.
    """
    # 사용자 조회
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please submit survey first.")

    return RecommendationService.get_recommendations(db, user.id, top_n)


@router.get("/api/jobs/{job_id}", response_model=JobDetail)
def get_job_detail(job_id: int, db: Session = Depends(get_db_dependency)):
    """직업 상세 정보 조회"""
    job_detail = JobService.get_job_detail(db, job_id)
    if not job_detail:
        raise HTTPException(status_code=404, detail="Job not found")
    return job_detail


@router.get("/api/jobs/{job_id}/gap", response_model=GapAnalysis)
def get_gap_analysis(
    job_id: int,
    user_skills: str = None,  # 쉼표로 구분된 스킬 ID 리스트 (예: "1,2,3")
    db: Session = Depends(get_db_dependency)
):
    """
    Gap 분석
    
    직업 요구 스킬과 사용자 보유 스킬을 비교하여 부족한 역량을 분석합니다.
    user_skills: 쉼표로 구분된 스킬 ID 리스트 (예: "1,2,3")
    """
    skill_ids = None
    if user_skills:
        try:
            skill_ids = [int(sid.strip()) for sid in user_skills.split(",")]
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid user_skills format")

    gap_analysis = JobService.get_gap_analysis(db, job_id, skill_ids)
    if not gap_analysis:
        raise HTTPException(status_code=404, detail="Job not found")
    return gap_analysis

