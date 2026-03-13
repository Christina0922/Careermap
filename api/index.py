"""
Vercel serverless function entry point for FastAPI
"""
import sys
import os

# Vercel 환경 변수 설정
os.environ.setdefault("VERCEL", "1")

try:
    from mangum import Mangum
    from main import app
    
    # Mangum adapter for ASGI apps on Vercel
    handler = Mangum(app, lifespan="off")
except Exception as e:
    # 에러 발생 시 간단한 핸들러 반환
    def handler(event, context):
        return {
            "statusCode": 500,
            "body": f"Error initializing app: {str(e)}"
        }

