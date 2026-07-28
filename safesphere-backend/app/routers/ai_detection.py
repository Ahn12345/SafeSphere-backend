from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app import schemas

router = APIRouter(prefix="/ai", tags=["ai_detection"])


# ---- 실시간 웹 알림용 WebSocket 연결 관리 ----
class ConnectionManager:
    """프론트엔드(웹)에 연결된 클라이언트 목록을 관리하고 알림을 브로드캐스트"""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


def run_detection_stub(request: schemas.DetectionRequest) -> schemas.DetectionResult:
    """
    AI 이상 감지 로직 뼈대(스텁).

    TODO(승민): 여기에 실제 판단 로직을 채워 넣을 것.
      - 센서 타입별 임계값 비교, 혹은 학습된 모델 추론 결과 사용
      - is_anomaly=True 판단 시 Alert 레코드 생성 + manager.broadcast()로 프론트에 실시간 알림
      - 현재는 항상 정상(false)을 반환하는 더미 상태
    """
    return schemas.DetectionResult(
        sensor_id=request.sensor_id,
        is_anomaly=False,
        risk_score=0.0,
        reason="stub: 로직 미구현 (항상 정상 반환)",
    )


@router.post("/detect", response_model=schemas.DetectionResult)
def detect(request: schemas.DetectionRequest):
    """단발성 감지 요청 테스트용 엔드포인트 (프론트에서 직접 호출해 뼈대 동작 확인 가능)"""
    return run_detection_stub(request)


@router.websocket("/ws/alerts")
async def alerts_websocket(websocket: WebSocket):
    """
    프론트엔드가 연결해두면 이상 감지 시 실시간으로 알림을 받을 수 있는 채널.
    TODO: run_detection_stub에서 이상 감지 시 manager.broadcast(...) 호출하도록 연결.
    """
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # 연결 유지 (프론트에서 딱히 안 보내도 무방)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
