from pydantic import BaseModel
from typing import List


class SurveyAnswerSubmit(BaseModel):
    question_id: int
    option_ids: List[int]  # 복수 선택 지원


class SurveySubmitRequest(BaseModel):
    email: str
    answers: List[SurveyAnswerSubmit]


class SurveyOptionResponse(BaseModel):
    id: int
    option_text: str
    riasec_type: str
    score: int

    class Config:
        from_attributes = True


class SurveyQuestionResponse(BaseModel):
    id: int
    question_text: str
    options: List[SurveyOptionResponse]

    class Config:
        from_attributes = True

