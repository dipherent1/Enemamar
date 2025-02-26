from fastapi import APIRouter, HTTPException, Request
from app.domain.schema.applicationSchema import JobApplicationBase
from fastapi import Depends, Header
from app.service.applicationService import get_application_service, ApplicationService
from app.utils.middleware.dependancies import is_admin

applicationRouter = APIRouter(
    prefix="/application",
    tags=["application"]
)

# Create application
@applicationRouter.post("/")
async def create_application(application: JobApplicationBase, application_service: ApplicationService = Depends(get_application_service)):
    return application_service.create_application(application)

# Get all applications
@applicationRouter.get("/")
async def get_all_applications(application_service: ApplicationService = Depends(get_application_service)):
    return application_service.get_all_applications()