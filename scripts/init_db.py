"""
데이터베이스 초기화 스크립트

1. 데이터베이스 테이블 생성
2. 초기 마이그레이션 생성 (선택사항)
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.models import *  # 모든 모델 import

def init_database():
    """데이터베이스 테이블 생성"""
    print("데이터베이스 테이블을 생성합니다...")
    Base.metadata.create_all(bind=engine)
    print("[OK] 데이터베이스 테이블 생성 완료")
    print("\n다음 단계:")
    print("1. python scripts/load_seed_data.py - Seed 데이터 로드")

if __name__ == "__main__":
    init_database()

