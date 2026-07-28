from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.routers.ai_detection import run_detection_stub

router = APIRouter(prefix="/sensors", tags=["sensors"])


@router.get("", response_model=List[schemas.SensorOut])
def list_sensors(db: Session = Depends(get_db)):
    return db.query(models.Sensor).all()


@router.post("", response_model=schemas.SensorOut)
def create_sensor(sensor: schemas.SensorCreate, db: Session = Depends(get_db)):
    db_sensor = models.Sensor(**sensor.model_dump())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


@router.post("/{sensor_id}/readings", response_model=schemas.SensorReadingOut)
def add_reading(
    sensor_id: int,
    reading: schemas.SensorReadingCreate,
    db: Session = Depends(get_db),
):
    """
    센서 측정값 수신 엔드포인트.
    지금은 저장 후 AI 감지 스텁을 호출만 해두고, 실제 이상 감지 로직은
    run_detection_stub 안에 나중에 채워 넣으면 이 엔드포인트는 그대로 재사용 가능.
    """
    sensor = db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    db_reading = models.SensorReading(sensor_id=sensor_id, **reading.model_dump())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)

    # AI 감지 스텁 호출 (현재는 더미 결과만 반환, 알림 생성 로직은 TODO)
    run_detection_stub(
        schemas.DetectionRequest(
            sensor_id=sensor_id, value=reading.value, unit=reading.unit
        )
    )

    return db_reading
