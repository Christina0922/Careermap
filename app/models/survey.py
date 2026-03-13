from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class SurveyQuestion(Base):
    __tablename__ = "survey_questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)

    # Relationships
    options = relationship("SurveyOption", back_populates="question")
    answers = relationship("SurveyAnswer", back_populates="question")


class SurveyOption(Base):
    __tablename__ = "survey_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("survey_questions.id"), nullable=False)
    option_text = Column(String, nullable=False)
    riasec_type = Column(String, nullable=False)  # R, I, A, S, E, C
    score = Column(Integer, default=2)

    # Relationships
    question = relationship("SurveyQuestion", back_populates="options")
    answers = relationship("SurveyAnswer", back_populates="option")


class SurveyAnswer(Base):
    __tablename__ = "survey_answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("survey_questions.id"), nullable=False)
    option_id = Column(Integer, ForeignKey("survey_options.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="survey_answers")
    question = relationship("SurveyQuestion", back_populates="answers")
    option = relationship("SurveyOption", back_populates="answers")

