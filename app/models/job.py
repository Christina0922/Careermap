from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False)  # JOB_CATEGORIES 키 사용
    description = Column(String)
    difficulty_level = Column(String)  # DIFFICULTY_LEVELS 키 사용
    avg_preparation_time = Column(Integer)  # 월 단위
    education_requirement = Column(String)  # EDUCATION_REQUIREMENTS 키 사용
    license_required = Column(String, nullable=True)

    # Relationships
    riasec = relationship("JobRIASEC", back_populates="job", uselist=False)
    skills = relationship("JobSkill", back_populates="job")
    career_paths = relationship("CareerPath", back_populates="job", order_by="CareerPath.step_order")


class JobRIASEC(Base):
    __tablename__ = "job_riasec"

    job_id = Column(Integer, ForeignKey("jobs.id"), primary_key=True)
    R = Column(Integer, default=0)
    I = Column(Integer, default=0)
    A = Column(Integer, default=0)
    S = Column(Integer, default=0)
    E = Column(Integer, default=0)
    C = Column(Integer, default=0)

    # Relationships
    job = relationship("Job", back_populates="riasec")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)  # SKILL_CATEGORIES 키 사용

    # Relationships
    job_skills = relationship("JobSkill", back_populates="skill")


class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    importance_level = Column(String, nullable=False)  # IMPORTANCE_LEVELS 키 사용

    # Relationships
    job = relationship("Job", back_populates="skills")
    skill = relationship("Skill", back_populates="job_skills")


class CareerPath(Base):
    __tablename__ = "career_paths"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    step_order = Column(Integer, nullable=False)
    step_title = Column(String, nullable=False)
    estimated_time = Column(Integer)  # 월 단위

    # Relationships
    job = relationship("Job", back_populates="career_paths")

