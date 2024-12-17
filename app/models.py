from pydantic import BaseModel
from typing import List

# Contact Model
class Contact(BaseModel):
    name: str
    email: str
    job_title: str

# Account Model
class Account(BaseModel):
    account_name: str
    industry: str
    pain_points: List[str]
    contacts: List[Contact]
    campaign_objective: str

# Email Model
class Email(BaseModel):
    subject: str
    body: str
    call_to_action: str

# Campaign Response Model
class CampaignResponse(BaseModel):
    account_name: str
    emails: List[Email]
