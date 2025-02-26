from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional
from app.domain.model.application import (
    JobPosition, CivilStatus, EducationLevel, SubmissionRole, VisaStatus,
    ApplicationStatus, COCVerificationStatus
)

# Work Experience Schema
class WorkExperienceBase(BaseModel):
    country: str = Field(..., title="Country")
    position: JobPosition = Field(..., title="Position")
    other_job: Optional[str] = Field(None, title="Other Job Position")
    experience_others: Optional[str] = Field(None, title="Other Experience Details")
    duration: int = Field(..., title="Duration (Years)")

class WorkExperienceCreate(WorkExperienceBase):
    pass

class WorkExperienceResponse(WorkExperienceBase):
    id: int
    # class Config:
    #     orm_mode = True

# Main Job Application Schema
class JobApplicationBase(BaseModel):
    full_name: str
    job_applied: JobPosition
    other_job: Optional[str]
    contract_time: int
    monthly_salary: float
    gender: str
    complexion: str
    civil_status: CivilStatus

    emergency_contact_name: str
    emergency_contact_phone: str

    latest_education: EducationLevel
    education_others: Optional[List[str]]

    passport_no: str
    place_of_issue: str
    date_of_issue: date
    date_of_expire: date

    nationality: str
    religion: str
    date_of_birth: date
    age: int
    place_of_birth: str
    home_address: str
    contact_no: str
    children: int
    weight: float
    height: float

    speaks_english: bool = False
    speaks_arabic: bool = False
    speaks_other_languages: bool = False

    skill_cleaning: bool = False
    skill_washing: bool = False
    skill_ironing: bool = False
    skill_cooking: bool = False
    skill_baby_sitting: bool = False
    skill_children_care: bool = False
    skill_elder_care: bool = False
    other_skills: Optional[List[str]]

    remarks: Optional[str]
    name_signature: str

    application_status: ApplicationStatus
    missing_files_status: bool = True
    coc_verification_status: COCVerificationStatus
    visa_status: VisaStatus

    submit_to: SubmissionRole

    # Photo URIs
    photo_uri: Optional[List[str]]
    passport_photo_uri: Optional[List[str]]
    medical_photo_uri: Optional[List[str]]
    educational_photo_uri: Optional[List[str]]
    work_experience_photo_uri: Optional[List[str]]
    coc_photo_uri: Optional[List[str]]

class JobApplicationCreate(JobApplicationBase):
    work_experiences: List[WorkExperienceCreate] = []

class JobApplicationResponse(JobApplicationBase):
    id: int
    work_experiences: List[WorkExperienceResponse] = []

    # class Config:
    #     orm_mode = True
