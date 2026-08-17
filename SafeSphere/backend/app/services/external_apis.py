"""
공공데이터포털(data.go.kr) 연동 모듈.

지금은 서비스키가 없는 상태라 실제 호출은 실패한다. 구조만 잡아둔 상태이며,
아래 3개 함수의 BASE_URL / 파라미터명은 활용신청 승인 후 각 API 상세페이지의
Swagger 문서를 보고 정확히 맞춰야 한다 (TODO 표시된 부분).

- get_disaster_texts()      : ① 행정안전부_긴급재난문자 (개인정보 불필요, 지역명+조회시작일자만 사용)
- get_earthquake_shelters() : ② 지진 옥외대피장소 (전국 단위, 시도명으로 필터링)
- get_chemical_shelters()   : ③ 화학사고 대피장소 (시도/시군구, 위경도/수용인원 포함)
"""

import httpx

from app.config import settings

# TODO: 활용신청 승인 후 Swagger 문서에서 정확한 요청주소로 교체
DISASTER_TEXT_BASE_URL = "https://www.safetydata.go.kr/V2/api/DSSP-IF-00247"
EARTHQUAKE_SHELTER_BASE_URL = "https://www.safetydata.go.kr/V2/api/DSSP-IF-10944"
CHEMICAL_SHELTER_BASE_URL = "https://www.safetydata.go.kr/V2/api/DSSP-IF-10941"

TIMEOUT = 10.0


async def get_disaster_texts(region_name: str, start_date: str) -> dict:
    """
    ① 긴급재난문자 조회.
    region_name: 지역명 (예: "충청북도")
    start_date: 조회시작일자 (예: "20260101")

    TODO: 실제 파라미터명(요청변수)을 Swagger 문서 기준으로 확인 후 아래 params 수정.
    현재는 추정치이며 서비스키 없이는 401/오류가 정상이다.
    """
    params = {
        "serviceKey": settings.disaster_text_api_key or settings.public_data_service_key,
        "locationName": region_name,
        "srchFrom": start_date,
        "pageNo": 1,
        "numOfRows": 20,
        "returnType": "json",
    }
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(DISASTER_TEXT_BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


async def get_earthquake_shelters(sido_name: str | None = None) -> dict:
    """
    ② 지진 옥외대피장소 조회 (전국 단위 데이터, 시도명으로 필터링 가능).
    sido_name: 예: "충청북도" (생략 시 전국 조회 - API가 지원하는 경우)

    TODO: 실제 파라미터명 확인 필요.
    """
    params = {
        "serviceKey": settings.earthquake_shelter_api_key or settings.public_data_service_key,
        "pageNo": 1,
        "numOfRows": 50,
        "returnType": "json",
    }
    if sido_name:
        params["sidoName"] = sido_name

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(EARTHQUAKE_SHELTER_BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


async def get_chemical_shelters(sido_name: str | None = None, sigungu_name: str | None = None) -> dict:
    """
    ③ 화학사고 대피장소 조회 (시도/시군구명, 위경도, 수용인원 등 포함).
    SafeSphere의 핵심 시나리오(화학물질 유출 시 대피 안내)에 직접 쓰이는 API.

    TODO: 실제 파라미터명 확인 필요.
    """
    params = {
        "serviceKey": settings.chemical_shelter_api_key or settings.public_data_service_key,
        "pageNo": 1,
        "numOfRows": 50,
        "returnType": "json",
    }
    if sido_name:
        params["sidoName"] = sido_name
    if sigungu_name:
        params["sigunguName"] = sigungu_name

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(CHEMICAL_SHELTER_BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
