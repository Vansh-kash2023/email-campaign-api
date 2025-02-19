from typing import List, Literal
from pydantic import BaseModel, EmailStr

class Contact(BaseModel):
    name: str
    email: EmailStr
    job_title: str

class Account(BaseModel):
    account_name: str
    industry: str
    pain_points: List[str]
    contacts: List[Contact]
    campaign_objective: Literal["awareness", "nurturing", "upselling"]

class InputData(BaseModel):
    accounts: List[Account]
    number_of_emails: int

class Email(BaseModel):
    subject: str
    body: str
    call_to_action: str

class Campaign(BaseModel):
    account_name: str
    emails: List[Email]

class SuccessResponse(BaseModel):
    campaigns: List[Campaign]

class ErrorResponse(BaseModel):
    error: str
