from fastapi import APIRouter, status

from src.api.dependencies.mission import MissionServiceDep
from src.schemas.mission import CreateMissionRequest, CreateMissionResponse, ListInfo, Info, AssignMissionResponse, \
                                DeleteMissionResponse, UpdateMissionRequest, UpdateMissionResponse

router = APIRouter() 


@router.get("/")
async def select_all_missions(mission_service: MissionServiceDep) -> ListInfo:
    return await mission_service.select_all_missions()


@router.get("/{mission_id}")
async def select_mission(mission_id: int, mission_service: MissionServiceDep) -> Info: 
    return await mission_service.select_mission(mission_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_mission(payload: CreateMissionRequest, mission_service: MissionServiceDep) -> CreateMissionResponse: 
    return await mission_service.create_mission(payload)


@router.put("/{mission_id}/spy-cats/{spy_cat_id}")
async def assign_mission_to_spy_cat(mission_id: int, spy_cat_id: int, mission_service: MissionServiceDep) -> AssignMissionResponse: 
    return await mission_service.assign_mission_to_spy_cat(spy_cat_id, mission_id)


@router.put("/{mission_id}")
async def update_mission(mission_id: int, payload: UpdateMissionRequest, mission_service: MissionServiceDep) -> UpdateMissionResponse: 
    return await mission_service.update_mission(mission_id, payload) 


@router.delete("/{mission_id}")
async def delete_mission(mission_id: int, mission_service: MissionServiceDep) -> DeleteMissionResponse: 
    return await mission_service.delete_mission(mission_id)
