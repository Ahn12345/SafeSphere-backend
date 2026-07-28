from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# ---- Zone ----
class ZoneBase(BaseModel):
    name: str
    building: Optional[str] = None
    zone_type: Optional[str] = None


class ZoneCreate(ZoneBase):
    pass


class ZoneOut(ZoneBase):
    id: int
    risk_level: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---- Sensor ----
class SensorBase(BaseModel):
    zone_id: int
    sensor_type: str
    label: Optional[str] = None


class SensorCreate(SensorBase):
    pass


class SensorOut(SensorBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---- SensorReading ----
class SensorReadingCreate(BaseModel):
    value: float
    unit: Optional[str] = None


class SensorReadingOut(SensorReadingCreate):
    id: int
    sensor_id: int
    recorded_at: datetime

    class Config:
        from_attributes = True


# ---- Alert ----
class AlertOut(BaseModel):
    id: int
    zone_id: int
    sensor_id: Optional[int]
    severity: str
    message: str
    status: str
    created_at: datetime
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True


class AlertUpdate(BaseModel):
    status: str  # acknowledged / resolved


# ---- AI Detection (stub) ----
class DetectionRequest(BaseModel):
    sensor_id: int
    value: float
    unit: Optional[str] = None


class DetectionResult(BaseModel):
    """
    AI 이상 감지 결과. 지금은 항상 더미 값을 반환하는 스텁이며,
    실제 판단 로직(임계값/모델 추론)은 추후 이 스키마 형태를 유지한 채 채워 넣으면 됨.
    """
    sensor_id: int
    is_anomaly: bool
    risk_score: float          # 0.0 ~ 1.0
    reason: str
