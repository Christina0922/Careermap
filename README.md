# CareerMap - RIASEC 기반 직업 추천 시스템

## 개요

RIASEC 모델을 기반으로 한 직업 추천 및 전환 로드맵 시스템입니다.

## 기술 스택

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (마이그레이션)

## 설치 및 실행

1. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 편집하여 데이터베이스 연결 정보 설정
```

4. 데이터베이스 생성 및 초기화
```bash
# PostgreSQL 데이터베이스 생성
createdb careermap_db

# 방법 1: 직접 테이블 생성 (빠른 초기화)
python scripts/init_db.py

# 방법 2: Alembic 마이그레이션 사용
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

5. Seed 데이터 로드
```bash
python scripts/load_seed_data.py
```

6. 서버 실행
```bash
uvicorn main:app --reload
```

## API 엔드포인트

### 설문
- `GET /api/survey/questions` - 설문 문항 조회 (40문항)
- `POST /api/survey/submit` - 설문 제출 및 RIASEC 점수 계산

### 직업 추천
- `GET /api/jobs/recommendations?email={email}&top_n={n}` - 직업 추천 (기본 상위 10개)
- `GET /api/jobs/{job_id}` - 직업 상세 정보
- `GET /api/jobs/{job_id}/gap?user_skills={skill_ids}` - Gap 분석 (부족한 역량 분석)

### 기타
- `GET /` - API 정보
- `GET /health` - 헬스 체크
- `GET /docs` - Swagger UI 문서

## 프로젝트 구조

```
Careermap/
├── app/
│   ├── models/          # 데이터베이스 모델
│   │   ├── user.py      # 사용자, RIASEC 점수
│   │   ├── survey.py    # 설문 문항, 선택지, 답변
│   │   └── job.py       # 직업, 스킬, 커리어 패스
│   ├── schemas/         # Pydantic 스키마
│   ├── services/        # 비즈니스 로직
│   │   ├── survey_service.py
│   │   ├── recommendation_service.py  # RIASEC 추천 알고리즘
│   │   └── job_service.py
│   ├── api/             # API 라우터
│   ├── constants.py     # Enum 및 상수 정의
│   └── database.py      # 데이터베이스 연결
├── scripts/
│   ├── init_db.py       # 데이터베이스 초기화
│   ├── seed_data.py     # Seed 데이터 정의
│   └── load_seed_data.py  # Seed 데이터 로드
├── alembic/             # 마이그레이션 파일
├── main.py              # FastAPI 앱 진입점
└── requirements.txt     # Python 의존성
```

## 주요 기능

### 1. RIASEC 모델 기반 추천
- 6차원 벡터 (R, I, A, S, E, C) 기반 직업 적합도 계산
- 거리 기반 적합도 점수 (0-100)

### 2. 설문 시스템
- 40문항 객관식 설문
- 각 질문 6개 선택지 (RIASEC 타입별 점수)
- 자동 RIASEC 점수 계산

### 3. 직업 데이터
- 120개 직업 (10개 카테고리)
- 각 직업별 RIASEC 점수
- 요구 스킬 및 중요도
- 6단계 커리어 패스

### 4. Gap 분석
- 직업 요구 스킬 vs 사용자 보유 스킬 비교
- 부족한 역량 식별

## 데이터 구조

### RIASEC 타입
- **R** (Realistic): 기술/현장
- **I** (Investigative): 연구/분석
- **A** (Artistic): 창의
- **S** (Social): 사회/교육/상담
- **E** (Enterprising): 경영/리더십
- **C** (Conventional): 체계/행정

### 직업 카테고리
의료, 법, 금융, 기술, 디자인, 교육, 연구, 행정, 영업, 서비스

