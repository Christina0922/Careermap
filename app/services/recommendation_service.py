from sqlalchemy.orm import Session
from typing import List
from app.models.user import UserRIASECScore
from app.models.job import Job, JobRIASEC
from app.schemas.job import JobRecommendation, JobResponse
from app.constants import RIASEC_WEIGHT


class RecommendationService:
    """RIASEC 기반 직업 추천 서비스"""

    @staticmethod
    def calculate_distance(user_scores: UserRIASECScore, job_scores: JobRIASEC) -> float:
        """
        사용자와 직업의 RIASEC 벡터 거리 계산
        
        distance = |R_user - R_job| + |I_user - I_job| + ... + |C_user - C_job|
        """
        distance = (
            abs(user_scores.R - job_scores.R) +
            abs(user_scores.I - job_scores.I) +
            abs(user_scores.A - job_scores.A) +
            abs(user_scores.S - job_scores.S) +
            abs(user_scores.E - job_scores.E) +
            abs(user_scores.C - job_scores.C)
        )
        return distance

    @staticmethod
    def calculate_compatibility(distance: float) -> float:
        """
        적합도 계산
        
        compatibility = 100 - (distance * weight)
        """
        compatibility = 100 - (distance * RIASEC_WEIGHT)
        return max(0.0, min(100.0, compatibility))  # 0-100 범위로 제한

    @staticmethod
    def get_recommendations(db: Session, user_id: int, top_n: int = 10) -> List[JobRecommendation]:
        """
        사용자에게 직업 추천
        
        1. 사용자 RIASEC 점수 조회
        2. 모든 직업과 거리 계산
        3. 적합도 계산
        4. 상위 N개 직업 선택
        """
        # 사용자 RIASEC 점수 조회
        user_scores = db.query(UserRIASECScore).filter(
            UserRIASECScore.user_id == user_id
        ).first()

        if not user_scores:
            return []

        # 모든 직업과 RIASEC 점수 조회
        jobs_with_riasec = db.query(Job, JobRIASEC).join(
            JobRIASEC, Job.id == JobRIASEC.job_id
        ).all()

        # 거리 및 적합도 계산
        recommendations = []
        for job, job_riasec in jobs_with_riasec:
            distance = RecommendationService.calculate_distance(user_scores, job_riasec)
            compatibility = RecommendationService.calculate_compatibility(distance)

            recommendations.append(JobRecommendation(
                job=JobResponse(
                    id=job.id,
                    job_title=job.job_title,
                    category=job.category,
                    description=job.description
                ),
                compatibility=round(compatibility, 2)
            ))

        # 적합도 내림차순 정렬 및 상위 N개 선택
        recommendations.sort(key=lambda x: x.compatibility, reverse=True)
        return recommendations[:top_n]

