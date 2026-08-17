from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    앱 환경설정. .env 파일에서 값을 읽어옵니다.
    DATABASE_URL은 팀원분이 SQL DB(PostgreSQL 기준)를 구성한 뒤
    실제 접속 정보로 채워주세요.
    """
    database_url: str = "postgresql://safesphere_user:changeme@localhost:5432/safesphere"
    frontend_origin: str = "http://localhost:5173"

    # 공공데이터포털(data.go.kr) 서비스키. 각 API별로 활용신청 승인 후 발급받은 키를 넣는다.
    # 세 API가 보통 같은 계정으로 발급되면 키가 동일할 수 있지만, 다르면 아래처럼 분리해서 관리.
    public_data_service_key: str = ""
    disaster_text_api_key: str = ""      # ① 행정안전부_긴급재난문자
    earthquake_shelter_api_key: str = ""  # ② 지진 옥외대피장소
    chemical_shelter_api_key: str = ""    # ③ 화학사고 대피장소

    class Config:
        env_file = ".env"


settings = Settings()
