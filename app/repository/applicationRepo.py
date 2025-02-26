from sqlalchemy.orm import Session
from app.domain.model.application import JobApplication, WorkExperience
from app.domain.schema.authSchema import tokenLoginData, editUser
from app.utils.security.jwt_handler import create_access_token, create_refresh_token

class ApplicationRepostory:
    def __init__(self, db: Session):
        self.db = db
    
    def create_application(self, application: JobApplication):
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application
    
    def get_all_applications(self):
        return self.db.query(JobApplication).all()