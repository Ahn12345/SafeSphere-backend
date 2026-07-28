from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    앱 환경설정. .env 파일에서 값을 읽어옵니다.
    DATABASE_URL은 팀원분이 SQL DB(PostgreSQL 기준)를 구성한 뒤
    실제 접속 정보로 채워주세요.
    """
    database_url: str = "postgresql://safesphere_user:changeme@localhost:5432/safesphere"
    frontend_origin: str = "http://localhost:5173"

    class Config:
        env_file = ".env"


settings = Settings()
