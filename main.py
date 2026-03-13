from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.api.routes import router
import os

# 데이터베이스 초기화는 지연 로딩 (첫 요청 시)
def init_database():
    try:
        from app.database import engine, Base
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Database initialization warning: {e}")

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

app.include_router(router)

# 정적 파일 제공 (Vercel에서는 직접 읽기)
# app.mount("/static", StaticFiles(directory="static"), name="static")  # Vercel에서 제거


@app.get("/", response_class=HTMLResponse)
def root():
    # 데이터베이스 초기화 (첫 요청 시)
    init_database()
    
    import os
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

