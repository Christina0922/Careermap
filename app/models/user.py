from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    riasec_scores = relationship("UserRIASECScore", back_populates="user", uselist=False)
    survey_answers = relationship("SurveyAnswer", back_populates="user")


class UserRIASECScore(Base):
    __tablename__ = "user_riasec_scores"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    R = Column(Integer, default=0)
    I = Column(Integer, default=0)
    A = Column(Integer, default=0)
    S = Column(Integer, default=0)
    E = Column(Integer, default=0)
    C = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="riasec_scores")

