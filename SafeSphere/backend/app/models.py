from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship

from app.database import Base


class Zone(Base):
    """공장 내부/외부 구역 (도면 상의 구획 단위). 예: 화학 약품 저장 탱크 구역, 관리 사무실 등"""
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)          # 예: "화학 약품 저장 탱크 구역"
    building = Column(String(100), nullable=True)        # 예: "반도체 FAB", "화학공장"
    zone_type = Column(String(50), nullable=True)         # 예: indoor / outdoor
    risk_level = Column(String(20), default="normal")     # normal / caution / warning / critical
    created_at = Column(DateTime, default=datetime.utcnow)

    sensors = relationship("Sensor", back_populates="zone")
    alerts = relationship("Alert", back_populates="zone")


class Sensor(Base):
    """구역별로 설치된 센서 (화학물질 감지기, 스마트 보호구 신호 수신기 등)"""
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    sensor_type = Column(String(50), nullable=False)   # chemical_leak / temperature / ppe_signal / smoke 등
    label = Column(String(100), nullable=True)          # 예: "T-1 저장탱크 화학물질 감지기"
    status = Column(String(20), default="normal")        # normal / needs_check / fault
    created_at = Column(DateTime, default=datetime.utcnow)

    zone = relationship("Zone", back_populates="sensors")
    readings = relationship("SensorReading", back_populates="sensor")


class SensorReading(Base):
    """센서에서 들어오는 개별 측정값. AI 이상 감지 로직의 입력 데이터가 됨"""
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=True)             # 예: ppm, C, %
    recorded_at = Column(DateTime, default=datetime.utcnow)

    sensor = relationship("Sensor", back_populates="readings")


class Alert(Base):
    """AI 감지 로직이 이상을 판단했을 때 생성되는 경고. 웹으로 알림 전송의 기반 데이터"""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=True)
    severity = Column(String(20), nullable=False, default="caution")  # caution / warning / critical
    message = Column(Text, nullable=False)
    status = Column(String(20), default="open")           # open / acknowledged / resolved
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    zone = relationship("Zone", back_populates="alerts")
