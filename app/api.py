from fastapi import APIRouter, HTTPException, FastAPI
from app.gpt import generate_campaign_emails
from app.models import CampaignResponse, Account
from typing import List
from pydantic import BaseModel

# Input Models
class Contact(BaseModel):
    name: str
    email: str
    job_title: str

class CampaignRequest(BaseModel):
    accounts: List[Account]
    number_of_emails: int

# FastAPI Setup
router = APIRouter()

@router.post("/generate-campaign/", response_model=List[CampaignResponse])
async def create_campaign(request: CampaignRequest):
    try:
        campaigns = await generate_campaign_emails(request)
        return campaigns
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Main FastAPI app
app = FastAPI(title="ABM Email Campaign API")
app.include_router(router)
