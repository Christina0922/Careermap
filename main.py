from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.database import engine, Base

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

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


@app.get("/")
def root():
    from fastapi.responses import FileResponse
    import os
    html_path = os.path.join("static", "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    else:
        return {
            "message": "CareerMap API",
            "version": "1.0.0",
            "docs": "/docs",
            "client": "/static/index.html"
        }


@app.get("/health")
def health_check():
    return {"status": "healthy"}

