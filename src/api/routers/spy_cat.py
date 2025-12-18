from fastapi import APIRouter, status

from src.api.dependencies.spy_cat import SpyCatServiceDep
from src.schemas.spy_cat import CreateSpyCatRequest, CreateSpyCatResponse, ListInfo, Info, \
                                DeleteSpyCatResponse, UpdateSpyCatRequest, UpdateSpyCatResponse

router = APIRouter()


@router.get("/")
async def select_all_spy_cats(spy_cat_service: SpyCatServiceDep) -> ListInfo: 
    return await spy_cat_service.select_all_spy_cats()


@router.get("/{spy_cat_id}")
async def select_one_spy_cat(spy_cat_id: int, spy_cat_service: SpyCatServiceDep) -> Info: 
    return await spy_cat_service.select_one_spy_cat(spy_cat_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_spy_cat(payload: CreateSpyCatRequest, spy_cat_service: SpyCatServiceDep) -> CreateSpyCatResponse: 
    return await spy_cat_service.create_spy_cat(payload)


@router.put("/{spy_cat_id}")
async def update_spy_cat(spy_cat_id: int, payload: UpdateSpyCatRequest, spy_cat_service: SpyCatServiceDep) -> UpdateSpyCatResponse: 
    return await spy_cat_service.update_spy_cat(spy_cat_id, payload)


@router.delete("/{spy_cat_id}")
async def delete_spy_cat(spy_cat_id: int, spy_cat_service: SpyCatServiceDep) -> DeleteSpyCatResponse: 
    return await spy_cat_service.delete_spy_cat(spy_cat_id)
