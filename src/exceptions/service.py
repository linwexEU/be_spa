

class ServiceError(Exception): 
    pass 


class ValidateBreedError(ServiceError): 
    pass 


class SpyCatAlreadyExists(ServiceError): 
    pass 


class SpyCatNotFound(ServiceError): 
    pass 


class MissionNotFound(ServiceError): 
    pass 


class MissionAlreadtAssigned(ServiceError): 
    pass 


class DeleteAssignedMission(ServiceError): 
    pass 


class MissionAlreadyCompleted(ServiceError): 
    pass 
