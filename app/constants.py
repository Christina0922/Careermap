"""
모든 enum과 상수를 dictionary로 관리
"""

# RIASEC 타입
RIASEC_TYPES = {
    "R": "Realistic",
    "I": "Investigative",
    "A": "Artistic",
    "S": "Social",
    "E": "Enterprising",
    "C": "Conventional"
}

# 직업 카테고리
JOB_CATEGORIES = {
    "MEDICAL": "의료",
    "LAW": "법",
    "FINANCE": "금융",
    "TECHNOLOGY": "기술",
    "DESIGN": "디자인",
    "EDUCATION": "교육",
    "RESEARCH": "연구",
    "ADMINISTRATION": "행정",
    "SALES": "영업",
    "SERVICE": "서비스"
}

# 난이도 레벨
DIFFICULTY_LEVELS = {
    "EASY": "쉬움",
    "MEDIUM": "보통",
    "HARD": "어려움",
    "VERY_HARD": "매우 어려움"
}

# 교육 요구사항
EDUCATION_REQUIREMENTS = {
    "HIGH_SCHOOL": "고등학교",
    "ASSOCIATE": "전문대학",
    "BACHELOR": "학사",
    "MASTER": "석사",
    "DOCTORATE": "박사",
    "NONE": "무관"
}

# 스킬 카테고리
SKILL_CATEGORIES = {
    "TECHNICAL": "기술적",
    "SOFT": "소프트",
    "LANGUAGE": "언어",
    "CERTIFICATION": "자격증"
}

# 중요도 레벨
IMPORTANCE_LEVELS = {
    "REQUIRED": "필수",
    "IMPORTANT": "중요",
    "PREFERRED": "선호"
}

# RIASEC 점수 가중치 (거리 계산용)
RIASEC_WEIGHT = 1.0

