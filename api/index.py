"""
Vercel serverless function entry point for FastAPI
"""
import os
import sys

# Vercel 환경 변수 설정
os.environ.setdefault("VERCEL", "1")

def create_app():
    """앱 생성 함수 - 지연 초기화"""
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.responses import HTMLResponse
        
        app = FastAPI(
            title="CareerMap API",
            description="RIASEC 기반 직업 추천 시스템",
            version="1.0.0"
        )
        
        # CORS 설정
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # 데이터베이스 초기화 함수
        def init_database():
            try:
                from app.database import engine, Base
                Base.metadata.create_all(bind=engine)
            except Exception as e:
                print(f"Database initialization warning: {e}")
        
        # 라우터 추가 (지연 import)
        @app.on_event("startup")
        async def startup_event():
            try:
                from app.api.routes import router
                app.include_router(router)
            except Exception as e:
                print(f"Router import warning: {e}")
        
        # 라우터를 즉시 추가 (startup 이벤트는 Vercel에서 작동하지 않을 수 있음)
        try:
            from app.api.routes import router
            app.include_router(router)
        except Exception as e:
            print(f"Router import error: {e}")
        
        @app.get("/", response_class=HTMLResponse)
        def root():
            init_database()
            html_path = os.path.join("static", "index.html")
            try:
                if os.path.exists(html_path):
                    with open(html_path, "r", encoding="utf-8") as f:
                        return f.read()
            except Exception as e:
                print(f"Error reading HTML: {e}")
            
            return """
            <html>
            <head>
                <meta charset="UTF-8">
                <title>CareerMap API</title>
            </head>
            <body>
                <h1>CareerMap API</h1>
                <p>Version: 1.0.0</p>
                <p><a href="/docs">API Documentation</a></p>
                <p><a href="/health">Health Check</a></p>
            </body>
            </html>
            """
        
        @app.get("/health")
        def health_check():
            return {"status": "healthy"}
        
        return app
    
    except Exception as e:
        print(f"Error creating app: {e}")
        import traceback
        traceback.print_exc()
        raise

# 앱 생성
try:
    app = create_app()
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
except Exception as e:
    print(f"Fatal error: {e}")
    import traceback
    traceback.print_exc()
    
    # Fallback handler
    def handler(event, context):
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": f'{{"error": "Application initialization failed: {str(e)}"}}'
        }
