from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Vercel 환경에서는 /tmp 디렉토리 사용 (읽기/쓰기 가능)
if os.getenv("VERCEL") or os.getenv("VERCEL_ENV"):
    # /tmp 디렉토리 확인 및 생성
    tmp_dir = "/tmp"
    if not os.path.exists(tmp_dir):
        try:
            os.makedirs(tmp_dir, exist_ok=True)
        except:
            pass
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{tmp_dir}/careermap.db")
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./careermap.db")

# SQLite 연결 옵션 (Vercel 환경 대응)
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Pool 설정 (Vercel serverless 환경 대응)
engine = create_engine(
    DATABASE_URL, 
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=300
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

