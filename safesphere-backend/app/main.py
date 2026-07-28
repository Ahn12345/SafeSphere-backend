from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import zones, sensors, alerts, ai_detection

# 개발 초기 단계: 테이블이 없으면 생성 (운영 단계에서는 Alembic 마이그레이션으로 전환 권장)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SafeSphere API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(zones.router)
app.include_router(sensors.router)
app.include_router(alerts.router)
app.include_router(ai_detection.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
