# SafeSphere Backend (FastAPI 뼈대)

공장 내/외부 재난 대응·작업자 안전 모니터링 시스템의 백엔드 스캐폴드입니다.
AI 이상 감지 로직은 아직 더미(스텁) 상태이며, 구조만 잡혀 있습니다.

## 구조

```
app/
  main.py            # FastAPI 앱 진입점, 라우터 등록, CORS 설정
  config.py          # .env 기반 설정값 로드
  database.py        # SQLAlchemy 엔진/세션
  models.py          # DB 모델 (Zone, Sensor, SensorReading, Alert)
  schemas.py         # Pydantic 요청/응답 스키마
  routers/
    zones.py         # 구역 CRUD
    sensors.py        # 센서 CRUD + 측정값 수신
    alerts.py          # 알림 조회/상태 변경
    ai_detection.py   # AI 감지 스텁 + 실시간 웹소켓 알림 채널
```

## 실행 방법

```bash
pip install -r requirements.txt
cp .env.example .env   # DATABASE_URL을 팀원분 DB 정보로 수정
uvicorn app.main:app --reload
```

- API 문서: http://localhost:8000/docs (FastAPI 자동 생성 Swagger UI)
- Health check: `GET /health`

## 현재 뼈대로 되는 것

- 구역(Zone) / 센서(Sensor) 등록 및 조회
- 센서 측정값(`POST /sensors/{id}/readings`) 저장 → AI 감지 스텁 호출까지 연결됨
- `POST /ai/detect` : 감지 로직 단독 테스트용
- `WS /ai/ws/alerts` : 프론트가 연결해두면 실시간 알림을 받을 수 있는 웹소켓 채널 (아직 브로드캐스트 트리거는 미연결)
- 알림(Alert) 조회 및 상태 변경(`open` → `acknowledged` / `resolved`)

## TODO (다음 단계)

1. `app/routers/ai_detection.py`의 `run_detection_stub()`에 실제 판단 로직 작성
   - 센서 타입별 임계값 비교부터 시작해도 됨 (예: 화학물질 ppm 초과 시 anomaly)
2. 이상 감지 시 `Alert` DB 레코드 생성 + `manager.broadcast()`로 프론트에 실시간 푸시 연결
3. `.env`의 `DATABASE_URL`을 팀원분이 구성한 실제 SQL DB 접속 정보로 교체
4. 배포 시 Docker Compose에 이 컨테이너 + 프론트 컨테이너 + Nginx(또는 Caddy) 리버스 프록시 구성으로 연결
