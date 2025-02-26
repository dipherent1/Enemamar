from sqlalchemy import Integer, String, Date, Numeric, Boolean, ForeignKey, Enum, JSON, DateTime
from sqlalchemy.sql import func
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from enum import Enum as PyEnum
from app.core.config.database import Base

# Enums for dropdown selections
class JobPosition(PyEnum):
    houseMaid = "House Maid"
    babysitter = "Babysitter"
    cooker = "Cooker"
    driver = "Driver"
    others = "Others"

class CivilStatus(PyEnum):
    single = "Single"
    married = "Married"
    divorced = "Divorced"
    widowed = "Widowed"

class EducationLevel(PyEnum):
    primarySchool = "Primary School"
    highSchool = "High School"
    college = "College"
    additionalCourse = "Additional Course"

class SubmissionRole(PyEnum):
    admin = "Admin"
    manager = "Manager"

class VisaStatus(PyEnum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"

class ApplicationStatus(PyEnum):
    pending = "Pending"
    finalized = "Finalized"
    hired = "Hired"
    government_registered = "Government Registered"
    rejected = "Rejected"
    

class COCVerificationStatus(PyEnum):
    pending = "Pending"
    not_available = "Not Available"
    available = "Available"  # Fix the typo and ensure consistent casing
    approved_by_staff = "Approved by Staff"

class JobApplication(Base):
    __tablename__ = "job_applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # General Info
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    job_applied: Mapped[JobPosition] = mapped_column(Enum(JobPosition), nullable=False)
    other_job: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contract_time: Mapped[int] = mapped_column(Integer, nullable=False)
    monthly_salary: Mapped[float] = mapped_column(Numeric, nullable=False)
    gender: Mapped[str] = mapped_column(Enum("Male", "Female", name="gender_enum"), nullable=False)
    complexion: Mapped[str] = mapped_column(String(100), nullable=False)
    civil_status: Mapped[CivilStatus] = mapped_column(Enum(CivilStatus), nullable=False)

    # Emergency Contact
    emergency_contact_name: Mapped[str] = mapped_column(String(255), nullable=False)
    emergency_contact_phone: Mapped[str] = mapped_column(String(50), nullable=False)

    # Education Qualification
    latest_education: Mapped[EducationLevel] = mapped_column(Enum(EducationLevel), nullable=False)
    education_others: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    # Passport Detail
    passport_no: Mapped[str] = mapped_column(String(50), nullable=False)
    place_of_issue: Mapped[str] = mapped_column(String(255), nullable=False)
    date_of_issue: Mapped[date] = mapped_column(Date, nullable=False)
    date_of_expire: Mapped[date] = mapped_column(Date, nullable=False)

    # Application Detail
    nationality: Mapped[str] = mapped_column(String(100), nullable=False)
    religion: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    place_of_birth: Mapped[str] = mapped_column(String(255), nullable=False)
    home_address: Mapped[str] = mapped_column(String(500), nullable=False)
    contact_no: Mapped[str] = mapped_column(String(50), nullable=False)
    children: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[float] = mapped_column(Numeric, nullable=False)
    height: Mapped[float] = mapped_column(Numeric, nullable=False)

    # Languages
    speaks_english: Mapped[bool] = mapped_column(Boolean, default=False)
    speaks_arabic: Mapped[bool] = mapped_column(Boolean, default=False)
    speaks_other_languages: Mapped[bool] = mapped_column(Boolean, default=False)

    # Skills
    skill_cleaning: Mapped[bool] = mapped_column(Boolean, default=False)
    skill_washing: Mapped[bool] = mapped_column(Boolean, default=False)
    skill_ironing: Mapped[bool] = mapped_column(Boolean, default=False)
    skill_cooking: Mapped[bool] = mapped_column(Boolean, default=False)
    skill_baby_sitting: Mapped[bool] = mapped_column(Boolean, default=False)
    skill_children_care: Mapped[bool] = mapped_column(Boolean, default=False)
    skill_elder_care: Mapped[bool] = mapped_column(Boolean, default=False)
    other_skills: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    # Additional Information
    remarks: Mapped[str | None] = mapped_column(String(500), nullable=True)
    name_signature: Mapped[str] = mapped_column(String(255), nullable=False)

    # Status
    application_status: Mapped[ApplicationStatus] = mapped_column(Enum(ApplicationStatus), nullable=False, default = ApplicationStatus.pending)
    missing_files_status: Mapped[bool] = mapped_column(Boolean, default=True)
    coc_verification_status: Mapped[COCVerificationStatus] = mapped_column(
        Enum(COCVerificationStatus), 
        nullable=False, 
        default=COCVerificationStatus.not_available
    )
    visa_status: Mapped[VisaStatus] = mapped_column(
        Enum(VisaStatus), 
        nullable=False, 
        default=VisaStatus.pending
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),  # Use server_default for timestamp
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now(),  # Automatically update timestamp
    )
    # Submission Details
    submit_to: Mapped[SubmissionRole] = mapped_column(Enum(SubmissionRole), nullable=False)

    # Document Uploads (URIs for Photos)
    photo_uri: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)  # Profile Photos
    passport_photo_uri: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    medical_photo_uri: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    educational_photo_uri: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    work_experience_photo_uri: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    coc_photo_uri: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    # Relationship: one application can have multiple work experiences
    work_experiences: Mapped[list["WorkExperience"]] = relationship(
        "WorkExperience", back_populates="job_application", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class WorkExperience(Base):
    __tablename__ = "work_experiences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    job_application_id: Mapped[int] = mapped_column(Integer, ForeignKey("job_applications.id"), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    position: Mapped[JobPosition] = mapped_column(Enum(JobPosition), nullable=False)
    other_job: Mapped[str | None] = mapped_column(String(255), nullable=True)
    experience_others: Mapped[str | None] = mapped_column(String(255), nullable=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)

    job_application: Mapped["JobApplication"] = relationship("JobApplication", back_populates="work_experiences")
