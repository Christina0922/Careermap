"""
Seed 데이터 로드 스크립트

40개 설문 문항과 120개 직업 데이터를 데이터베이스에 로드합니다.
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.survey import SurveyQuestion, SurveyOption
from app.models.job import Job, JobRIASEC, Skill, JobSkill, CareerPath
from app.constants import (
    JOB_CATEGORIES,
    DIFFICULTY_LEVELS,
    EDUCATION_REQUIREMENTS,
    SKILL_CATEGORIES,
    IMPORTANCE_LEVELS,
    RIASEC_TYPES
)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)


def create_survey_questions(db: Session):
    """40개 설문 문항 생성"""
    questions_data = [
        {
            "question_text": "가장 흥미로운 활동은 무엇인가요?",
            "options": [
                {"text": "기계나 장비를 다루는 일", "riasec": "R", "score": 2},
                {"text": "데이터를 분석하는 일", "riasec": "I", "score": 2},
                {"text": "창의적인 작품을 만드는 일", "riasec": "A", "score": 2},
                {"text": "사람을 돕거나 상담하는 일", "riasec": "S", "score": 2},
                {"text": "사업이나 프로젝트를 이끄는 일", "riasec": "E", "score": 2},
                {"text": "자료를 정리하고 관리하는 일", "riasec": "C", "score": 2},
            ]
        },
        {
            "question_text": "어떤 환경에서 일하는 것을 선호하시나요?",
            "options": [
                {"text": "현장이나 작업장", "riasec": "R", "score": 2},
                {"text": "연구실이나 실험실", "riasec": "I", "score": 2},
                {"text": "스튜디오나 창작 공간", "riasec": "A", "score": 2},
                {"text": "학교나 상담실", "riasec": "S", "score": 2},
                {"text": "회의실이나 사무실", "riasec": "E", "score": 2},
                {"text": "정리된 사무 공간", "riasec": "C", "score": 2},
            ]
        },
        {
            "question_text": "어떤 능력을 가장 중요하게 생각하시나요?",
            "options": [
                {"text": "기술적 실무 능력", "riasec": "R", "score": 2},
                {"text": "논리적 분석 능력", "riasec": "I", "score": 2},
                {"text": "창의적 표현 능력", "riasec": "A", "score": 2},
                {"text": "소통과 공감 능력", "riasec": "S", "score": 2},
                {"text": "리더십과 경영 능력", "riasec": "E", "score": 2},
                {"text": "체계적 관리 능력", "riasec": "C", "score": 2},
            ]
        },
        {
            "question_text": "어떤 문제 해결 방식을 선호하시나요?",
            "options": [
                {"text": "직접 손으로 만들어 해결", "riasec": "R", "score": 2},
                {"text": "데이터와 연구로 분석", "riasec": "I", "score": 2},
                {"text": "새로운 아이디어로 접근", "riasec": "A", "score": 2},
                {"text": "사람들과 협력하여 해결", "riasec": "S", "score": 2},
                {"text": "전략과 계획으로 해결", "riasec": "E", "score": 2},
                {"text": "절차와 규칙에 따라 해결", "riasec": "C", "score": 2},
            ]
        },
        {
            "question_text": "어떤 성과를 가장 중요하게 생각하시나요?",
            "options": [
                {"text": "실용적이고 구체적인 결과물", "riasec": "R", "score": 2},
                {"text": "연구와 발견의 성과", "riasec": "I", "score": 2},
                {"text": "예술적이고 독창적인 작품", "riasec": "A", "score": 2},
                {"text": "사람들의 성장과 변화", "riasec": "S", "score": 2},
                {"text": "사업적 성공과 성장", "riasec": "E", "score": 2},
                {"text": "체계적이고 정확한 업무", "riasec": "C", "score": 2},
            ]
        },
    ]

    # 나머지 35개 문항 생성 (모두 다른 질문)
    all_questions = [
        {"text": "어떤 도구를 사용하는 것을 선호하시나요?", "options": [
            {"text": "공구나 기계", "riasec": "R", "score": 2},
            {"text": "컴퓨터나 분석 도구", "riasec": "I", "score": 2},
            {"text": "예술 도구나 소프트웨어", "riasec": "A", "score": 2},
            {"text": "교육 자료나 상담 도구", "riasec": "S", "score": 2},
            {"text": "경영 도구나 프레젠테이션", "riasec": "E", "score": 2},
            {"text": "문서나 데이터베이스", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 학습 방식을 선호하시나요?", "options": [
            {"text": "실습과 체험", "riasec": "R", "score": 2},
            {"text": "연구와 실험", "riasec": "I", "score": 2},
            {"text": "창작과 표현", "riasec": "A", "score": 2},
            {"text": "토론과 협력", "riasec": "S", "score": 2},
            {"text": "프로젝트와 기획", "riasec": "E", "score": 2},
            {"text": "체계적 학습과 정리", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 성격의 사람들과 일하고 싶으신가요?", "options": [
            {"text": "실용적이고 현실적인 사람들", "riasec": "R", "score": 2},
            {"text": "지적이고 분석적인 사람들", "riasec": "I", "score": 2},
            {"text": "창의적이고 독창적인 사람들", "riasec": "A", "score": 2},
            {"text": "친절하고 배려하는 사람들", "riasec": "S", "score": 2},
            {"text": "야심차고 목표 지향적인 사람들", "riasec": "E", "score": 2},
            {"text": "체계적이고 신중한 사람들", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 보상 방식을 선호하시나요?", "options": [
            {"text": "구체적인 결과물과 성취", "riasec": "R", "score": 2},
            {"text": "지식과 발견", "riasec": "I", "score": 2},
            {"text": "창의적 인정과 작품", "riasec": "A", "score": 2},
            {"text": "사람들의 감사와 성장", "riasec": "S", "score": 2},
            {"text": "성공과 리더십 인정", "riasec": "E", "score": 2},
            {"text": "안정과 체계적 보상", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 위험을 감수할 수 있나요?", "options": [
            {"text": "물리적 위험", "riasec": "R", "score": 2},
            {"text": "연구 실패 위험", "riasec": "I", "score": 2},
            {"text": "창의적 실험 위험", "riasec": "A", "score": 2},
            {"text": "인간관계 위험", "riasec": "S", "score": 2},
            {"text": "사업적 위험", "riasec": "E", "score": 2},
            {"text": "최소한의 위험", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 시간대에 일하는 것을 선호하시나요?", "options": [
            {"text": "일찍 시작해서 일찍 마치는 시간", "riasec": "R", "score": 2},
            {"text": "집중할 수 있는 조용한 시간", "riasec": "I", "score": 2},
            {"text": "자유롭게 창작할 수 있는 시간", "riasec": "A", "score": 2},
            {"text": "사람들과 소통할 수 있는 시간", "riasec": "S", "score": 2},
            {"text": "회의와 협상이 많은 시간", "riasec": "E", "score": 2},
            {"text": "규칙적이고 예측 가능한 시간", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 의사소통 방식을 선호하시나요?", "options": [
            {"text": "간단명료한 지시와 설명", "riasec": "R", "score": 2},
            {"text": "논리적이고 체계적인 토론", "riasec": "I", "score": 2},
            {"text": "시각적이고 표현적인 소통", "riasec": "A", "score": 2},
            {"text": "공감과 이해를 바탕으로 한 대화", "riasec": "S", "score": 2},
            {"text": "설득과 협상 중심의 소통", "riasec": "E", "score": 2},
            {"text": "문서와 기록을 통한 소통", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 압박 상황에서 더 잘 일하시나요?", "options": [
            {"text": "물리적 도전과 한계 극복", "riasec": "R", "score": 2},
            {"text": "지적 문제 해결 압박", "riasec": "I", "score": 2},
            {"text": "창의적 아이디어 발굴 압박", "riasec": "A", "score": 2},
            {"text": "사람들의 기대와 신뢰", "riasec": "S", "score": 2},
            {"text": "목표 달성과 성과 압박", "riasec": "E", "score": 2},
            {"text": "정확성과 완벽함 요구", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 프로젝트에 관심이 있나요?", "options": [
            {"text": "제품 제작이나 건설 프로젝트", "riasec": "R", "score": 2},
            {"text": "연구나 실험 프로젝트", "riasec": "I", "score": 2},
            {"text": "예술 작품이나 창작 프로젝트", "riasec": "A", "score": 2},
            {"text": "교육이나 사회적 프로젝트", "riasec": "S", "score": 2},
            {"text": "사업이나 마케팅 프로젝트", "riasec": "E", "score": 2},
            {"text": "시스템 구축이나 조직 프로젝트", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 책을 선호하시나요?", "options": [
            {"text": "기술 매뉴얼이나 실용서", "riasec": "R", "score": 2},
            {"text": "과학이나 학술서", "riasec": "I", "score": 2},
            {"text": "소설이나 예술서", "riasec": "A", "score": 2},
            {"text": "인문학이나 심리학 서적", "riasec": "S", "score": 2},
            {"text": "경영이나 자기계발서", "riasec": "E", "score": 2},
            {"text": "참고서나 자료집", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 영화나 드라마를 좋아하시나요?", "options": [
            {"text": "액션이나 모험 영화", "riasec": "R", "score": 2},
            {"text": "SF나 미스터리 영화", "riasec": "I", "score": 2},
            {"text": "예술 영화나 독립 영화", "riasec": "A", "score": 2},
            {"text": "드라마나 휴먼 영화", "riasec": "S", "score": 2},
            {"text": "스릴러나 범죄 영화", "riasec": "E", "score": 2},
            {"text": "다큐멘터리나 정보 영화", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 취미 활동을 즐기시나요?", "options": [
            {"text": "만들기나 수리 활동", "riasec": "R", "score": 2},
            {"text": "독서나 연구 활동", "riasec": "I", "score": 2},
            {"text": "예술이나 창작 활동", "riasec": "A", "score": 2},
            {"text": "봉사나 모임 활동", "riasec": "S", "score": 2},
            {"text": "네트워킹이나 경쟁 활동", "riasec": "E", "score": 2},
            {"text": "수집이나 정리 활동", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 여행을 선호하시나요?", "options": [
            {"text": "모험 여행이나 액티비티", "riasec": "R", "score": 2},
            {"text": "역사나 문화 탐방", "riasec": "I", "score": 2},
            {"text": "예술 도시나 갤러리 탐방", "riasec": "A", "score": 2},
            {"text": "사람들과 함께하는 여행", "riasec": "S", "score": 2},
            {"text": "럭셔리나 특별한 경험", "riasec": "E", "score": 2},
            {"text": "계획적이고 체계적인 여행", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 음악을 좋아하시나요?", "options": [
            {"text": "록이나 메탈 음악", "riasec": "R", "score": 2},
            {"text": "클래식이나 재즈", "riasec": "I", "score": 2},
            {"text": "인디나 실험적 음악", "riasec": "A", "score": 2},
            {"text": "팝이나 발라드", "riasec": "S", "score": 2},
            {"text": "힙합이나 일렉트로닉", "riasec": "E", "score": 2},
            {"text": "편안한 배경음악", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 스포츠를 좋아하시나요?", "options": [
            {"text": "육상이나 근력 운동", "riasec": "R", "score": 2},
            {"text": "전략적 보드게임", "riasec": "I", "score": 2},
            {"text": "예술적 스포츠", "riasec": "A", "score": 2},
            {"text": "팀 스포츠", "riasec": "S", "score": 2},
            {"text": "경쟁적 스포츠", "riasec": "E", "score": 2},
            {"text": "규칙적 운동", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 게임을 좋아하시나요?", "options": [
            {"text": "액션이나 시뮬레이션 게임", "riasec": "R", "score": 2},
            {"text": "퍼즐이나 전략 게임", "riasec": "I", "score": 2},
            {"text": "창의적 샌드박스 게임", "riasec": "A", "score": 2},
            {"text": "멀티플레이어 협력 게임", "riasec": "S", "score": 2},
            {"text": "경쟁적 PvP 게임", "riasec": "E", "score": 2},
            {"text": "규칙적 퍼즐 게임", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 뉴스를 주로 보시나요?", "options": [
            {"text": "기술이나 산업 뉴스", "riasec": "R", "score": 2},
            {"text": "과학이나 연구 뉴스", "riasec": "I", "score": 2},
            {"text": "문화나 예술 뉴스", "riasec": "A", "score": 2},
            {"text": "사회나 교육 뉴스", "riasec": "S", "score": 2},
            {"text": "경제나 경영 뉴스", "riasec": "E", "score": 2},
            {"text": "정치나 행정 뉴스", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 강의나 세미나에 관심이 있나요?", "options": [
            {"text": "실습 중심 워크샵", "riasec": "R", "score": 2},
            {"text": "학술 세미나나 강연", "riasec": "I", "score": 2},
            {"text": "창의성 워크샵", "riasec": "A", "score": 2},
            {"text": "인문학 강의", "riasec": "S", "score": 2},
            {"text": "경영이나 리더십 강의", "riasec": "E", "score": 2},
            {"text": "기술이나 자격증 강의", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 모임에 참여하고 싶으신가요?", "options": [
            {"text": "만들기 모임이나 동호회", "riasec": "R", "score": 2},
            {"text": "독서 모임이나 토론회", "riasec": "I", "score": 2},
            {"text": "예술 모임이나 창작 모임", "riasec": "A", "score": 2},
            {"text": "봉사 모임이나 모임", "riasec": "S", "score": 2},
            {"text": "네트워킹 모임", "riasec": "E", "score": 2},
            {"text": "정기 모임이나 클럽", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 쇼핑을 선호하시나요?", "options": [
            {"text": "도구나 기계 쇼핑", "riasec": "R", "score": 2},
            {"text": "책이나 자료 쇼핑", "riasec": "I", "score": 2},
            {"text": "예술품이나 디자인 쇼핑", "riasec": "A", "score": 2},
            {"text": "선물이나 기념품 쇼핑", "riasec": "S", "score": 2},
            {"text": "명품이나 브랜드 쇼핑", "riasec": "E", "score": 2},
            {"text": "필수품이나 실용품 쇼핑", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 음식을 좋아하시나요?", "options": [
            {"text": "실용적이고 든든한 음식", "riasec": "R", "score": 2},
            {"text": "건강하고 영양 있는 음식", "riasec": "I", "score": 2},
            {"text": "예술적으로 플레이팅된 음식", "riasec": "A", "score": 2},
            {"text": "함께 나누는 음식", "riasec": "S", "score": 2},
            {"text": "고급 레스토랑 음식", "riasec": "E", "score": 2},
            {"text": "규칙적이고 일정한 음식", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 옷을 선호하시나요?", "options": [
            {"text": "실용적이고 편한 옷", "riasec": "R", "score": 2},
            {"text": "기능적이고 실용적인 옷", "riasec": "I", "score": 2},
            {"text": "개성 있고 스타일리시한 옷", "riasec": "A", "score": 2},
            {"text": "편안하고 친근한 옷", "riasec": "S", "score": 2},
            {"text": "비즈니스나 정장", "riasec": "E", "score": 2},
            {"text": "깔끔하고 정돈된 옷", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 집을 선호하시나요?", "options": [
            {"text": "실용적이고 기능적인 집", "riasec": "R", "score": 2},
            {"text": "조용하고 집중할 수 있는 집", "riasec": "I", "score": 2},
            {"text": "예술적이고 독특한 집", "riasec": "A", "score": 2},
            {"text": "가족이나 친구들과 함께하는 집", "riasec": "S", "score": 2},
            {"text": "고급스럽고 인상적인 집", "riasec": "E", "score": 2},
            {"text": "정돈되고 체계적인 집", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 차를 선호하시나요?", "options": [
            {"text": "실용적이고 튼튼한 차", "riasec": "R", "score": 2},
            {"text": "기술적이고 효율적인 차", "riasec": "I", "score": 2},
            {"text": "디자인이 예쁜 차", "riasec": "A", "score": 2},
            {"text": "가족용 넓은 차", "riasec": "S", "score": 2},
            {"text": "고급스럽고 브랜드 차", "riasec": "E", "score": 2},
            {"text": "안전하고 신뢰할 수 있는 차", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 휴가를 선호하시나요?", "options": [
            {"text": "액티비티 휴가", "riasec": "R", "score": 2},
            {"text": "학습이나 탐구 휴가", "riasec": "I", "score": 2},
            {"text": "예술 도시 탐방 휴가", "riasec": "A", "score": 2},
            {"text": "가족이나 친구들과의 휴가", "riasec": "S", "score": 2},
            {"text": "럭셔리 휴가", "riasec": "E", "score": 2},
            {"text": "계획적이고 안정적인 휴가", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 선물을 좋아하시나요?", "options": [
            {"text": "실용적인 도구나 기계", "riasec": "R", "score": 2},
            {"text": "책이나 학습 자료", "riasec": "I", "score": 2},
            {"text": "예술품이나 창작 도구", "riasec": "A", "score": 2},
            {"text": "의미 있는 기념품", "riasec": "S", "score": 2},
            {"text": "고급스러운 선물", "riasec": "E", "score": 2},
            {"text": "실용적이고 필요한 선물", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 앱을 자주 사용하시나요?", "options": [
            {"text": "생산성이나 도구 앱", "riasec": "R", "score": 2},
            {"text": "학습이나 정보 앱", "riasec": "I", "score": 2},
            {"text": "창작이나 예술 앱", "riasec": "A", "score": 2},
            {"text": "소셜이나 커뮤니케이션 앱", "riasec": "S", "score": 2},
            {"text": "비즈니스나 경영 앱", "riasec": "E", "score": 2},
            {"text": "조직이나 관리 앱", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 소셜 미디어를 선호하시나요?", "options": [
            {"text": "기술 중심 플랫폼", "riasec": "R", "score": 2},
            {"text": "정보 공유 플랫폼", "riasec": "I", "score": 2},
            {"text": "시각적 콘텐츠 플랫폼", "riasec": "A", "score": 2},
            {"text": "커뮤니티 중심 플랫폼", "riasec": "S", "score": 2},
            {"text": "네트워킹 플랫폼", "riasec": "E", "score": 2},
            {"text": "정보 정리 플랫폼", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 운동을 선호하시나요?", "options": [
            {"text": "근력 운동이나 헬스", "riasec": "R", "score": 2},
            {"text": "요가나 명상", "riasec": "I", "score": 2},
            {"text": "댄스나 예술적 운동", "riasec": "A", "score": 2},
            {"text": "그룹 운동이나 클래스", "riasec": "S", "score": 2},
            {"text": "경쟁적 스포츠", "riasec": "E", "score": 2},
            {"text": "규칙적 유산소 운동", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 카페를 선호하시나요?", "options": [
            {"text": "간단하고 실용적인 카페", "riasec": "R", "score": 2},
            {"text": "조용하고 집중할 수 있는 카페", "riasec": "I", "score": 2},
            {"text": "분위기 있고 예쁜 카페", "riasec": "A", "score": 2},
            {"text": "친근하고 편안한 카페", "riasec": "S", "score": 2},
            {"text": "고급스럽고 비즈니스 카페", "riasec": "E", "score": 2},
            {"text": "체인이나 규칙적인 카페", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 날씨를 선호하시나요?", "options": [
            {"text": "활동하기 좋은 맑은 날씨", "riasec": "R", "score": 2},
            {"text": "집중하기 좋은 시원한 날씨", "riasec": "I", "score": 2},
            {"text": "감성적인 날씨", "riasec": "A", "score": 2},
            {"text": "함께하기 좋은 날씨", "riasec": "S", "score": 2},
            {"text": "활동적이고 역동적인 날씨", "riasec": "E", "score": 2},
            {"text": "예측 가능한 안정적인 날씨", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 계절을 선호하시나요?", "options": [
            {"text": "활동하기 좋은 봄이나 가을", "riasec": "R", "score": 2},
            {"text": "집중하기 좋은 가을이나 겨울", "riasec": "I", "score": 2},
            {"text": "감성적인 계절", "riasec": "A", "score": 2},
            {"text": "함께하기 좋은 계절", "riasec": "S", "score": 2},
            {"text": "활동적인 여름", "riasec": "E", "score": 2},
            {"text": "안정적인 계절", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 동물을 좋아하시나요?", "options": [
            {"text": "활동적인 개나 말", "riasec": "R", "score": 2},
            {"text": "지능적인 동물", "riasec": "I", "score": 2},
            {"text": "예쁘고 독특한 동물", "riasec": "A", "score": 2},
            {"text": "친근하고 사교적인 동물", "riasec": "S", "score": 2},
            {"text": "위엄 있는 동물", "riasec": "E", "score": 2},
            {"text": "규칙적이고 예측 가능한 동물", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 색상을 선호하시나요?", "options": [
            {"text": "실용적인 색상", "riasec": "R", "score": 2},
            {"text": "차분하고 신중한 색상", "riasec": "I", "score": 2},
            {"text": "밝고 창의적인 색상", "riasec": "A", "score": 2},
            {"text": "따뜻하고 친근한 색상", "riasec": "S", "score": 2},
            {"text": "강렬하고 인상적인 색상", "riasec": "E", "score": 2},
            {"text": "차분하고 안정적인 색상", "riasec": "C", "score": 2},
        ]},
        {"text": "어떤 종류의 향을 좋아하시나요?", "options": [
            {"text": "깔끔하고 실용적인 향", "riasec": "R", "score": 2},
            {"text": "은은하고 신비로운 향", "riasec": "I", "score": 2},
            {"text": "독특하고 창의적인 향", "riasec": "A", "score": 2},
            {"text": "따뜻하고 편안한 향", "riasec": "S", "score": 2},
            {"text": "강렬하고 인상적인 향", "riasec": "E", "score": 2},
            {"text": "차분하고 안정적인 향", "riasec": "C", "score": 2},
        ]},
    ]
    
    # 나머지 질문 추가 (40개까지)
    for i in range(5, 41):
        if i - 5 < len(all_questions):
            questions_data.append(all_questions[i - 5])
        else:
            # 기본 질문 템플릿 (반복 방지)
            questions_data.append({
                "question_text": f"다음 중 관심 있는 활동은? (질문 {i+1})",
                "options": [
                    {"text": "기계나 장비를 다루는 일", "riasec": "R", "score": 2},
                    {"text": "데이터를 분석하는 일", "riasec": "I", "score": 2},
                    {"text": "창의적인 작품을 만드는 일", "riasec": "A", "score": 2},
                    {"text": "사람을 돕거나 상담하는 일", "riasec": "S", "score": 2},
                    {"text": "사업이나 프로젝트를 이끄는 일", "riasec": "E", "score": 2},
                    {"text": "자료를 정리하고 관리하는 일", "riasec": "C", "score": 2},
                ]
            })

    # 데이터베이스에 저장
    for q_data in questions_data:
        # 질문 텍스트 추출 (다양한 키 이름 지원)
        question_text = q_data.get("question_text") or q_data.get("text", "")
        question = SurveyQuestion(question_text=question_text)
        db.add(question)
        db.flush()

        for opt_data in q_data["options"]:
            option = SurveyOption(
                question_id=question.id,
                option_text=opt_data["text"],
                riasec_type=opt_data["riasec"],
                score=opt_data["score"]
            )
            db.add(option)

    db.commit()
    print(f"[OK] {len(questions_data)}개 설문 문항 생성 완료")


def create_skills(db: Session):
    """공통 스킬 생성"""
    skills_data = [
        # 기술적 스킬
        {"name": "Python", "category": "TECHNICAL"},
        {"name": "Java", "category": "TECHNICAL"},
        {"name": "JavaScript", "category": "TECHNICAL"},
        {"name": "SQL", "category": "TECHNICAL"},
        {"name": "데이터 분석", "category": "TECHNICAL"},
        {"name": "머신러닝", "category": "TECHNICAL"},
        {"name": "웹 개발", "category": "TECHNICAL"},
        {"name": "모바일 개발", "category": "TECHNICAL"},
        {"name": "클라우드", "category": "TECHNICAL"},
        {"name": "네트워크", "category": "TECHNICAL"},
        # 소프트 스킬
        {"name": "커뮤니케이션", "category": "SOFT"},
        {"name": "리더십", "category": "SOFT"},
        {"name": "팀워크", "category": "SOFT"},
        {"name": "문제 해결", "category": "SOFT"},
        {"name": "프로젝트 관리", "category": "SOFT"},
        # 언어
        {"name": "영어", "category": "LANGUAGE"},
        {"name": "중국어", "category": "LANGUAGE"},
        {"name": "일본어", "category": "LANGUAGE"},
        # 자격증
        {"name": "정보처리기사", "category": "CERTIFICATION"},
        {"name": "공인회계사", "category": "CERTIFICATION"},
        {"name": "변리사", "category": "CERTIFICATION"},
        {"name": "의사면허", "category": "CERTIFICATION"},
    ]

    for skill_data in skills_data:
        # 중복 체크
        existing_skill = db.query(Skill).filter(Skill.skill_name == skill_data["name"]).first()
        if not existing_skill:
            skill = Skill(
                skill_name=skill_data["name"],
                category=skill_data["category"]
            )
            db.add(skill)

    db.commit()
    print(f"[OK] {len(skills_data)}개 스킬 생성 완료")


def create_jobs(db: Session):
    """120개 직업 생성"""
    jobs_data = [
        # 의료 (12개)
        {"title": "의사", "category": "MEDICAL", "riasec": {"I": 20, "S": 15, "R": 10, "E": 5, "A": 3, "C": 7}},
        {"title": "간호사", "category": "MEDICAL", "riasec": {"S": 20, "R": 12, "I": 8, "C": 10, "E": 5, "A": 5}},
        {"title": "수의사", "category": "MEDICAL", "riasec": {"I": 18, "R": 15, "S": 12, "C": 8, "E": 5, "A": 2}},
        {"title": "약사", "category": "MEDICAL", "riasec": {"I": 18, "C": 15, "S": 10, "R": 7, "E": 5, "A": 5}},
        {"title": "물리치료사", "category": "MEDICAL", "riasec": {"S": 18, "R": 15, "I": 10, "C": 7, "E": 5, "A": 5}},
        {"title": "임상병리사", "category": "MEDICAL", "riasec": {"I": 20, "C": 15, "R": 10, "S": 8, "E": 4, "A": 3}},
        {"title": "방사선사", "category": "MEDICAL", "riasec": {"I": 18, "R": 15, "C": 12, "S": 8, "E": 4, "A": 3}},
        {"title": "치과의사", "category": "MEDICAL", "riasec": {"I": 18, "R": 16, "S": 12, "E": 6, "C": 5, "A": 3}},
        {"title": "한의사", "category": "MEDICAL", "riasec": {"I": 17, "S": 15, "R": 10, "C": 8, "E": 5, "A": 5}},
        {"title": "응급구조사", "category": "MEDICAL", "riasec": {"R": 18, "S": 17, "I": 8, "C": 7, "E": 5, "A": 5}},
        {"title": "의료기사", "category": "MEDICAL", "riasec": {"R": 16, "I": 14, "C": 12, "S": 10, "E": 5, "A": 3}},
        {"title": "보건의료정보관리사", "category": "MEDICAL", "riasec": {"C": 18, "I": 15, "S": 10, "R": 7, "E": 5, "A": 5}},

        # 법 (10개)
        {"title": "변호사", "category": "LAW", "riasec": {"E": 18, "I": 16, "S": 12, "C": 10, "A": 6, "R": 8}},
        {"title": "판사", "category": "LAW", "riasec": {"I": 20, "C": 18, "E": 12, "S": 10, "R": 5, "A": 5}},
        {"title": "검사", "category": "LAW", "riasec": {"I": 19, "E": 16, "C": 12, "S": 10, "R": 6, "A": 5}},
        {"title": "법무사", "category": "LAW", "riasec": {"C": 18, "I": 15, "E": 12, "S": 10, "R": 5, "A": 5}},
        {"title": "변리사", "category": "LAW", "riasec": {"I": 19, "E": 15, "C": 13, "S": 8, "R": 7, "A": 8}},
        {"title": "법률사무원", "category": "LAW", "riasec": {"C": 20, "I": 14, "E": 10, "S": 8, "R": 4, "A": 4}},
        {"title": "공증인", "category": "LAW", "riasec": {"C": 19, "I": 15, "E": 12, "S": 8, "R": 4, "A": 2}},
        {"title": "법률고문", "category": "LAW", "riasec": {"E": 18, "I": 16, "C": 12, "S": 10, "R": 4, "A": 4}},
        {"title": "법률연구원", "category": "LAW", "riasec": {"I": 20, "C": 16, "E": 10, "S": 8, "R": 4, "A": 2}},
        {"title": "법원사무관", "category": "LAW", "riasec": {"C": 20, "I": 12, "E": 10, "S": 10, "R": 4, "A": 4}},

        # 금융 (12개)
        {"title": "은행원", "category": "FINANCE", "riasec": {"C": 18, "E": 15, "S": 12, "I": 8, "R": 4, "A": 3}},
        {"title": "공인회계사", "category": "FINANCE", "riasec": {"I": 19, "C": 18, "E": 12, "S": 8, "R": 3, "A": 0}},
        {"title": "세무사", "category": "FINANCE", "riasec": {"I": 18, "C": 17, "E": 12, "S": 8, "R": 3, "A": 2}},
        {"title": "투자은행가", "category": "FINANCE", "riasec": {"E": 20, "I": 17, "C": 12, "S": 8, "R": 3, "A": 0}},
        {"title": "재무분석가", "category": "FINANCE", "riasec": {"I": 20, "E": 16, "C": 14, "S": 6, "R": 2, "A": 2}},
        {"title": "보험계리사", "category": "FINANCE", "riasec": {"I": 20, "C": 18, "E": 10, "S": 6, "R": 4, "A": 2}},
        {"title": "자산관리사", "category": "FINANCE", "riasec": {"E": 19, "I": 15, "S": 12, "C": 10, "R": 2, "A": 2}},
        {"title": "신용분석가", "category": "FINANCE", "riasec": {"I": 19, "C": 16, "E": 12, "S": 8, "R": 3, "A": 2}},
        {"title": "외환딜러", "category": "FINANCE", "riasec": {"E": 20, "I": 16, "C": 12, "S": 6, "R": 4, "A": 2}},
        {"title": "금융컨설턴트", "category": "FINANCE", "riasec": {"E": 19, "S": 15, "I": 12, "C": 10, "R": 2, "A": 2}},
        {"title": "부동산평가사", "category": "FINANCE", "riasec": {"I": 17, "C": 16, "E": 12, "S": 10, "R": 3, "A": 2}},
        {"title": "금융기획자", "category": "FINANCE", "riasec": {"E": 18, "I": 15, "C": 14, "S": 8, "R": 3, "A": 2}},

        # 기술 (20개)
        {"title": "소프트웨어 개발자", "category": "TECHNOLOGY", "riasec": {"I": 20, "R": 12, "C": 10, "E": 8, "A": 8, "S": 2}},
        {"title": "데이터 분석가", "category": "TECHNOLOGY", "riasec": {"I": 22, "C": 14, "E": 8, "R": 6, "A": 5, "S": 5}},
        {"title": "데이터 사이언티스트", "category": "TECHNOLOGY", "riasec": {"I": 23, "C": 12, "E": 8, "R": 5, "A": 4, "S": 8}},
        {"title": "AI 엔지니어", "category": "TECHNOLOGY", "riasec": {"I": 22, "R": 12, "C": 10, "E": 8, "A": 6, "S": 2}},
        {"title": "웹 개발자", "category": "TECHNOLOGY", "riasec": {"I": 18, "A": 12, "R": 10, "C": 10, "E": 8, "S": 2}},
        {"title": "모바일 앱 개발자", "category": "TECHNOLOGY", "riasec": {"I": 19, "A": 13, "R": 10, "C": 9, "E": 7, "S": 2}},
        {"title": "시스템 엔지니어", "category": "TECHNOLOGY", "riasec": {"I": 19, "R": 14, "C": 12, "E": 8, "A": 4, "S": 3}},
        {"title": "네트워크 엔지니어", "category": "TECHNOLOGY", "riasec": {"I": 18, "R": 15, "C": 12, "E": 8, "A": 4, "S": 3}},
        {"title": "보안 전문가", "category": "TECHNOLOGY", "riasec": {"I": 21, "C": 14, "R": 10, "E": 8, "A": 4, "S": 3}},
        {"title": "클라우드 아키텍트", "category": "TECHNOLOGY", "riasec": {"I": 20, "E": 14, "C": 12, "R": 10, "A": 2, "S": 2}},
        {"title": "DevOps 엔지니어", "category": "TECHNOLOGY", "riasec": {"I": 19, "R": 14, "C": 13, "E": 8, "A": 4, "S": 2}},
        {"title": "QA 엔지니어", "category": "TECHNOLOGY", "riasec": {"I": 18, "C": 16, "R": 10, "E": 6, "A": 5, "S": 5}},
        {"title": "프로덕트 매니저", "category": "TECHNOLOGY", "riasec": {"E": 19, "I": 15, "S": 12, "C": 10, "A": 6, "R": 8}},
        {"title": "기술 컨설턴트", "category": "TECHNOLOGY", "riasec": {"E": 18, "I": 16, "S": 14, "C": 8, "A": 2, "R": 2}},
        {"title": "IT 프로젝트 매니저", "category": "TECHNOLOGY", "riasec": {"E": 19, "C": 15, "S": 12, "I": 10, "R": 2, "A": 2}},
        {"title": "UI/UX 디자이너", "category": "TECHNOLOGY", "riasec": {"A": 20, "I": 14, "S": 12, "E": 8, "C": 4, "R": 2}},
        {"title": "게임 개발자", "category": "TECHNOLOGY", "riasec": {"A": 19, "I": 17, "R": 10, "E": 8, "C": 4, "S": 2}},
        {"title": "블록체인 개발자", "category": "TECHNOLOGY", "riasec": {"I": 21, "R": 12, "C": 10, "E": 9, "A": 5, "S": 3}},
        {"title": "임베디드 개발자", "category": "TECHNOLOGY", "riasec": {"I": 20, "R": 16, "C": 12, "E": 6, "A": 4, "S": 2}},
        {"title": "빅데이터 엔지니어", "category": "TECHNOLOGY", "riasec": {"I": 22, "C": 14, "R": 10, "E": 8, "A": 4, "S": 2}},

        # 디자인 (10개)
        {"title": "그래픽 디자이너", "category": "DESIGN", "riasec": {"A": 22, "I": 12, "E": 10, "S": 8, "C": 4, "R": 4}},
        {"title": "웹 디자이너", "category": "DESIGN", "riasec": {"A": 21, "I": 14, "E": 10, "S": 8, "C": 5, "R": 2}},
        {"title": "산업 디자이너", "category": "DESIGN", "riasec": {"A": 20, "I": 15, "R": 12, "E": 10, "C": 3, "S": 0}},
        {"title": "패션 디자이너", "category": "DESIGN", "riasec": {"A": 23, "E": 14, "I": 10, "S": 8, "C": 3, "R": 2}},
        {"title": "인테리어 디자이너", "category": "DESIGN", "riasec": {"A": 20, "I": 14, "R": 12, "E": 10, "S": 4, "C": 0}},
        {"title": "영상 편집자", "category": "DESIGN", "riasec": {"A": 21, "I": 13, "E": 10, "C": 8, "S": 5, "R": 3}},
        {"title": "애니메이션 제작자", "category": "DESIGN", "riasec": {"A": 22, "I": 14, "E": 10, "C": 6, "S": 5, "R": 3}},
        {"title": "일러스트레이터", "category": "DESIGN", "riasec": {"A": 24, "I": 12, "E": 10, "S": 6, "C": 4, "R": 4}},
        {"title": "브랜드 디자이너", "category": "DESIGN", "riasec": {"A": 20, "E": 16, "I": 12, "S": 8, "C": 4, "R": 0}},
        {"title": "광고 디자이너", "category": "DESIGN", "riasec": {"A": 21, "E": 15, "I": 12, "S": 10, "C": 2, "R": 0}},

        # 교육 (12개)
        {"title": "교사", "category": "EDUCATION", "riasec": {"S": 22, "I": 14, "C": 12, "E": 8, "A": 4, "R": 0}},
        {"title": "대학교수", "category": "EDUCATION", "riasec": {"I": 21, "S": 18, "E": 10, "C": 8, "A": 3, "R": 0}},
        {"title": "강사", "category": "EDUCATION", "riasec": {"S": 21, "E": 15, "I": 12, "C": 8, "A": 4, "R": 0}},
        {"title": "교육컨설턴트", "category": "EDUCATION", "riasec": {"E": 19, "S": 18, "I": 12, "C": 8, "A": 3, "R": 0}},
        {"title": "유치원 교사", "category": "EDUCATION", "riasec": {"S": 24, "A": 12, "C": 10, "E": 6, "I": 6, "R": 2}},
        {"title": "특수교사", "category": "EDUCATION", "riasec": {"S": 23, "I": 14, "C": 10, "E": 6, "A": 5, "R": 2}},
        {"title": "평생교육사", "category": "EDUCATION", "riasec": {"S": 20, "E": 15, "I": 12, "C": 10, "A": 3, "R": 0}},
        {"title": "교육연구원", "category": "EDUCATION", "riasec": {"I": 21, "S": 16, "C": 12, "E": 8, "A": 2, "R": 1}},
        {"title": "학원 강사", "category": "EDUCATION", "riasec": {"S": 20, "E": 16, "I": 14, "C": 8, "A": 2, "R": 0}},
        {"title": "온라인 강사", "category": "EDUCATION", "riasec": {"S": 19, "E": 17, "I": 12, "A": 10, "C": 2, "R": 0}},
        {"title": "교육기획자", "category": "EDUCATION", "riasec": {"E": 19, "I": 15, "S": 14, "C": 10, "A": 2, "R": 0}},
        {"title": "교육행정가", "category": "EDUCATION", "riasec": {"C": 20, "E": 16, "S": 12, "I": 10, "A": 2, "R": 0}},

        # 연구 (10개)
        {"title": "연구원", "category": "RESEARCH", "riasec": {"I": 24, "C": 14, "E": 8, "S": 6, "A": 4, "R": 4}},
        {"title": "과학자", "category": "RESEARCH", "riasec": {"I": 25, "R": 12, "C": 10, "E": 6, "A": 4, "S": 3}},
        {"title": "연구개발원", "category": "RESEARCH", "riasec": {"I": 23, "R": 14, "C": 12, "E": 9, "A": 2, "S": 0}},
        {"title": "데이터 연구원", "category": "RESEARCH", "riasec": {"I": 24, "C": 16, "E": 8, "R": 6, "A": 4, "S": 2}},
        {"title": "생명과학 연구원", "category": "RESEARCH", "riasec": {"I": 25, "R": 12, "C": 11, "E": 6, "A": 3, "S": 3}},
        {"title": "화학 연구원", "category": "RESEARCH", "riasec": {"I": 25, "R": 14, "C": 10, "E": 6, "A": 2, "S": 2}},
        {"title": "물리학 연구원", "category": "RESEARCH", "riasec": {"I": 26, "R": 12, "C": 10, "E": 5, "A": 4, "S": 1}},
        {"title": "사회과학 연구원", "category": "RESEARCH", "riasec": {"I": 23, "S": 14, "C": 12, "E": 8, "A": 4, "R": 1}},
        {"title": "경제학 연구원", "category": "RESEARCH", "riasec": {"I": 24, "E": 14, "C": 12, "S": 6, "A": 2, "R": 0}},
        {"title": "통계학자", "category": "RESEARCH", "riasec": {"I": 25, "C": 18, "E": 8, "S": 5, "A": 3, "R": 1}},

        # 행정 (10개)
        {"title": "공무원", "category": "ADMINISTRATION", "riasec": {"C": 22, "S": 14, "E": 10, "I": 10, "A": 2, "R": 2}},
        {"title": "행정사", "category": "ADMINISTRATION", "riasec": {"C": 21, "E": 14, "S": 12, "I": 9, "A": 2, "R": 2}},
        {"title": "사무직", "category": "ADMINISTRATION", "riasec": {"C": 23, "S": 12, "E": 10, "I": 8, "A": 4, "R": 3}},
        {"title": "인사담당자", "category": "ADMINISTRATION", "riasec": {"C": 20, "S": 18, "E": 12, "I": 8, "A": 2, "R": 0}},
        {"title": "총무", "category": "ADMINISTRATION", "riasec": {"C": 22, "E": 14, "S": 12, "I": 8, "A": 2, "R": 2}},
        {"title": "회계사무원", "category": "ADMINISTRATION", "riasec": {"C": 24, "I": 14, "E": 8, "S": 6, "A": 4, "R": 4}},
        {"title": "비서", "category": "ADMINISTRATION", "riasec": {"C": 23, "S": 16, "E": 12, "I": 5, "A": 2, "R": 2}},
        {"title": "문서관리사", "category": "ADMINISTRATION", "riasec": {"C": 24, "I": 12, "S": 10, "E": 8, "A": 2, "R": 4}},
        {"title": "기획자", "category": "ADMINISTRATION", "riasec": {"E": 18, "I": 16, "C": 14, "S": 10, "A": 2, "R": 0}},
        {"title": "정책연구원", "category": "ADMINISTRATION", "riasec": {"I": 20, "C": 18, "E": 12, "S": 8, "A": 2, "R": 0}},

        # 영업 (12개)
        {"title": "영업사원", "category": "SALES", "riasec": {"E": 22, "S": 18, "C": 10, "I": 6, "A": 2, "R": 2}},
        {"title": "세일즈 매니저", "category": "SALES", "riasec": {"E": 24, "S": 16, "C": 8, "I": 8, "A": 2, "R": 2}},
        {"title": "영업대표", "category": "SALES", "riasec": {"E": 25, "S": 15, "C": 8, "I": 6, "A": 4, "R": 2}},
        {"title": "마케터", "category": "SALES", "riasec": {"E": 21, "A": 14, "I": 12, "S": 12, "C": 9, "R": 0}},
        {"title": "광고기획자", "category": "SALES", "riasec": {"E": 20, "A": 18, "I": 12, "S": 10, "C": 8, "R": 2}},
        {"title": "브랜드 매니저", "category": "SALES", "riasec": {"E": 22, "A": 16, "I": 12, "S": 12, "C": 6, "R": 2}},
        {"title": "영업 컨설턴트", "category": "SALES", "riasec": {"E": 21, "S": 18, "I": 12, "C": 7, "A": 2, "R": 0}},
        {"title": "B2B 영업", "category": "SALES", "riasec": {"E": 23, "I": 14, "S": 12, "C": 9, "A": 2, "R": 0}},
        {"title": "B2C 영업", "category": "SALES", "riasec": {"E": 22, "S": 20, "A": 10, "C": 6, "I": 2, "R": 0}},
        {"title": "해외영업", "category": "SALES", "riasec": {"E": 23, "S": 16, "I": 12, "C": 7, "A": 2, "R": 0}},
        {"title": "영업기획자", "category": "SALES", "riasec": {"E": 21, "I": 16, "C": 14, "S": 9, "A": 2, "R": 0}},
        {"title": "고객관리", "category": "SALES", "riasec": {"S": 20, "E": 18, "C": 14, "I": 6, "A": 2, "R": 0}},

        # 서비스 (12개)
        {"title": "요리사", "category": "SERVICE", "riasec": {"R": 18, "A": 16, "E": 12, "S": 10, "C": 4, "I": 0}},
        {"title": "바리스타", "category": "SERVICE", "riasec": {"S": 18, "A": 14, "R": 12, "E": 10, "C": 4, "I": 2}},
        {"title": "호텔리어", "category": "SERVICE", "riasec": {"S": 20, "E": 16, "C": 12, "A": 8, "I": 2, "R": 2}},
        {"title": "여행가이드", "category": "SERVICE", "riasec": {"S": 22, "E": 16, "A": 12, "C": 6, "I": 2, "R": 2}},
        {"title": "이벤트 기획자", "category": "SERVICE", "riasec": {"E": 20, "A": 16, "S": 14, "C": 8, "I": 6, "R": 2}},
        {"title": "웨딩플래너", "category": "SERVICE", "riasec": {"E": 19, "A": 17, "S": 16, "C": 6, "I": 2, "R": 0}},
        {"title": "미용사", "category": "SERVICE", "riasec": {"A": 20, "S": 18, "E": 12, "R": 6, "C": 2, "I": 2}},
        {"title": "피트니스 트레이너", "category": "SERVICE", "riasec": {"S": 20, "R": 16, "E": 12, "I": 8, "C": 2, "A": 2}},
        {"title": "요가 강사", "category": "SERVICE", "riasec": {"S": 22, "A": 14, "E": 10, "I": 6, "C": 4, "R": 2}},
        {"title": "심리상담사", "category": "SERVICE", "riasec": {"S": 24, "I": 16, "C": 8, "E": 6, "A": 4, "R": 2}},
        {"title": "사회복지사", "category": "SERVICE", "riasec": {"S": 25, "I": 12, "C": 10, "E": 8, "A": 4, "R": 1}},
        {"title": "고객서비스", "category": "SERVICE", "riasec": {"S": 22, "C": 16, "E": 10, "I": 6, "A": 4, "R": 2}},
    ]

    # 스킬 매핑 (간단한 예시)
    skill_mapping = {
        "의사": ["의사면허", "커뮤니케이션"],
        "데이터 분석가": ["Python", "SQL", "데이터 분석"],
        "소프트웨어 개발자": ["Python", "Java", "JavaScript", "웹 개발"],
        "공인회계사": ["공인회계사", "커뮤니케이션"],
        "변리사": ["변리사", "커뮤니케이션"],
    }

    for job_data in jobs_data:
        job = Job(
            job_title=job_data["title"],
            category=job_data["category"],
            description=f"{job_data['title']}에 대한 설명입니다.",
            difficulty_level="MEDIUM",
            avg_preparation_time=24,  # 기본 24개월
            education_requirement="BACHELOR",
            license_required=None
        )
        db.add(job)
        db.flush()

        # RIASEC 점수 저장
        riasec = JobRIASEC(
            job_id=job.id,
            R=job_data["riasec"].get("R", 0),
            I=job_data["riasec"].get("I", 0),
            A=job_data["riasec"].get("A", 0),
            S=job_data["riasec"].get("S", 0),
            E=job_data["riasec"].get("E", 0),
            C=job_data["riasec"].get("C", 0),
        )
        db.add(riasec)

        # 스킬 연결 (간단한 예시)
        if job_data["title"] in skill_mapping:
            skills = db.query(Skill).filter(
                Skill.skill_name.in_(skill_mapping[job_data["title"]])
            ).all()
            for skill in skills:
                job_skill = JobSkill(
                    job_id=job.id,
                    skill_id=skill.id,
                    importance_level="IMPORTANT"
                )
                db.add(job_skill)

        # 커리어 패스 생성 (기본 6단계)
        career_steps = [
            {"order": 1, "title": "기초 학습", "time": 3},
            {"order": 2, "title": "전문 지식 습득", "time": 6},
            {"order": 3, "title": "실무 경험", "time": 6},
            {"order": 4, "title": "프로젝트 수행", "time": 6},
            {"order": 5, "title": "포트폴리오 구축", "time": 2},
            {"order": 6, "title": "취업 지원", "time": 1},
        ]
        for step in career_steps:
            career_path = CareerPath(
                job_id=job.id,
                step_order=step["order"],
                step_title=step["title"],
                estimated_time=step["time"]
            )
            db.add(career_path)

    db.commit()
    print(f"[OK] {len(jobs_data)}개 직업 생성 완료")


def main():
    """Seed 데이터 로드 메인 함수"""
    db = SessionLocal()
    try:
        print("Seed 데이터 로드를 시작합니다...")
        create_survey_questions(db)
        create_skills(db)
        create_jobs(db)
        print("\n[OK] 모든 Seed 데이터 로드 완료!")
    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

