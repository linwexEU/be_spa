from src.models.enums import State
from src.exceptions.service import DeleteAssignedMission, MissionAlreadtAssigned, MissionAlreadyCompleted, MissionNotFound, \
                                   SpyCatNotFound
from src.utils.service import BaseService
from src.schemas.mission import AssignMissionResponse, CreateMissionRequest, CreateMissionResponse, DeleteMissionResponse, \
                                SMission, ListInfo, Info, UpdateMissionRequest, UpdateMissionResponse
from src.api.services.commands.spy_cat import CheckSpyCatExistCommand
from src.utils.logger import log


class MissionService(BaseService): 
    @log
    async def select_all_missions(self) -> ListInfo: 
        async with self.uow: 
            missions = await self.uow.mission_repo.select() 
            return ListInfo.from_orm(missions) 
    
    @log
    async def select_mission(self, mission_id: int) -> Info: 
        async with self.uow:
            mission = await self.uow.mission_repo.select_one(mission_id)
            if mission is None: 
                raise MissionNotFound(f"Mission with id={mission_id} not found")
            return Info.from_orm(mission)

    @log
    async def create_mission(self, payload: CreateMissionRequest) -> CreateMissionResponse: 
        async with self.uow:
            # Check Spy cat exist
            if payload.spy_cat:
                cmd = CheckSpyCatExistCommand(payload.spy_cat, self.uow.spy_cat_repo)
                res = await cmd.execute()
                if not res: 
                    raise SpyCatNotFound(f"Spy cat with id={payload.spy_cat} not found")

            # Create Target
            target_id = await self.uow.target_repo.create(payload.target.model_dump())

            # Create Mission
            mission = SMission(spy_cat=payload.spy_cat, target=target_id)
            mission_id = await self.uow.mission_repo.create(mission.model_dump())

            return CreateMissionResponse(entity_id=mission_id)

    @log 
    async def assign_mission_to_spy_cat(self, spy_cat_id: int, mission_id: int) -> AssignMissionResponse: 
        async with self.uow:
            # Check Spy cat exist
            if spy_cat_id:
                cmd = CheckSpyCatExistCommand(spy_cat_id, self.uow.spy_cat_repo)
                res = await cmd.execute()
                if not res: 
                    raise SpyCatNotFound(f"Spy cat with id={spy_cat_id} not found") 

            # Check Mission exist
            mission = await self.uow.mission_repo.select_one(mission_id)
            if mission is None: 
                raise MissionNotFound(f"Mission with id={mission_id} not found")
            
            # Check if aleady assigned
            if mission.spy_cat: 
                raise MissionAlreadtAssigned(f"Mission with id={mission_id} already assigned to Spy cat with id={mission.fr_spy_cat.id}")

            # Assign mission
            mission_id = await self.uow.mission_repo.assign(mission_id, spy_cat_id)
            return AssignMissionResponse(entity_id=mission_id)
    
    @log
    async def update_mission(self, mission_id: int, payload: UpdateMissionRequest) -> UpdateMissionResponse: 
        async with self.uow:
            # Check Mission exist
            mission = await self.uow.mission_repo.select_one(mission_id)
            if mission is None: 
                raise MissionNotFound(f"Mission with id={mission_id} not found")
            
            # Check that mission isn't completed
            if payload.target.notes or payload.target.state: 
                if mission.state == State.Completed: 
                    raise MissionAlreadyCompleted("You can't change a completed mission")
                
            await self.uow.target_repo.update(mission.fr_target.id, payload.target.model_dump(exclude_none=True))

            # Check if state = Completed
            if payload.target.state == State.Completed:
                await self.uow.mission_repo.mark_as_completed(mission_id)

            return UpdateMissionResponse(entity_id=mission_id)

    @log
    async def delete_mission(self, mission_id: int) -> DeleteMissionResponse: 
        async with self.uow:
            # Check Mission exist
            mission = await self.uow.mission_repo.select_one(mission_id)
            if mission is None: 
                raise MissionNotFound(f"Mission with id={mission_id} not found")
            
            # Check Mission hasn't assigned yet
            if mission.spy_cat: 
                raise DeleteAssignedMission(f"Mission with id={mission_id} assigned and can't be deleted")

            mission_id = await self.uow.mission_repo.delete(mission_id)
            return DeleteMissionResponse(entity_id=mission_id)
