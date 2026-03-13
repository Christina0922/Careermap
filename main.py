from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.api.routes import router
from app.database import engine, Base
import os

# 데이터베이스 테이블 생성 (Vercel에서는 지연 초기화)
try:
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

# 정적 파일 제공
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def root():
    import os
    html_path = os.path.join("static", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return """
        <html>
        <body>
            <h1>CareerMap API</h1>
            <p>Version: 1.0.0</p>
            <p><a href="/docs">API Documentation</a></p>
        </body>
        </html>
        """


@app.get("/health")
def health_check():
    return {"status": "healthy"}

