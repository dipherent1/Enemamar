from app.utils.exceptions.exceptions import ValidationError, DuplicatedError, NotFoundError
import re
from app.domain.schema.applicationSchema import JobApplicationBase
from app.domain.model.application import JobApplication, WorkExperience
from app.repository.applicationRepo import ApplicationRepostory
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.config.database import get_db
from app.utils.security.hash import hash_password, verify_password
from app.utils.security.jwt_handler import verify_access_token

class ApplicationService:
    def __init__(self, db):
        self.application_repo = ApplicationRepostory(db)
    
    def create_application(self, application: JobApplicationBase):
        # Convert application to JobApplication ORM object
        application = JobApplication(**application.model_dump(exclude_none=True))
        # Create the application
        try:
            application = self.application_repo.create_application(application)
        #check if duplicate
        except IntegrityError as e:
            raise DuplicatedError("Application already exists")
        #check if the field has wrong input
        except ValueError as e:
            raise ValidationError(str(e))
        
        # Return response
        response = {"detail": "Application created successfully", "application": application}
        return response
    
    def get_all_applications(self):
        applications = self.application_repo.get_all_applications()
        # Convert the applications to response model
        applications_response = [application.model_dump() for application in applications]
        # Return the response
        response = {"detail": "Applications retrieved successfully", "applications": applications_response}
        return response
    

def get_application_service(db: Session = Depends(get_db)):
    return ApplicationService(db)