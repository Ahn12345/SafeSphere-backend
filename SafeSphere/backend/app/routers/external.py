import httpx
from fastapi import APIRouter, HTTPException, Query

from app.services import external_apis

router = APIRouter(prefix="/external", tags=["external_data"])


@router.get("/disaster-texts")
async def disaster_texts(
    region_name: str = Query(..., description="지역명 (예: 충청북도)"),
    start_date: str = Query(..., description="조회시작일자 YYYYMMDD"),
):
    """① 긴급재난문자 프록시. 서비스키 미설정 시 502로 명확히 알려줌."""
    try:
        return await external_apis.get_disaster_texts(region_name, start_date)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"공공데이터 API 오류: {e}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"공공데이터 API 연결 실패 (서비스키 미설정일 수 있음): {e}")


@router.get("/earthquake-shelters")
async def earthquake_shelters(sido_name: str | None = Query(None, description="시도명 (예: 충청북도)")):
    """② 지진 옥외대피장소 프록시."""
    try:
        return await external_apis.get_earthquake_shelters(sido_name)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"공공데이터 API 오류: {e}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"공공데이터 API 연결 실패 (서비스키 미설정일 수 있음): {e}")


@router.get("/chemical-shelters")
async def chemical_shelters(
    sido_name: str | None = Query(None, description="시도명 (예: 충청북도)"),
    sigungu_name: str | None = Query(None, description="시군구명 (예: 청주시)"),
):
    """③ 화학사고 대피장소 프록시. SafeSphere 핵심 시나리오용."""
    try:
        return await external_apis.get_chemical_shelters(sido_name, sigungu_name)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"공공데이터 API 오류: {e}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"공공데이터 API 연결 실패 (서비스키 미설정일 수 있음): {e}")
