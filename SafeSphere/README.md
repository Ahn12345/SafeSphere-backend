# SafeSphere Backend

공장 내·외부 재난 대응 및 작업자 안전 모니터링 시스템의 백엔드 (제13회 전국 ICT융합 공모전 출품작)

FastAPI + SQLAlchemy 백엔드를 Docker Compose + Nginx로 띄울 수 있게 구성했습니다.
프론트엔드(Next.js)는 별도 저장소/배포(Vercel 등)로 관리합니다.

## 구조

```
SafeSphere/
  backend/      # FastAPI + SQLAlchemy
  nginx/
    nginx.conf  # 백엔드 앞단 리버스 프록시 (도메인/TLS 종료용)
  docker-compose.yml
```

## Docker로 실행하기

```bash
cp backend/.env.example backend/.env
# backend/.env 열어서 DATABASE_URL, FRONTEND_ORIGIN 등 실제 값으로 수정

docker compose up --build
```

- `http://localhost/health` → 백엔드 health check
- `http://localhost/zones`, `/sensors`, `/alerts`, `/ai/detect`, `/external/...` → API
- `ws://localhost/ai/ws/alerts` → 실시간 알림 웹소켓

## Docker 없이 로컬 개발

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload   # localhost:8000
```

프론트엔드가 별도 포트(예: localhost:3000)에서 돈다면, `backend/.env`의
`FRONTEND_ORIGIN`을 그 주소로 맞춰야 CORS 에러가 안 납니다.

## 실제 도메인 배포 시

1. 도메인 구매 후 Cloudflare에 연결
2. 서버(VM 등)에 이 저장소 clone → `docker compose up --build -d`
3. nginx가 80번 포트를 물고 있으므로, 앞단에 Caddy나 별도 TLS 종료 프록시를 하나 더 두거나
   `nginx/nginx.conf`를 Caddy 설정으로 교체해서 자동 TLS 발급을 받으면 됩니다.
4. 프론트엔드는 이 백엔드 도메인을 `NEXT_PUBLIC_API_URL`로 가리키도록 설정

## TODO

- [ ] `backend/app/services/external_apis.py`의 공공데이터 API URL/파라미터 확정 (서비스키 발급 후)
- [ ] `backend/app/routers/ai_detection.py`의 `run_detection_stub()` 실제 로직 구현
- [ ] `backend/.env`에 실제 SQL DB 접속 정보 반영
- [ ] 실 도메인 + TLS 인증서 적용
