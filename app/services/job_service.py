from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.job import Job, JobRIASEC, Skill, JobSkill, CareerPath
from app.schemas.job import JobDetail, SkillInfo, CareerPathStep, GapAnalysis


class JobService:
    """직업 관련 서비스"""

    @staticmethod
    def get_job_detail(db: Session, job_id: int) -> Optional[JobDetail]:
        """직업 상세 정보 조회"""
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return None

        # RIASEC 점수
        job_riasec = db.query(JobRIASEC).filter(JobRIASEC.job_id == job_id).first()
        riasec_scores = None
        if job_riasec:
            from app.schemas.user import RIASECScore
            riasec_scores = RIASECScore(
                R=job_riasec.R,
                I=job_riasec.I,
                A=job_riasec.A,
                S=job_riasec.S,
                E=job_riasec.E,
                C=job_riasec.C
            )

        # 스킬 정보
        job_skills = db.query(JobSkill, Skill).join(
            Skill, JobSkill.skill_id == Skill.id
        ).filter(JobSkill.job_id == job_id).all()

        skills = [
            SkillInfo(
                id=skill.id,
                skill_name=skill.skill_name,
                category=skill.category,
                importance_level=js.importance_level
            )
            for js, skill in job_skills
        ]

        # 커리어 패스
        career_paths = db.query(CareerPath).filter(
            CareerPath.job_id == job_id
        ).order_by(CareerPath.step_order).all()

        paths = [
            CareerPathStep(
                step_order=cp.step_order,
                step_title=cp.step_title,
                estimated_time=cp.estimated_time
            )
            for cp in career_paths
        ]

        return JobDetail(
            id=job.id,
            job_title=job.job_title,
            category=job.category,
            description=job.description,
            difficulty_level=job.difficulty_level,
            avg_preparation_time=job.avg_preparation_time,
            education_requirement=job.education_requirement,
            license_required=job.license_required,
            riasec=riasec_scores,
            skills=skills,
            career_paths=paths
        )

    @staticmethod
    def get_gap_analysis(
        db: Session,
        job_id: int,
        user_skills: Optional[List[int]] = None
    ) -> Optional[GapAnalysis]:
        """
        Gap 분석
        
        사용자 보유 스킬 vs 직업 요구 스킬 비교
        user_skills: 사용자가 보유한 스킬 ID 리스트 (현재는 None으로 처리)
        """
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return None

        # 직업 요구 스킬 조회
        job_skills = db.query(JobSkill, Skill).join(
            Skill, JobSkill.skill_id == Skill.id
        ).filter(JobSkill.job_id == job_id).all()

        required_skills = [
            SkillInfo(
                id=skill.id,
                skill_name=skill.skill_name,
                category=skill.category,
                importance_level=js.importance_level
            )
            for js, skill in job_skills
        ]

        # 부족한 스킬 계산 (현재는 사용자 스킬 정보가 없으므로 모든 스킬을 부족한 것으로 표시)
        # 실제 구현 시 user_skills와 비교하여 필터링
        missing_skills = required_skills.copy()
        if user_skills:
            missing_skills = [
                skill for skill in required_skills
                if skill.id not in user_skills
            ]

        return GapAnalysis(
            job_id=job.id,
            job_title=job.job_title,
            missing_skills=missing_skills,
            required_skills=required_skills
        )

