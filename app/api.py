from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.gpt import generate_campaign_emails
from typing import List

# Define the input model
class Contact(BaseModel):
    name: str
    email: str
    job_title: str

class Account(BaseModel):
    account_name: str
    industry: str
    pain_points: List[str]
    contacts: List[Contact]
    campaign_objective: str

class CampaignRequest(BaseModel):
    accounts: List[Account]
    number_of_emails: int

# Define the response model
class Email(BaseModel):
    subject: str
    body: str
    call_to_action: str

class CampaignResponse(BaseModel):
    account_name: str
    emails: List[Email]

# Initialize the router
router = APIRouter()

@router.post("/generate-campaign/", response_model=List[CampaignResponse])
async def create_campaign(request: CampaignRequest):
    try:
        # Call the GPT function to generate campaign emails
        campaigns = await generate_campaign_emails(request)
        return campaigns
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
