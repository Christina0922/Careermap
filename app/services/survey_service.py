from sqlalchemy.orm import Session
from app.models.user import User, UserRIASECScore
from app.models.survey import SurveyQuestion, SurveyOption, SurveyAnswer
from app.schemas.survey import SurveySubmitRequest, SurveyQuestionResponse, SurveyOptionResponse
from app.constants import RIASEC_TYPES


class SurveyService:
    """설문 관련 서비스"""

    @staticmethod
    def get_all_questions(db: Session) -> List[SurveyQuestionResponse]:
        """모든 설문 문항 조회"""
        questions = db.query(SurveyQuestion).order_by(SurveyQuestion.id).all()
        
        result = []
        for question in questions:
            options = [
                SurveyOptionResponse(
                    id=opt.id,
                    option_text=opt.option_text,
                    riasec_type=opt.riasec_type,
                    score=opt.score
                )
                for opt in question.options
            ]
            result.append(SurveyQuestionResponse(
                id=question.id,
                question_text=question.question_text,
                options=options
            ))
        
        return result

    @staticmethod
    def submit_survey(db: Session, request: SurveySubmitRequest) -> UserRIASECScore:
        """
        설문 제출 및 RIASEC 점수 계산
        
        1. 사용자 생성 또는 조회
        2. 답변 저장
        3. RIASEC 점수 계산 및 저장
        """
        # 사용자 조회 또는 생성
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            user = User(email=request.email)
            db.add(user)
            db.flush()

        # 기존 답변 삭제 (재응답 시)
        db.query(SurveyAnswer).filter(SurveyAnswer.user_id == user.id).delete()

        # RIASEC 점수 초기화
        riasec_scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}

        # 답변 저장 및 점수 계산 (복수 선택 지원)
        for answer_data in request.answers:
            for option_id in answer_data.option_ids:
                option = db.query(SurveyOption).filter(
                    SurveyOption.id == option_id
                ).first()

                if option:
                    # 답변 저장
                    answer = SurveyAnswer(
                        user_id=user.id,
                        question_id=answer_data.question_id,
                        option_id=option_id
                    )
                    db.add(answer)

                    # RIASEC 점수 누적
                    riasec_type = option.riasec_type
                    if riasec_type in riasec_scores:
                        riasec_scores[riasec_type] += option.score

        # RIASEC 점수 저장 또는 업데이트
        user_riasec = db.query(UserRIASECScore).filter(
            UserRIASECScore.user_id == user.id
        ).first()

        if user_riasec:
            user_riasec.R = riasec_scores["R"]
            user_riasec.I = riasec_scores["I"]
            user_riasec.A = riasec_scores["A"]
            user_riasec.S = riasec_scores["S"]
            user_riasec.E = riasec_scores["E"]
            user_riasec.C = riasec_scores["C"]
        else:
            user_riasec = UserRIASECScore(
                user_id=user.id,
                R=riasec_scores["R"],
                I=riasec_scores["I"],
                A=riasec_scores["A"],
                S=riasec_scores["S"],
                E=riasec_scores["E"],
                C=riasec_scores["C"]
            )
            db.add(user_riasec)

        db.commit()
        db.refresh(user_riasec)

        return user_riasec

